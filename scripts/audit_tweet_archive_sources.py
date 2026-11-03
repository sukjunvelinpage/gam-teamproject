"""공개 참조 스냅샷을 대조하고 근접 ID·본문 유사도 교차키를 재현한다.

기본 실행은 저장된 스냅샷만 사용한다. 누락된 스냅샷을 새로 받으려면
python scripts/audit_tweet_archive_sources.py --download-missing 을 사용한다.
정밀 ID의 근접 연결은 잠정 대조키이며 정답 식별자 복구를 보증하지 않는다.
"""
from __future__ import annotations

import argparse
import bisect
import hashlib
import json
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd
import requests

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "docs/tweet_audit_2026-11-02"
REFERENCES = {
    "archive_reference.json": "https://raw.githubusercontent.com/ttzztztz/TrumpTwitterArchive/master/trump.json",
    "independent_archive_reference.csv": "https://raw.githubusercontent.com/MarkHershey/CompleteTrumpTweetsArchive/master/data/realDonaldTrump_in_office.csv",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download-missing", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, url in REFERENCES.items():
        target = OUT / filename
        if not target.exists():
            if not args.download_missing:
                raise FileNotFoundError(f"참조 사본 없음: {target}; --download-missing으로 수집 가능")
            response = requests.get(url, timeout=45)
            response.raise_for_status()
            target.write_bytes(response.content)

    raw = pd.read_csv(BASE / "data/trump_tweets_1st_term_raw.csv", dtype={"id": str})
    upstream = pd.DataFrame(json.loads((OUT / "archive_reference.json").read_text(encoding="utf-8")))
    upstream["date_utc"] = pd.to_datetime(upstream.date, utc=True)
    upstream = upstream[(upstream.date_utc >= "2017-01-20") & (upstream.date_utc < "2021-01-21")]
    raw_dates = pd.to_datetime(raw.date_utc, utc=True)
    local_set = Counter(zip(raw_dates, raw.text))
    upstream_set = Counter(zip(upstream.date_utc, upstream.text))
    ref = pd.read_csv(OUT / "independent_archive_reference.csv", skipinitialspace=True, dtype=str)
    ref["exact_id"] = ref["Tweet URL"].str.extract(r"/status/(\d+)", expand=False)
    sorted_ids = sorted((int(value), i) for i, value in enumerate(ref.exact_id))
    values = [value for value, _ in sorted_ids]
    result = []
    used = set()
    for n, row in enumerate(raw.itertuples()):
        value = int(row.id)
        pos = bisect.bisect_left(values, value)
        nearby = [(v, j) for v, j in sorted_ids[max(0, pos - 2):pos + 3] if abs(v - value) <= 512]
        record = {"raw_row": n, "stored_id": row.id, "source_date_utc": row.date_utc,
                  "reference_exact_id": "", "reference_url": "", "text_similarity": 0}
        if nearby:
            candidates = [(SequenceMatcher(None, str(row.text), str(ref.iloc[j]["Tweet Text"])).ratio(), v, j) for v, j in nearby]
            similarity, _, selected = max(candidates)
            match = ref.iloc[selected]
            record.update(reference_exact_id=match.exact_id, reference_url=match["Tweet URL"], text_similarity=similarity)
            used.add(match.exact_id)
        result.append(record)
    crosswalk = pd.DataFrame(result)
    crosswalk.to_csv(OUT / "exact_id_crosswalk.csv", index=False, encoding="utf-8-sig")
    unmatched = ref[~ref.exact_id.isin(used)]
    unmatched.to_csv(OUT / "independent_archive_unmatched_by_id.csv", index=False, encoding="utf-8-sig")
    report = {
        "local_rows": len(raw), "upstream_in_period_rows": len(upstream),
        "upstream_rows_missing_locally": sum((upstream_set - local_set).values()),
        "local_rows_missing_upstream": sum((local_set - upstream_set).values()),
        "secondary_reference_rows": len(ref), "secondary_unique_urls": ref["Tweet URL"].nunique(),
        "near_id_matched_raw_rows": int(crosswalk.reference_exact_id.ne("").sum()),
        "matched_text_similarity_ge_08": int(crosswalk.text_similarity.ge(.8).sum()),
        "secondary_unmatched_rows": len(unmatched),
        "source_hashes": {name: hashlib.sha256((OUT / name).read_bytes()).hexdigest() for name in REFERENCES},
        "match_rule": "저장ID와 참조ID 차이 512 이내의 근접 후보 중 본문 SequenceMatcher 유사도 최대값. 잠정 연결이며 ID 복원 보증 아님.",
    }
    (OUT / "archive_comparison_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
