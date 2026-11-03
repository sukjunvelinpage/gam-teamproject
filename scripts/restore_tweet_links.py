"""보류 트윗의 공개 t.co 연결 대상을 보존하고 검토 단서를 수집한다.

대상을 따라 임의 웹사이트에 접속하지 않는다. X의 status 링크는 로컬 공개
아카이브와 정확한 문자열 ID로 연결한다. 원글 내용의 의미 검토는 별도이다.
기존 연구자료를 쓰거나 수정하지 않는다. 중단 후 같은 명령으로 재개할 수 있다.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures
import csv
import datetime
import hashlib
import html
import json
import random
import re
import time
from pathlib import Path
from urllib.parse import urlsplit

import pandas as pd
import requests

BASE = Path(__file__).resolve().parents[1]
AUDIT = BASE / "docs/tweet_audit_2026-11-02"
OUT = AUDIT / "restoration"
INPUT = AUDIT / "remaining_context_required.csv"
REF = AUDIT / "independent_archive_reference.csv"
URL_RE = re.compile(r"https?://t[.]co/[A-Za-z0-9]+", re.I)
STATUS_RE = re.compile(r"^https?://(?:www[.])?(?:twitter[.]com|x[.]com)/(?:[^/?#]+/)?status(?:es)?/(\d+)(?:[/?#]|$)", re.I)
TRUSTED_ARTICLE_HOSTS = {"www.whitehouse.gov", "trumpwhitehouse.archives.gov", "www.reuters.com", "apnews.com", "www.apnews.com", "www.bbc.com", "www.bbc.co.uk", "www.foxnews.com", "www.cnbc.com", "www.washingtonexaminer.com", "www.breitbart.com", "www.newsmax.com", "thehill.com", "www.nytimes.com", "www.washingtonpost.com", "www.wsj.com", "www.businesswire.com", "www.prnewswire.com", "www.presidency.ucsb.edu"}


def resolve(url: str, timeout: int) -> dict:
    """t.co 첫 리다이렉트만 확인한다; 대상 호스트에 자동접속하지 않는다."""
    try:
        response = requests.get(url, allow_redirects=False, timeout=timeout, stream=True,
                                headers={"User-Agent": "Mozilla/5.0 (compatible; ResearchAudit/1.0)"})
        location = response.headers.get("Location", "")
        status = response.status_code
        response.close()
        return {"url": url, "http_status": status, "location": location,
                "outcome": "redirect" if 300 <= status < 400 and location else "not_redirect",
                "error": ""}
    except requests.RequestException as exc:
        return {"url": url, "http_status": "", "location": "", "outcome": "request_failed",
                "error": f"{type(exc).__name__}: {str(exc)[:250]}"}


def fetch_article(url: str, timeout: int) -> dict:
    """검증된 공개 호스트의 첫 응답만 확인한다. 유료벽·접근제한을 우회하지 않는다."""
    if urlsplit(url).scheme not in {"http", "https"} or urlsplit(url).hostname not in TRUSTED_ARTICLE_HOSTS:
        raise ValueError("허용되지 않은 기사 호스트")
    record = {"url": url, "retrieved_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "http_status": "", "outcome": "", "content_type": "", "title": "", "description": "",
              "published_time": "", "text_excerpt": "", "error": ""}
    try:
        response = requests.get(url, allow_redirects=False, timeout=timeout, stream=True,
                                headers={"User-Agent": "Mozilla/5.0 (compatible; ResearchAudit/1.0)"})
        record["http_status"] = response.status_code
        record["content_type"] = response.headers.get("Content-Type", "")
        if response.status_code != 200 or "html" not in record["content_type"].lower():
            record["outcome"] = "non_200_or_not_html"
            response.close()
            return record
        body = b""
        for chunk in response.iter_content(32768):
            body += chunk
            if len(body) >= 1500000:
                break
        response.close()
        text = body.decode(response.encoding or "utf-8", errors="replace")
        title = re.search(r"<title\b[^>]*>(.*?)</title\s*>", text, re.I | re.S)
        record["title"] = html.unescape(re.sub(r"\s+", " ", title.group(1)).strip()) if title else ""
        tags = re.findall(r"<meta\b[^>]*>", text, re.I)
        for tag in tags:
            attrs = dict((name.lower(), html.unescape(value)) for name, _, value in re.findall(r'''([\w:-]+)\s*=\s*(["'])(.*?)\2''', tag, re.S))
            key = (attrs.get("property") or attrs.get("name") or "").lower()
            if key in {"og:description", "description", "twitter:description"} and not record["description"]:
                record["description"] = attrs.get("content", "")[:1500]
            if key in {"article:published_time", "datepublished", "publishdate", "pubdate"} and not record["published_time"]:
                record["published_time"] = attrs.get("content", "")[:80]
        paragraphs = []
        for value in re.findall(r"<p\b[^>]*>(.*?)</p\s*>", text, re.I | re.S):
            clean = html.unescape(re.sub(r"<[^>]+>", " ", value))
            clean = re.sub(r"\s+", " ", clean).strip()
            if len(clean) >= 45:
                paragraphs.append(clean)
        record["text_excerpt"] = "\n".join(paragraphs)[:6000]
        record["outcome"] = "html_metadata_needs_manual_review"
    except (requests.RequestException, UnicodeError, LookupError) as exc:
        record["outcome"] = "request_failed"
        record["error"] = f"{type(exc).__name__}: {str(exc)[:250]}"
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=12)
    parser.add_argument("--limit", type=int, default=0, help="0은 전체 고유 URL")
    parser.add_argument("--retry-failed", action="store_true", help="연결 오류에 한해 재시도 (404/접근 차단 제외)")
    parser.add_argument("--fetch-articles", action="store_true", help="검증된 공개 호스트의 기사 메타데이터와 일부 본문 확인")
    args = parser.parse_args()
    if not 1 <= args.workers <= 8 or not 1 <= args.timeout <= 60:
        raise ValueError("workers는 1~8, timeout은 1~60초여야 함")
    random.seed(42)
    OUT.mkdir(parents=True, exist_ok=True)
    tweets = pd.read_csv(INPUT, dtype={"id": str}).fillna("")
    rows = []
    for row in tweets.itertuples(index=False):
        for url in dict.fromkeys(URL_RE.findall(str(row.text))):
            rows.append({"raw_row": int(row.raw_row), "stored_id": str(row.id), "audit_key": row.audit_key,
                         "stored_date_utc": row.date_utc, "tweet_text": row.text,
                         "original_url": url})
    source = pd.DataFrame(rows, columns=["raw_row", "stored_id", "audit_key", "stored_date_utc", "tweet_text", "original_url"])
    source.to_csv(OUT / "links_input_inventory.csv", index=False, encoding="utf-8-sig")
    checkpoint = OUT / "links_redirect_checkpoint.jsonl"
    old = []
    if checkpoint.exists():
        for line in checkpoint.read_text(encoding="utf-8").splitlines():
            if line.strip():
                old.append(json.loads(line))
    cache = {record["url"]: record for record in old}
    unique = list(dict.fromkeys(source.original_url))
    todo = [u for u in unique if u not in cache or (args.retry_failed and cache[u]["outcome"] == "request_failed")]
    if args.limit:
        todo = todo[:args.limit]
    print(f"{len(tweets)} tweets; {len(source)} URL occurrences; {len(unique)} unique; {len(todo)} pending", flush=True)
    with checkpoint.open("a", encoding="utf-8", newline="\n") as file:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(resolve, url, args.timeout): url for url in todo}
            for n, future in enumerate(concurrent.futures.as_completed(futures), 1):
                result = future.result()
                cache[result["url"]] = result
                file.write(json.dumps(result, ensure_ascii=False) + "\n")
                file.flush()
                if n % 50 == 0 or n == len(todo):
                    print(f"completed {n}/{len(todo)}", flush=True)
                time.sleep(0.03)

    reference = pd.read_csv(REF, skipinitialspace=True, dtype=str).fillna("")
    reference["exact_status_id"] = reference["Tweet URL"].str.extract(r"/status/(\d+)", expand=False).fillna("")
    # 같은 ID의 아카이브 문구가 여러 개면 무작위로 하나를 선택하지 않는다.
    matches = {}
    for status_id, group in reference.groupby("exact_status_id", sort=False):
        if not status_id:
            continue
        variants = group["Tweet Text"].drop_duplicates().tolist()
        matches[status_id] = variants
    output = []
    for row in source.itertuples(index=False):
        result = cache.get(row.original_url, {"http_status": "", "location": "", "outcome": "not_attempted", "error": ""})
        loc = result["location"]
        m = STATUS_RE.match(loc)
        matched_id = m.group(1) if m else ""
        texts = matches.get(matched_id, [])
        reference_url = "https://github.com/MarkHershey/CompleteTrumpTweetsArchive/blob/master/data/realDonaldTrump_in_office.csv" if texts else ""
        linked_is_media = bool(re.search(r"/(?:photo|video)/\d+", loc, re.I))
        is_same_post = bool(matched_id and row.stored_id.isdecimal() and abs(int(matched_id) - int(row.stored_id)) < 512)
        # Snowflake의 상위 비트로 게시 순서를 대조한다. 초·날짜 경계에서
        # 하위 ID 손상으로 같은 밀리초가 될 수 있으므로 그 경우도 불확정이다.
        is_later_or_simultaneous = bool(matched_id and row.stored_id.isdecimal() and
                                       (int(matched_id) >> 22) >= (int(row.stored_id) >> 22))
        if linked_is_media:
            evidence_state = "media_not_recovered"
            recovered = ""
        elif is_same_post:
            evidence_state = "same_post_no_new_context"
            recovered = ""
        elif is_later_or_simultaneous:
            evidence_state = "linked_post_not_strictly_earlier"
            recovered = ""
        elif len(texts) == 1 and (len(texts[0].strip()) < 20 or re.search(r"(?:\.\.\.|…)\s*$", texts[0])):
            evidence_state = "linked_reference_truncated_or_short"
            recovered = ""
        elif len(texts) == 1:
            evidence_state = "exact_linked_status_id_local_reference"
            recovered = texts[0]
        elif len(texts) > 1:
            evidence_state = "conflicting_reference_texts"
            recovered = ""
        elif result["outcome"] == "redirect":
            evidence_state = "redirect_only_no_content"
            recovered = ""
        else:
            evidence_state = result["outcome"]
            recovered = ""
        output.append({**row._asdict(), **result, "linked_status_id": matched_id,
                       "destination_host": urlsplit(loc).hostname or "",
                       "reference_variant_count": len(texts), "reference_text": recovered,
                       "reference_source": reference_url, "evidence_state": evidence_state,
                       "temporal_note": "연결 자료가 게시 시점에 확인 가능했는지는 별도 검증 필요; 가격 데이터로 라벨 결정 금지"})
    fields = ["raw_row", "stored_id", "audit_key", "stored_date_utc", "tweet_text", "original_url", "url", "http_status", "location", "outcome", "error", "linked_status_id", "destination_host", "reference_variant_count", "reference_text", "reference_source", "evidence_state", "temporal_note"]
    with (OUT / "links_restoration_evidence.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(output)
    attempted = [v for k, v in cache.items() if k in set(unique)]
    summary = {"input_rows": len(tweets), "rows_with_tco": int(source.raw_row.nunique()),
               "tco_occurrences": len(source), "unique_tco": len(unique),
               "attempted_unique_tco": len(attempted),
               "redirect_outcomes": dict(collections.Counter(x["outcome"] for x in attempted)),
               "evidence_states_occurrences": dict(collections.Counter(x["evidence_state"] for x in output)),
               "tweets_with_exact_reference": len({x["raw_row"] for x in output if x["evidence_state"] == "exact_linked_status_id_local_reference"}),
               "input_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
               "limitations": ["리다이렉트만 확인한 글은 원문 복원이 아님", "X 링크라도 링크 대상과 원 트윗 본문이 같다는 뜻이 아님", "아카이브 인코딩·잘림·공개시각 검증 필요", "이미지·영상·기사 본문은 자동 복원하지 않음", "서로 다른 ID는 동일 문구여도 별도 사건이며 동일 ID는 중복 게시 가능"]}
    (OUT / "links_restoration_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    if args.fetch_articles:
        article_urls = sorted({x["location"] for x in output if urlsplit(x["location"]).hostname in TRUSTED_ARTICLE_HOSTS})
        article_path = OUT / "links_article_checkpoint.jsonl"
        article_cache = {}
        if article_path.exists():
            article_cache = {x["url"]: x for x in (json.loads(line) for line in article_path.read_text(encoding="utf-8").splitlines() if line.strip())}
        remaining = [u for u in article_urls if u not in article_cache]
        print(f"approved article-host URLs: {len(article_urls)}; pending: {len(remaining)}", flush=True)
        with article_path.open("a", encoding="utf-8", newline="\n") as file:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
                futures = {pool.submit(fetch_article, u, args.timeout): u for u in remaining}
                for n, future in enumerate(concurrent.futures.as_completed(futures), 1):
                    result = future.result()
                    article_cache[result["url"]] = result
                    file.write(json.dumps(result, ensure_ascii=False) + "\n")
                    file.flush()
                    if n % 25 == 0 or n == len(remaining):
                        print(f"article completed {n}/{len(remaining)}", flush=True)
                    time.sleep(0.03)
        evidence = []
        for row in output:
            article = article_cache.get(row["location"])
            if article:
                source_id = row["stored_id"]
                snow = pd.to_datetime((int(source_id) >> 22) + 1288834974657, unit="ms", utc=True) if source_id.isdecimal() else pd.NaT
                published = pd.to_datetime(article["published_time"], utc=True, errors="coerce")
                # 날짜만 있는 메타데이터는 자정으로 인위적 보정하지 않는다.
                precise = bool(re.search(r"\d{1,2}:\d{2}", article["published_time"]))
                if pd.isna(snow) or pd.isna(published) or not precise:
                    time_relation = "발행시각 불명확·별도검증"
                elif published > snow:
                    time_relation = "메타데이터 발행이 트윗보다 늦음·원인검증"
                else:
                    time_relation = "메타데이터 발행은 트윗 이전·현재내용 변경가능"
                evidence.append({"raw_row": row["raw_row"], "audit_key": row["audit_key"], "tweet_date_utc": row["stored_date_utc"],
                                 "tweet_snowflake_utc": str(snow) if not pd.isna(snow) else "", "publication_time_relation": time_relation,
                                 "tweet_text": row["tweet_text"], "original_url": row["original_url"], **article,
                                 "review_status": "기사 출처·게시시각·본문 확인 전 미확정"})
        pd.DataFrame(evidence).to_csv(OUT / "links_article_evidence.csv", index=False, encoding="utf-8-sig")
        print("article outcomes " + json.dumps(dict(collections.Counter(x["outcome"] for x in article_cache.values())), ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
