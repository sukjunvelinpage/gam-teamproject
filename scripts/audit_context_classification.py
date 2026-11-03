"""트윗 전체 모집단의 분류·누락·거래일 연결을 읽기 전용으로 감사한다.

실행: python scripts/audit_context_classification.py
기존 데이터는 수정하지 않으며 docs/tweet_audit_2026-11-02에 근거를 저장한다.
정규식 경보는 의미 판독이나 정답 라벨을 대신하지 않는다.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "docs" / "tweet_audit_2026-11-02"
FILES = {
    "raw": BASE / "data/trump_tweets_1st_term_raw.csv",
    "classified": BASE / "data/trump_policy_tweets_context_classified.csv",
    "market": BASE / "data/trump_market_extended_data.csv",
}

# 기존 7대 도메인을 확장하되 넓은 거시·재정 후보는 별도로 구분한다.
PATTERNS = {
    "trade": r"\b(?:tariffs?|duties|trade|trading|nafta|usmca|korus|wto|tpp|trans.pacific|section\s*232|section\s*301|lighthizer|protectionis\w*|imports?|exports?|reciprocal|phase\s*(?:one|1)|buy american)\b",
    "china": r"\b(?:china|chinese|beijing|xi\s+jinping|president\s+xi|huawei|zte)\b",
    "monetary_fx": r"\b(?:fed|federal reserve|powell|yellen|interest\s+rates?|rate\s+(?:cuts?|hikes?)|quantitative|monetary|currency|currencies|devalu\w*|dollar|euro|yuan|renminbi)\b",
    "industry_farm": r"\b(?:steel|alumin\w*|farmers?|farming|soybeans?|agricultur\w*|farm\s+(?:aid|relief)|section\s*232)\b",
    "company_tech": r"\b(?:boeing|apple|caterpillar|huawei|zte|general motors|gm|ford|harley\w*|amazon|google|facebook|tiktok|wechat|qualcomm|broadcom|semiconduct\w*|tim\s+cook|5g)\b",
    "macro_fiscal_optional": r"\b(?:tax\s+(?:cuts?|reform|relief)|taxes|stimulus|relief\s+(?:bill|package)|paycheck\s+protection|cares\s+act|stock\s+market|dow|s&p|gdp|unemployment|jobs\s+report|oil|opec|sanctions?)\b",
}
ENTITY = r"\b(?:sidney\s*powell|sidneypowell\d*|colin\s+powell|dina\s+powell|shawn\s+steel|michelle\s+steel|man\s+of\s+steel|steel\s+(?:cages?|slats?|barrier|wall)|fed\s+up|(?:was|were|being|been)\s+fed|apple\s+(?:cart|doesn)|big\s+apple)\b"
DIRECT = r"\b(?:tariffs?|duties|trade\s+(?:deal|agreement|war)|usmca|nafta|wto|phase\s+(?:one|1)|federal\s+reserve|interest\s+rates?|currency\s+manip\w*|huawei|zte|soybeans?)\b"
HARD = r"\b(?:impos\w*|rais\w*|increas\w*|charg\w*|additional|effective|hereby|order\w*|ban\w*|restrict\w*|sanction\w*)\b"
POS = r"\b(?:deal|agreement|agreed|delay\w*|postpon\w*|suspend\w*|remov\w*|exempt\w*|progress|productive|good|great|buy\w*|purchas\w*)\b"
NEG = r"\b(?:tariffs?|deficit|unfair|bad|terrible|threat\w*|retaliat\w*|ban\w*|restric\w*|attack\w*|enemy)\b"


def normal(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(str(text))).strip()


def key(dt: str, text: str) -> str:
    return hashlib.sha256((str(pd.Timestamp(dt)) + "|" + normal(text)).encode()).hexdigest()


def has(pattern: str, text: str) -> bool:
    return bool(re.search(pattern, text, re.I))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    np.random.seed(42)
    OUT.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(FILES["raw"], dtype={"id": str})
    clf = pd.read_csv(FILES["classified"], dtype={"id": str})
    market = pd.read_csv(FILES["market"])
    raw["raw_row"] = np.arange(len(raw))
    raw["audit_key"] = [key(d, t) for d, t in zip(raw.date_utc, raw.text)]
    clf["audit_key"] = [key(d, t) for d, t in zip(clf.date_utc, clf.tweet_text)]
    columns = ["audit_key", "tweet_idx", "context_signal", "context_sub_type", "context_reason_ko", "mapped_trading_date"]
    ledger = raw.merge(clf[columns], on="audit_key", how="left", validate="many_to_one")
    ledger["in_classified"] = ledger.tweet_idx.notna()
    texts = ledger.text.fillna("").map(normal)
    for name, pattern in PATTERNS.items():
        ledger[name] = texts.map(lambda t: has(pattern, t))
    ledger["entity_or_idiom_flag"] = texts.map(lambda t: has(ENTITY, t))
    ledger["direct_policy_flag"] = texts.map(lambda t: has(DIRECT, t))
    ledger["retweet_flag"] = ledger.isRetweet.eq("t") | texts.str.startswith("RT @")
    ledger["fragment_flag"] = texts.str.contains(r"^(?:\.{2,}|…)|(?:\.{2,}|…)$", regex=True)
    ledger["link_only_flag"] = texts.str.replace(r"https?://\S+", "", regex=True).str.strip().str.len().lt(12)
    ledger["mixed_language_flag"] = texts.map(lambda t: has(POS, t) and has(NEG, t))
    ledger["candidate_themes"] = ledger.apply(lambda r: ";".join(n for n in PATTERNS if r[n]), axis=1)
    core = list(PATTERNS)[:-1]
    ledger["core_candidate"] = ledger[core].any(axis=1)
    ledger["screen_status"] = np.select(
        [ledger.in_classified, ledger.core_candidate, ledger.macro_fiscal_optional],
        ["existing_classified", "omission_candidate_not_confirmed", "optional_scope_candidate"],
        default="no_rule_hit_not_semantically_cleared",
    )
    # 우선순위는 검토 순서이며 누락/오분류 확정값이 아니다.
    ledger["priority"] = (ledger.direct_policy_flag.astype(int) * 4
                          + ledger.entity_or_idiom_flag.astype(int) * 3
                          + ledger.mixed_language_flag.astype(int)
                          + ledger.company_tech.astype(int)
                          + ledger.fragment_flag.astype(int))
    ledger.to_csv(OUT / "full_corpus_screening.csv", index=False, encoding="utf-8-sig")
    omissions = ledger.loc[~ledger.in_classified & ledger.core_candidate].sort_values(["priority", "date_utc"], ascending=[False, True])
    omissions.to_csv(OUT / "omission_candidates.csv", index=False, encoding="utf-8-sig")
    existing = ledger[ledger.in_classified].copy().sort_values("tweet_idx")
    existing["tweet_idx"] = existing.tweet_idx.astype(int)
    existing.to_csv(OUT / "existing_classification_audit.csv", index=False, encoding="utf-8-sig")

    # 로컬 거래일 spine 및 NYSE 실제 조기 폐장 시각을 각각 재계산한다.
    days = pd.DatetimeIndex(pd.to_datetime(market.Date))
    eastern = pd.to_datetime(clf.date_utc, utc=True).dt.tz_convert("America/New_York")
    local_days = eastern.dt.tz_localize(None).dt.normalize()
    target = local_days + pd.to_timedelta((eastern.dt.hour >= 16).astype(int), unit="D")
    idx = days.searchsorted(target)
    mapping = clf[["tweet_idx", "audit_key", "date_utc", "mapped_trading_date", "tweet_text"]].copy()
    mapping["fixed_16_expected"] = [str(days[i].date()) if i < len(days) else "" for i in idx]
    mapping["fixed_16_mismatch"] = mapping.mapped_trading_date.fillna("").ne(mapping.fixed_16_expected)
    import pandas_market_calendars as mcal
    schedule = mcal.get_calendar("NYSE").schedule(start_date=days.min(), end_date=days.max())
    close = pd.DatetimeIndex(schedule.market_close)
    ci = close.searchsorted(pd.to_datetime(clf.date_utc, utc=True), side="right")
    mapping["actual_close_expected"] = [str(schedule.index[i].date()) if i < len(schedule) else "" for i in ci]
    mapping["actual_close_mismatch"] = mapping.mapped_trading_date.fillna("").ne(mapping.actual_close_expected)
    # Snowflake 정수의 상위 비트는 생성 UTC 밀리초이다. 100 단위 ID 손실은
    # 2**22보다 작아 12시간 오차와는 규모가 전혀 다르다(초 경계는 유의).
    snow = pd.to_datetime(raw.id.map(lambda s: (int(s) >> 22) + 1288834974657), unit="ms", utc=True)
    raw_dt = pd.to_datetime(raw.date_utc, utc=True)
    timestamp = raw[["raw_row", "audit_key", "id", "date_utc", "text"]].copy()
    timestamp["snowflake_utc"] = snow.astype(str)
    timestamp["stored_minus_snowflake_seconds"] = (raw_dt - snow).dt.total_seconds()
    timestamp["timestamp_conflict"] = timestamp.stored_minus_snowflake_seconds.abs().gt(2)
    lookup = timestamp.set_index("audit_key")
    mapping["snowflake_utc"] = mapping.audit_key.map(lookup.snowflake_utc)
    mapping["timestamp_conflict"] = mapping.audit_key.map(lookup.timestamp_conflict)
    mapping["stored_minus_snowflake_seconds"] = mapping.audit_key.map(lookup.stored_minus_snowflake_seconds)
    snow_clf = pd.to_datetime(mapping.snowflake_utc, utc=True)
    snow_eastern = snow_clf.dt.tz_convert("America/New_York")
    snow_day = snow_eastern.dt.tz_localize(None).dt.normalize() + pd.to_timedelta((snow_eastern.dt.hour >= 16).astype(int), unit="D")
    si = days.searchsorted(snow_day)
    mapping["snowflake_fixed16_expected"] = [str(days[i].date()) if i < len(days) else "" for i in si]
    sci = close.searchsorted(snow_clf, side="right")
    mapping["snowflake_actual_close_expected"] = [str(schedule.index[i].date()) if i < len(schedule) else "" for i in sci]
    mapping["snowflake_fixed16_mismatch"] = mapping.mapped_trading_date.fillna("").ne(mapping.snowflake_fixed16_expected)
    mapping["snowflake_actual_close_mismatch"] = mapping.mapped_trading_date.fillna("").ne(mapping.snowflake_actual_close_expected)
    timestamp.to_csv(OUT / "raw_timestamp_audit.csv", index=False, encoding="utf-8-sig")
    mapping.to_csv(OUT / "trading_date_audit.csv", index=False, encoding="utf-8-sig")

    # 범주-극성 일관성, 반복 원문 라벨, 25개 집계열의 연결 검증.
    conflicts = []
    for text, g in clf.groupby("tweet_text"):
        if g.context_signal.nunique() > 1 or g.context_sub_type.nunique() > 1:
            conflicts.extend(g.to_dict("records"))
    pd.DataFrame(conflicts, columns=clf.columns).to_csv(OUT / "repeated_text_label_conflicts.csv", index=False, encoding="utf-8-sig")
    expected = pd.DataFrame(index=market.Date)
    fields = {
        "Trade_Pos_Count": clf.is_pipeline_trade.eq(1) & clf.context_signal.eq("Positive"),
        "Trade_Neg_Count": clf.is_pipeline_trade.eq(1) & clf.context_signal.eq("Negative"),
        "Trade_Noise_Count": clf.is_pipeline_trade.eq(1) & clf.context_signal.eq("Noise"),
        "Fed_Pos_Count": clf.is_pipeline_fed.eq(1) & clf.context_signal.eq("Positive"),
        "Fed_Neg_Count": (clf.is_pipeline_fed.eq(1) & clf.context_signal.eq("Negative")) | clf.context_sub_type.eq("NEG_Fed_Rate_Attack"),
        "Policy_Pos_Count": clf.context_signal.eq("Positive"),
        "Policy_Neg_Count": clf.context_signal.eq("Negative") & ~clf.context_sub_type.eq("NEG_Fed_Rate_Attack"),
        "Hard_Tariff_Neg_Count": clf.context_sub_type.eq("NEG_Tariff_Threat_Action"),
        "Deal_Pos_Count": clf.context_sub_type.eq("POS_Deal_Progress"),
    }
    for col, mask in fields.items():
        expected[col] = mask.groupby(clf.mapped_trading_date).sum().reindex(expected.index, fill_value=0)
    for label in ["Trade", "Policy"]:
        p, n = expected[f"{label}_Pos_Count"], expected[f"{label}_Neg_Count"]
        expected[f"{label}_Pos_Dummy"] = p.gt(0).astype(int)
        expected[f"{label}_Neg_Dummy"] = n.gt(0).astype(int)
        expected[f"{label}_Pure_Pos_Dummy"] = (p.gt(0) & n.eq(0)).astype(int)
        expected[f"{label}_Pure_Neg_Dummy"] = (n.gt(0) & p.eq(0)).astype(int)
        expected[f"{label}_Net_Signal"] = np.sign(p - n)
    for prefix in ["Fed_Pos", "Fed_Neg", "Hard_Tariff_Neg", "Deal_Pos"]:
        expected[f"{prefix}_Dummy"] = expected[f"{prefix}_Count"].gt(0).astype(int)
    for signal in ["Pos", "Neg"]:
        mask = fields[f"Policy_{signal}_Count"]
        expected[f"Policy_{signal}_Retweet_Sum"] = (clf.retweet_count * mask).groupby(clf.mapped_trading_date).sum().reindex(expected.index, fill_value=0)
    failures = []
    for c in expected:
        bad = expected[c].to_numpy() != market[c].to_numpy()
        for i in np.flatnonzero(bad):
            failures.append({"Date": market.Date.iloc[i], "column": c, "stored": market[c].iloc[i], "expected": expected[c].iloc[i]})
    pd.DataFrame(failures, columns=["Date", "column", "stored", "expected"]).to_csv(OUT / "daily_aggregation_mismatches.csv", index=False, encoding="utf-8-sig")
    reasons = clf.context_reason_ko.fillna("")
    stats = {
        "source_files": {k: {"path": str(p.relative_to(BASE)), "sha256": sha(p)} for k, p in FILES.items()},
        "raw_rows": len(raw), "classified_rows": len(clf), "market_rows": len(market), "market_columns": len(market.columns),
        "raw_timestamp_min": raw.date_utc.min(), "raw_timestamp_max": raw.date_utc.max(),
        "raw_id_duplicate_extra_rows": int(raw.id.duplicated().sum()),
        "raw_ids_ending_00": int(raw.id.str.endswith("00").sum()),
        "raw_time_text_duplicate_extra_rows": int(raw.duplicated(["date_utc", "text"]).sum()),
        "classified_unmatched_time_text": int((~clf.audit_key.isin(raw.audit_key)).sum()),
        "raw_missing_from_classified": int((~ledger.in_classified).sum()),
        "core_omission_candidates": len(omissions),
        "optional_only_candidates": int((ledger.screen_status == "optional_scope_candidate").sum()),
        "no_hit_rows": int((ledger.screen_status == "no_rule_hit_not_semantically_cleared").sum()),
        "signal_counts": clf.context_signal.value_counts().to_dict(),
        "subtype_counts": clf.context_sub_type.value_counts().to_dict(),
        "entity_flags_existing": int(existing.entity_or_idiom_flag.sum()),
        "repeated_text_conflict_rows": len(conflicts),
        "fixed16_mapping_mismatch_rows": int(mapping.fixed_16_mismatch.sum()),
        "actual_close_mapping_mismatch_rows": int(mapping.actual_close_mismatch.sum()),
        "raw_snowflake_timestamp_conflicts": int(timestamp.timestamp_conflict.sum()),
        "classified_snowflake_timestamp_conflicts": int(mapping.timestamp_conflict.sum()),
        "snowflake_fixed16_mapping_mismatch_rows": int(mapping.snowflake_fixed16_mismatch.sum()),
        "snowflake_actual_close_mapping_mismatch_rows": int(mapping.snowflake_actual_close_mismatch.sum()),
        "snowflake_actual_close_mapping_changed_signal_counts": clf.loc[mapping.snowflake_actual_close_mismatch, "context_signal"].value_counts().to_dict(),
        "market_calendar_missing_dates": sorted(set(schedule.index.strftime("%Y-%m-%d")) - set(market.Date)),
        "market_calendar_extra_dates": sorted(set(market.Date) - set(schedule.index.strftime("%Y-%m-%d"))),
        "daily_aggregation_mismatch_cells": len(failures), "daily_columns_checked": len(expected.columns),
        "reason_literal_replacement_rows": int(reasons.str.contains(chr(65533), regex=False).sum()),
        "reason_hangul_median_fraction": float(reasons.map(lambda s: sum('\uac00' <= c <= '\ud7a3' for c in s) / max(1, len(s))).median()),
        "raw_retweet_rows": int(ledger.retweet_flag.sum()),
        "classified_retweet_rows": int(existing.retweet_flag.sum()),
        "classified_fragment_rows": int(existing.fragment_flag.sum()),
        "classified_link_only_rows": int(existing.link_only_flag.sum()),
        "raw_before_inauguration_utc": int((pd.to_datetime(raw.date_utc, utc=True) < pd.Timestamp("2017-01-20T17:00:00Z")).sum()),
        "numpy_seed": 42,
    }
    (OUT / "audit_summary.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
