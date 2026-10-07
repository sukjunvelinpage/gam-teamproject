"""
Comprehensive Audit & Extraction Script for Trump Economic/Trade/Policy Tweets
-------------------------------------------------------------------------------
Extracts and audits Trump 1st-term tweets matching multi-dimensional keywords:
  1. Trade & Tariffs: tariff, tariffs, trade war, trade deal, usmca, nafta, trade deficit, reciprocal
  2. China & Bilateral: china, beijing, xi jinping
  3. Fed & Monetary: fed, federal reserve, powell, interest rate, rate cut, rate hike, quantitative
  4. Steel & Aluminum: steel, aluminum (Section 232)
  5. Agriculture: farmers, soybeans (Retaliation & Purchase)
  6. Target Companies & Tech: boeing, apple, caterpillar, huawei, zte
  7. FX & Currency: currency manipulator, currency manipulation, strong dollar, devaluation

Outputs:
  - trade_tweets_raw_audit.csv: All 1,237 matched tweets with full text, matched keywords,
                                engagement metrics, and granular audit classifications.
"""

import os
import re
import pandas as pd

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_RAW_CSV = os.path.join(DATA_DIR, "trump_tweets_1st_term_raw.csv")
TWEET_ARCHIVE_URL = "https://raw.githubusercontent.com/ttzztztz/TrumpTwitterArchive/master/trump.json"
START_DATE = "2017-01-20"
END_DATE = "2021-01-20"
OUTPUT_CSV = os.path.join(DATA_DIR, "trade_tweets_raw_audit.csv")

# ==============================================================================
# Step 1: Load 1st Term Tweets
# ==============================================================================
if os.path.exists(LOCAL_RAW_CSV):
    print(f"[Step 1] Loading 1st term tweets from local file: {LOCAL_RAW_CSV} ...")
    tweets = pd.read_csv(LOCAL_RAW_CSV)
    tweets["date_utc"] = pd.to_datetime(tweets["date_utc"], utc=True)
else:
    print(f"[Step 1] Loading raw Trump Twitter Archive from {TWEET_ARCHIVE_URL} ...")
    raw_df = pd.read_json(TWEET_ARCHIVE_URL)
    raw_df["date_utc"] = pd.to_datetime(raw_df["date"], utc=True)
    mask = (raw_df["date_utc"] >= f"{START_DATE} 00:00:00+00:00") & (
        raw_df["date_utc"] <= f"{END_DATE} 23:59:59+00:00"
    )
    tweets = raw_df.loc[mask].copy()

# Convert to Eastern Time
tweets["date_eastern"] = tweets["date_utc"].dt.tz_convert("America/New_York")
tweets["tweet_text"] = tweets["text"].fillna("").astype(str)
tweets["retweet_count"] = tweets["retweets"].fillna(0).astype(int)
tweets["favorite_count"] = tweets["favorites"].fillna(0).astype(int)

# ==============================================================================
# Step 2: Multi-Category Keyword Definition & Extraction
# ==============================================================================
print("\n[Step 2] Defining expanded thematic keywords and extracting matching tweets ...")

KEYWORD_DICT = {
    "Trade_Tariff": [
        "tariff", "tariffs", "trade war", "trade deal", "usmca", "nafta", "trade deficit", "reciprocal"
    ],
    "China": [
        "china", "beijing", "xi jinping"
    ],
    "Fed_Monetary": [
        "fed", "federal reserve", "powell", "interest rate", "interest rates", "rate cut", "rate hike", "quantitative"
    ],
    "Steel_Aluminum": [
        "steel", "aluminum"
    ],
    "Agriculture_Retaliation": [
        "farmers", "soybeans"
    ],
    "Target_Company_Tech": [
        "boeing", "apple", "caterpillar", "huawei", "zte"
    ],
    "FX_Currency": [
        "currency manipulator", "currency manipulation", "strong dollar", "devaluation"
    ],
}

PATTERNS = {
    cat: r"(?i)\b(" + "|".join([re.escape(k) for k in kws]) + r")\b"
    for cat, kws in KEYWORD_DICT.items()
}

matched_rows = []
for idx, row in tweets.iterrows():
    text = row["tweet_text"]
    hit_cats = []
    hit_words = []
    for cat, pat in PATTERNS.items():
        found = re.findall(pat, text)
        if found:
            hit_cats.append(cat)
            hit_words.extend([f.lower() for f in found])

    if hit_cats:
        unique_words = sorted(list(set(hit_words)))
        matched_rows.append({
            "date_utc": row["date_utc"],
            "date_eastern": row["date_eastern"],
            "tweet_text": text,
            "retweet_count": row["retweet_count"],
            "favorite_count": row["favorite_count"],
            "matched_themes": "; ".join(hit_cats),
            "matched_keywords": ", ".join(unique_words),
        })

matched_df = pd.DataFrame(matched_rows)
print(f"      Total matched tweets across all expanded themes: {len(matched_df):,} 건 (전체 26,239건 중)")

# ==============================================================================
# Step 3: Granular Audit & Signal vs Noise Classification
# ==============================================================================
print("\n[Step 3] Auditing content: Pure Policy Signals vs Non-Policy Noise ...")

