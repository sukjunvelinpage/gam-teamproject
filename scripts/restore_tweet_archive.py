"""보류 트윗을 공개 API 스냅샷과 대조한다. 원본 라벨은 수정하지 않는다."""
from __future__ import annotations

import bisect
import hashlib
import html
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/tweet_audit_2026-11-02"
OUT = BASE / "restoration"
FILES = {
    "bpb_master_2017": (OUT / "archive_master_2017.zip", "https://github.com/bpb27/trump_tweet_data_archive/blob/master/master_2017.json.zip"),
    "bpb_master_2018": (OUT / "archive_master_2018.zip", "https://github.com/bpb27/trump_tweet_data_archive/blob/master/master_2018.json.zip"),
    "pushshift": (OUT / "archive_pushshift.ndjson", "https://github.com/pushshift/realdonaldtrump/blob/master/realdonaldtrump_tweets.ndjson"),
}


def norm(value: str) -> str:
    s = html.unescape(str(value)).replace("&amp,", "&").replace("&amp;", "&")
    s = re.sub(r"https?://\S+", "", s)
    s = re.sub(r"\s+", " ", s).strip().casefold()
    return re.sub(r"[.…]+$", "", s).rstrip()


def timestamp(value):
    if isinstance(value, (int, float)):
        return pd.Timestamp(value, unit="s", tz="UTC")
    return pd.to_datetime(value, utc=True)


def full_text(record):
    return record.get("full_text") or record.get("extended_tweet", {}).get("full_text") or record.get("text") or ""


def urls(record):
    entities = record.get("extended_entities") or record.get("entities") or {}
    found = []
    for entity in entities.get("urls", []) + entities.get("media", []):
        for name in ("expanded_url", "media_url_https"):
            url = entity.get(name)
            if url and url not in found:
                found.append(url)
    return found


