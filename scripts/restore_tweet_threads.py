"""보류된 트윗의 시간상 인접한 스레드 후보를 생성한다.

시간 근접과 말줄임표는 연결의 증거일 뿐, reply ID가 없으므로 스레드 확정은 아니다.
후행 게시물은 사후 참고 자료로만 기록하며 원래 게시시점의 정보집합에 넣지 않는다.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/trump_tweets_1st_term_raw.csv"
HOLD = ROOT / "docs/tweet_audit_2026-11-02/remaining_context_required.csv"
EXACT = ROOT / "docs/tweet_audit_2026-11-02/exact_id_crosswalk.csv"
OUT = ROOT / "docs/tweet_audit_2026-11-02/restoration"


def text_ends(value: str) -> bool:
    return bool(re.search(r"(?:\.{2,}|…)\s*$", value.strip()))


def text_starts(value: str) -> bool:
    return bool(re.search(r"^\s*(?:\.{2,}|…)", value))


def main() -> None:
    np.random.seed(42)
    OUT.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(DATA, dtype={"id": str}).fillna({"text": ""})
    target = pd.read_csv(HOLD, dtype={"id": str})
    assert len(target) == 3627 and target.raw_row.is_unique
    raw["raw_row"] = np.arange(len(raw))
    raw["text"] = raw.text.astype(str)
    assert all(raw.loc[int(x.raw_row), "text"] == str(x.text) for x in target.itertuples())
    # Snowflake의 하위 비트 정밀도 손상은 초 경계의 미세한 오차를 만들 수 있다.
    raw["snowflake_ms"] = raw.id.map(lambda value: (int(value) >> 22) + 1288834974657)
    raw["snowflake_utc"] = pd.to_datetime(raw.snowflake_ms, unit="ms", utc=True)
    raw["is_retweet"] = raw.isRetweet.eq("t") | raw.text.str.startswith("RT @")
    raw["fragment_start"] = raw.text.map(text_starts)
    raw["fragment_end"] = raw.text.map(text_ends)
    sorted_raw = raw.sort_values(["snowflake_ms", "id", "raw_row"]).reset_index(drop=True)
    positions = dict(zip(sorted_raw.raw_row, sorted_raw.index))
    verified = {}
    if EXACT.exists():
        cross = pd.read_csv(EXACT, dtype={"reference_exact_id": str})
        cross = cross[cross.reference_exact_id.notna() & cross.text_similarity.ge(.97)].copy()
        cross = cross[~cross.reference_exact_id.duplicated(keep=False)]
        verified = dict(zip(cross.raw_row.astype(int), cross.reference_exact_id))
    links = []
    for focus in target.itertuples():
        row = sorted_raw.loc[positions[focus.raw_row]]
        if row.is_retweet:
            continue
        for step, relationship in [(-1, "previous"), (1, "next")]:
            pos = positions[focus.raw_row] + step
            if pos < 0 or pos >= len(sorted_raw):
                continue
            adjacent = sorted_raw.loc[pos]
            if adjacent.is_retweet:
                continue
            delta_ms = int(adjacent.snowflake_ms - row.snowflake_ms)
            if abs(delta_ms) > 120_000:
                continue
            is_boundary = ((relationship == "previous" and row.fragment_start and adjacent.fragment_end)
                           or (relationship == "next" and row.fragment_end and adjacent.fragment_start))
            if not is_boundary:
                continue
            # 같은 초라면 손상된 ID와 시각 정밀도 때문에 선후관계 확정 불가.
            order = ("earlier" if delta_ms <= -1000 else "later" if delta_ms >= 1000 else "same_second_uncertain")
            source_order = "rounded_snowflake_conservative"
            if int(focus.raw_row) in verified and int(adjacent.raw_row) in verified:
                target_ms = (int(verified[int(focus.raw_row)]) >> 22) + 1288834974657
                adjacent_ms = (int(verified[int(adjacent.raw_row)]) >> 22) + 1288834974657
                # 서로 다른 밀리초는 시각 순서가 확정되지만, 동일 밀리초는 ID 값만으로 단정 불가.
                if target_ms != adjacent_ms:
                    order = "earlier" if adjacent_ms < target_ms else "later"
                    source_order = "near_id_and_text_similarity_ge_0.97_secondary_archive"
            links.append({
                "raw_row": int(focus.raw_row), "audit_key": focus.audit_key,
                "target_id_lossy": row.id, "target_stored_utc": focus.date_utc,
                "target_snowflake_utc": row.snowflake_utc.isoformat(), "target_text": row.text,
                "candidate_raw_row": int(adjacent.raw_row), "candidate_id_lossy": adjacent.id,
                "candidate_snowflake_utc": adjacent.snowflake_utc.isoformat(),
                "candidate_text": adjacent.text, "delta_seconds": delta_ms / 1000,
                "chronological_relation": order, "adjacency_direction": relationship,
                "ordering_basis": source_order,
                "evidence": "인접 본문 상호 말줄임표 및 120초 이내; 답글 관계 메타데이터 없음",
                "validation_state": "unverified_candidate_not_a_confirmed_thread",
                "available_for_asof_label": order == "earlier",
                "caveat": "이전 후보도 연결 검증 전 자동 분류 금지; 나중 후보는 해당 트윗 당시 라벨에 사용 금지; 동초 순서 미확정",
            })
    columns = ["raw_row", "audit_key", "target_id_lossy", "target_stored_utc", "target_snowflake_utc",
               "target_text", "candidate_raw_row", "candidate_id_lossy", "candidate_snowflake_utc",
               "candidate_text", "delta_seconds", "chronological_relation", "adjacency_direction", "ordering_basis",
               "evidence", "validation_state", "available_for_asof_label", "caveat"]
    candidates = pd.DataFrame(links, columns=columns)
    candidates.to_csv(OUT / "threads_candidates.csv", index=False, encoding="utf-8-sig")
    overview = target[["raw_row", "audit_key", "id", "date_utc", "text", "reason_ko"]].copy()
    for category in ["earlier", "later", "same_second_uncertain"]:
        counts = candidates.loc[candidates.chronological_relation.eq(category)].groupby("raw_row").size()
        overview[f"{category}_candidate_count"] = overview.raw_row.map(counts).fillna(0).astype(int)
    overview["candidate_count"] = overview[[f"{x}_candidate_count" for x in ["earlier", "later", "same_second_uncertain"]]].sum(axis=1)
    overview["state"] = np.where(overview.candidate_count.gt(0), "candidate_requires_manual_validation", "no_candidate_remains_unresolved")
    overview.to_csv(OUT / "threads_overview.csv", index=False, encoding="utf-8-sig")
    summary = {
        "scope": "기존 needs_context 3,627개 전체; 원시 26,239행을 비교 기준으로 사용",
        "target_rows": len(target), "targets_with_candidates": int(overview.candidate_count.gt(0).sum()),
        "targets_without_candidates": int(overview.candidate_count.eq(0).sum()),
        "target_retweets_excluded_from_thread_inference": int(raw.loc[target.raw_row, "is_retweet"].sum()),
        "candidate_links": len(candidates), "candidate_relation_counts": candidates.chronological_relation.value_counts().to_dict(),
        "algorithm": "정렬된 원시 게시물 중 인접한 본인 게시물, 120초 이내, 앞글 말줄임과 뒷글 선행 말줄임 동시 충족. RT 제외. 같은 초여도 양쪽 ID가 보조 아카이브에 고유 매칭되고 텍스트 유사도 0.97 이상이며 밀리초가 다르면 시각 순서만 추론. 답글 연결은 여전히 미검증.",
        "limitations": "Twitter 답글·스레드 원관계 필드가 없어 모든 연결은 가설이다. 인접한 별개의 글·누락된 중간글을 식별하지 못하며 비인접 스레드와 링크·이미지·영상은 검색하지 않는다. Snowflake ID 하위자릿수 손상으로 원본 ID와 초 경계를 완전히 복원할 수 없다. 이후 게시물은 사건 시점 판정에 절대 사용하지 않는다.",
        "sha256": {str(x.relative_to(ROOT)): hashlib.sha256(x.read_bytes()).hexdigest() for x in [DATA, HOLD, EXACT] if x.exists()},
    }
    (OUT / "threads_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