COVID_PATTERNS = [
    "china virus", "chinese virus", "wuhan", "plague from china", "invisible enemy",
    "kung flu", "plague", "coronavirus", "covid"
]
BIDEN_PATTERNS = [
    "biden", "sleepy joe", "hunter", "democrat", "election", "poll", "fake news", "obama"
]
TRADE_CORE = [
    "tariff", "tariffs", "trade deal", "trade war", "trade deficit", "phase one", "phase 1",
    "wto", "duties", "usmca", "nafta", "reciprocal", "commerce", "lighthizer"
]
FED_CORE = [
    "fed", "federal reserve", "powell", "interest rate", "rate cut", "rate hike", "quantitative"
]

def audit_tweet(row):
    text = row["tweet_text"]
    lower = text.lower()

    has_covid = any(p in lower for p in COVID_PATTERNS)
    has_biden = any(p in lower for p in BIDEN_PATTERNS)
    has_trade_core = any(p in lower for p in TRADE_CORE)
    has_fed_core = any(p in lower for p in FED_CORE)
    has_steel = any(p in lower for p in ["steel", "aluminum"])
    has_farm = any(p in lower for p in ["farmers", "soybeans"])
    has_tech = any(p in lower for p in ["boeing", "apple", "caterpillar", "huawei", "zte"])
    has_fx = any(p in lower for p in [
        "currency manipulator", "currency manipulation", "strong dollar", "devaluation"
    ])

    # 1. Fed & Monetary Policy
    if has_fed_core and not has_trade_core:
        category = "Fed_Monetary_Policy"
        is_signal = 1
        is_pure_trade = 0
        reason = "Federal Reserve interest rates and monetary policy pressure"
    # 2. Pure Trade & Tariff Policy
    elif has_trade_core or (has_steel and "tariff" in lower) or has_fx:
        category = "Pure_Trade_Tariff"
        is_signal = 1
        is_pure_trade = 1
        reason = "Genuine trade deals, tariffs, deficits, or currency policy"
    # 3. Steel & Aluminum Industrial Policy
    elif has_steel:
        category = "Steel_Aluminum_Industry"
        is_signal = 1
        is_pure_trade = 1 if "tariff" in lower else 0
        reason = "Domestic steel and aluminum industry protection/jobs"
    # 4. Agriculture & Farm Aid (Retaliation Cushion)
    elif has_farm:
        category = "Agriculture_Farm_Aid"
        is_signal = 1
        is_pure_trade = 0
        reason = "US farm aid packages and agricultural trade purchases"
    # 5. Targeted Companies & Tech Regulation
    elif has_tech:
        category = "Company_Tech_Target"
        is_signal = 1
        is_pure_trade = 0
        reason = "Direct corporate target or 5G/tech supply chain restriction"
    # 6. COVID-19 Blame Noise
    elif has_covid:
        category = "COVID_Blame_Noise"
        is_signal = 0
        is_pure_trade = 0
        reason = "COVID-19 / Virus blaming without economic policy specifics"
    # 7. Domestic Political / Election Noise
    elif has_biden:
        category = "Election_Political_Noise"
        is_signal = 0
        is_pure_trade = 0
        reason = "Domestic 2020 election campaign attacks referencing China"
    # 8. General Diplomatic Courtesy / Miscellaneous Noise
    else:
        category = "Diplomatic_General_Noise"
        is_signal = 0
        is_pure_trade = 0
        reason = "General foreign relations / courtesy talks without tariff specifics"

    return pd.Series([is_signal, is_pure_trade, category, reason])

audit_cols = matched_df.apply(audit_tweet, axis=1)
matched_df["is_policy_signal"] = audit_cols[0]
matched_df["is_pure_trade"] = audit_cols[1]
matched_df["audit_category"] = audit_cols[2]
matched_df["noise_reason"] = audit_cols[3]

# Sort chronologically
matched_df = matched_df.sort_values("date_eastern").reset_index(drop=True)

# Save to CSV
matched_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"      Successfully saved {len(matched_df):,} audited tweets to: {OUTPUT_CSV}")

# ==============================================================================
# Summary Statistics Report
# ==============================================================================
print("\n" + "=" * 80)
print(f"COMPREHENSIVE AUDIT REPORT: {len(matched_df):,} EXPANDED POLICY/TRADE TWEETS")
print("=" * 80)
cat_counts = matched_df["audit_category"].value_counts()
for cat, count in cat_counts.items():
    pct = count / len(matched_df) * 100
    print(f"  - {cat:<26}: {count:>4}건 ({pct:>5.1f}%)")

print("-" * 80)
sig_count = matched_df["is_policy_signal"].sum()
noise_count = len(matched_df) - sig_count
print(f"  [Policy Signals] Economic / Policy Tweets : {sig_count:,}건 ({sig_count/len(matched_df)*100:.1f}%)")
print(f"  [Non-Policy Noise] Political / Viral Noise  : {noise_count:,}건 ({noise_count/len(matched_df)*100:.1f}%)")
print("=" * 80)