def main():
    pending = pd.read_csv(BASE / "remaining_context_required.csv", dtype={"id": str})
    cross = pd.read_csv(BASE / "exact_id_crosswalk.csv", dtype={"reference_exact_id": str}).set_index("raw_row")
    byid = {}
    metadata = []
    for name, (path, url) in FILES.items():
        if not path.exists():
            continue
        if path.suffix == ".zip":
            with zipfile.ZipFile(path) as z:
                data = json.loads(z.read(z.namelist()[0]))
        else:
            with path.open(encoding="utf-8") as stream:
                data = [json.loads(line) for line in stream if line.strip()]
        metadata.append({"source": name, "url": url, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "records": len(data), "time_min": min(str(timestamp(d["created_at"])) for d in data), "time_max": max(str(timestamp(d["created_at"])) for d in data)})
        for d in data:
            if "id_str" in d:
                byid.setdefault(d["id_str"], []).append((name, url, d))
    sorted_ids = sorted(map(int, byid))
    records = []
    for row in pending.itertuples():
        raw_id = int(row.id)
        pos = bisect.bisect_left(sorted_ids, raw_id)
        nearby = [str(x) for x in sorted_ids[max(0, pos-3):pos+4] if abs(x-raw_id) <= 512]
        reference_id = cross.at[row.raw_row, "reference_exact_id"] if row.raw_row in cross.index else None
        if pd.notna(reference_id) and str(reference_id) in nearby:
            nearby = [str(reference_id)]
        base = norm(row.text)
        matches = []
        for identifier in nearby:
            for name, url, d in byid[identifier]:
                expected_time = pd.Timestamp(((int(identifier) >> 22) + 1288834974657), unit="ms", tz="UTC")
                if abs((timestamp(d["created_at"]) - expected_time).total_seconds()) > 2:
                    continue
                candidate = norm(full_text(d))
                # 링크만 있는 글은 타임스탬프와 근접 ID만으로 동일성을 단정하지 않는다.
                if len(base) >= 18 and (candidate.startswith(base) or (len(candidate) >= 18 and base.startswith(candidate))):
                    matches.append((identifier, name, url, d))
        entry = {"raw_row": row.raw_row, "audit_key": row.audit_key, "stored_id": row.id, "stored_date_utc": row.date_utc, "original_text": row.text,
                 "archive_status": "unmatched_or_insufficient_identity", "source_name": "", "source_url": "", "exact_id": "", "source_tweet_url": "", "source_timestamp_utc": "", "archived_full_text": "", "retweeted_author": "", "retweeted_original_id": "", "retweeted_original_time_utc": "", "retweeted_original_text": "", "expanded_urls_json": "[]", "note_ko": "보류: 정확한 동일성 또는 추가 본문을 확인하지 못함. 연결 매체 미복원."}
        if matches:
            ids = set(x[0] for x in matches)
            if len(ids) == 1:
                # 중첩 리트윗과 더 긴 원문이 있는 스냅샷 우선.
                identifier, name, url, d = max(matches, key=lambda x: (bool(x[3].get("retweeted_status")), len(full_text(x[3]))))
                r = d.get("retweeted_status") or {}
                rt_time = timestamp(r["created_at"]) if r.get("created_at") else None
                outer_time = timestamp(d["created_at"])
                rt_valid = bool(rt_time is not None and rt_time <= outer_time)
                rt_text = full_text(r) if rt_valid else ""
                archived = full_text(d)
                baseline_length = len(norm(row.text))
                outer_expansion = len(norm(archived)) > baseline_length + 8
                rt_expansion = rt_valid and len(norm(rt_text)) > baseline_length + 8
                extra_urls = list(dict.fromkeys(urls(d) + (urls(r) if rt_valid else [])))
                status = "full_text_extended_review_required" if outer_expansion or rt_expansion else "metadata_only_review_required" if extra_urls else "matched_no_material_expansion"
                entry.update(archive_status=status, source_name=name, source_url=url, exact_id=identifier,
                    source_tweet_url=f"https://twitter.com/realDonaldTrump/status/{identifier}",
                    source_timestamp_utc=str(outer_time), archived_full_text=archived,
                    retweeted_author=(r.get("user") or {}).get("screen_name", "") if rt_valid else "",
                    retweeted_original_id=r.get("id_str", "") if rt_valid else "",
                    retweeted_original_time_utc=str(rt_time) if rt_valid else "", retweeted_original_text=rt_text,
                    expanded_urls_json=json.dumps(extra_urls,ensure_ascii=False),
                    note_ko="공개 API 스냅샷의 정확한 ID·생성시각과 18자 이상 본문 접두어 일치. 추가 텍스트/URL은 원문 검토 후보이며 자동 재분류하지 않음. 원문에 없는 미래 정보 사용 금지.")
            else:
                entry["archive_status"] = "multiple_ids_ambiguous"
                entry["note_ko"] = "둘 이상의 근접 ID가 본문과 일치하여 동일성을 확정하지 않음."
        records.append(entry)
    result = pd.DataFrame(records)
    assert len(result) == len(pending) and result.raw_row.is_unique
    result.to_csv(OUT / "archive_restoration_ledger.csv", index=False, encoding="utf-8-sig")
    summary = {"input_rows": len(result), "status_counts": result.archive_status.value_counts().to_dict(), "sources": metadata,
               "method": "근접 ID ±512, 검증 가능한 원문 접두어 최소 18자, 소스 ID 생성시각과 공개 API 게시시각 ±2초 확인. 정확 ID 교차표가 있으면 우선 사용. 의미 판단은 수행하지 않음.",
               "limitations": "URL만 있는 글은 동일성을 단정하지 않음. 2019~2021년 자료가 없는 스냅샷. 외부 기사·영상 원문 확인 및 개별 의미 재판정은 별도 필요."}
    (OUT / "archive_restoration_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    # 기존에 확보한 독립 참조본에서도 더 긴 본문을 찾되, 생략 표시가 있으면 부분 복원으로만 기록한다.
    reference = pd.read_csv(BASE / "independent_archive_reference.csv", dtype=str, skipinitialspace=True).fillna("")
    reference["exact_id"] = reference["Tweet URL"].str.extract(r"/status/(\d+)", expand=False).fillna("")
    refgroups = {key: group for key, group in reference.groupby("exact_id") if key}
    extensions = []
    for row in pending.itertuples():
        if row.raw_row not in cross.index:
            continue
        identifier = cross.at[row.raw_row, "reference_exact_id"]
        if pd.isna(identifier) or str(identifier) not in refgroups or abs(int(identifier) - int(row.id)) > 512:
            continue
        base = norm(row.text)
        if len(base) < 18:
            continue
        group = refgroups[str(identifier)]
        candidates = [r for r in group.itertuples(index=False, name=None) if norm(r[3]).startswith(base) and len(norm(r[3])) > len(base) + 8]
        if not candidates:
            continue
        # 상충하는 복수 본문은 자동으로 선택하지 않는다.
        texts = set(r[3] for r in candidates)
        if len(texts) != 1:
            continue
        ref = candidates[0]
        body = ref[3]
        without_urls = re.sub(r"https?://\S+", "", body).rstrip()
        partial = bool(re.search(r"(?:…|\.\.\.)\s*$", without_urls))
        source_time = pd.Timestamp((int(identifier) >> 22) + 1288834974657, unit="ms", tz="UTC")
        extensions.append({"raw_row": row.raw_row, "stored_id": row.id, "exact_id": identifier,
                           "original_text": row.text, "reference_text": body, "reference_tweet_url": ref[2],
                           "id_derived_time_utc": str(source_time), "reference_recorded_time": ref[1],
                           "completion_status": "partial_extension_review_required" if partial else "extended_text_review_required",
                           "note_ko": "독립 참조본의 정확 ID 교차표·근접 저장 ID·18자 이상 본문 접두어 대조. ID 유래 시간은 밀리초 수준이며 참조본 기록시각은 별도 보존. 본문 완전성·의미 및 외부 링크는 별도 확인 필요."})
    extcols = ["raw_row", "stored_id", "exact_id", "original_text", "reference_text", "reference_tweet_url", "id_derived_time_utc", "reference_recorded_time", "completion_status", "note_ko"]
    ext = pd.DataFrame(extensions, columns=extcols)
    ext.to_csv(OUT / "archive_independent_text_candidates.csv", index=False, encoding="utf-8-sig")
    summary["local_reference_extensions"] = {"rows": len(ext), "statuses": ext.completion_status.value_counts().to_dict(),
        "source_file": str((BASE / "independent_archive_reference.csv").relative_to(ROOT)),
        "source_sha256": hashlib.sha256((BASE / "independent_archive_reference.csv").read_bytes()).hexdigest()}
    (OUT / "archive_restoration_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
