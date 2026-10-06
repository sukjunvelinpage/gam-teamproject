"""
Audit & Validation Script for Trump Trade Tweets (729 raw matched tweets)
-------------------------------------------------------------------------
Step 1: Extracts all 729 tweets matching initial trade keywords with timestamps & engagement.
Step 2: Audits each tweet to identify:
  - Pure Trade/Tariff Policy Tweets (True Positives: tariffs, trade deals, deficit, IP theft, currency)
  - Non-Trade Noise / False Positives (e.g. 'China Virus' COVID blame, Biden/Election attacks, unrelated politics)
Outputs:
  - trade_tweets_raw_audit.csv: All 729 tweets with full text & audit classification
  - Audit statistics and error rate report
"""

import os
import re
import pandas as pd

TWEET_ARCHIVE_URL = "https://raw.githubusercontent.com/ttzztztz/TrumpTwitterArchive/master/trump.json"
START_DATE = "2017-01-20"
END_DATE = "2021-01-20"
OUTPUT_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trade_tweets_raw_audit.csv")

print("[Step 1] Loading raw Trump Twitter Archive ...")
raw_df = pd.read_json(TWEET_ARCHIVE_URL)
raw_df["date_utc"] = pd.to_datetime(raw_df["date"], utc=True)

# Filter 1st term
mask = (raw_df["date_utc"] >= f"{START_DATE} 00:00:00+00:00") & (
    raw_df["date_utc"] <= f"{END_DATE} 23:59:59+00:00"
)
tweets = raw_df.loc[mask].copy()

# Convert to Eastern Time
tweets["date_eastern"] = tweets["date_utc"].dt.tz_convert("America/New_York")
tweets["tweet_text"] = tweets["text"].fillna("").astype(str)
tweets["retweet_count"] = tweets["retweets"].fillna(0).astype(int)
tweets["favorite_count"] = tweets["favorites"].fillna(0).astype(int)

# Initial trade keyword filter
trade_keywords = ["tariff", "tariffs", "trade war", "china", "beijing", "xi jinping"]
trade_pattern = r"(?i)\b(" + "|".join([re.escape(k) for k in trade_keywords]) + r")\b"
matched_tweets = tweets[tweets["tweet_text"].str.contains(trade_pattern, regex=True)].copy()

print(f"      Initial matched trade tweets: {len(matched_tweets):,} 건")

# ==============================================================================
# Step 2: Content Audit & Granular Classification
# ==============================================================================
print("\n[Step 2] Auditing 729 tweets for Pure Trade vs False Positive Noise ...")

def classify_tweet_content(text: str):
    """
    Classifies whether the tweet is genuinely about Trade/Tariffs/Economic policy,
    or a False Positive / Political noise.
    """
    lower = text.lower()
    
    # 1. Obvious False Positive Patterns:
    # A) COVID-19 / Virus blaming without trade context
    covid_patterns = [
        "china virus", "chinese virus", "wuhan", "plague from china", "invisible enemy",
        "kung flu", "plague", "coronavirus", "covid"
    ]
    has_covid = any(p in lower for p in covid_patterns)
    
    # B) 2020 Election / Biden attacks without trade policy
    biden_patterns = [
        "biden", "sleepy joe", "hunter", "democrat", "election", "poll", "fake news", "obama"
    ]
    has_biden_politics = any(p in lower for p in biden_patterns)
    
    # C) True Trade / Tariff Indicators
    pure_trade_terms = [
        "tariff", "tariffs", "trade deal", "trade war", "trade deficit", "trade talks",
        "phase one", "phase 1", "farmers", "agriculture", "currency manipulation",
        "intellectual property", "wto", "negotiation", "negotiate", "export", "import",
        "duties", "commerce", "lighthizer", "mnuchin", "liu he", "billion in tariffs",
        "billions of dollars", "buy our product", "trade agreement", "usmca", "nafta",
        "trade barrier", "trade surplus", "reciprocal"
    ]
    has_pure_trade = any(p in lower for p in pure_trade_terms)
    
    # Decision Logic:
    # If it contains pure trade terms, it is genuinely economic trade related
    if has_pure_trade:
        category = "Pure_Trade_Tariff"
        is_pure_trade = 1
        noise_reason = "None (Genuine Trade/Tariff Policy)"
    elif has_covid:
        category = "COVID_Blame_Noise"
        is_pure_trade = 0
        noise_reason = "Blaming China for COVID-19 / Virus without trade policy"
    elif has_biden_politics:
        category = "Election_Political_Noise"
        is_pure_trade = 0
        noise_reason = "Domestic Political/Election attacks referencing China"
    else:
        # General diplomatic / foreign relations or miscellaneous mentioning China/Xi
        category = "Diplomatic_General_Noise"
        is_pure_trade = 0
        noise_reason = "General foreign policy / bilateral talk without tariff or trade specifics"
        
    return is_pure_trade, category, noise_reason

audit_results = matched_tweets["tweet_text"].apply(classify_tweet_content)
matched_tweets["is_pure_trade"] = [r[0] for r in audit_results]
matched_tweets["audit_category"] = [r[1] for r in audit_results]
matched_tweets["noise_reason"] = [r[2] for r in audit_results]

# Format output columns
output_df = matched_tweets[[
    "date_utc",
    "date_eastern",
    "tweet_text",
    "retweet_count",
    "favorite_count",
    "is_pure_trade",
    "audit_category",
    "noise_reason"
]].sort_values("date_eastern").reset_index(drop=True)

output_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"      Audit results saved to: {OUTPUT_CSV}")

# Summary Statistics
print("\n" + "=" * 75)
print("AUDIT SUMMARY REPORT: 729 TRADE/CHINA TWEETS")
print("=" * 75)
cat_counts = output_df["audit_category"].value_counts()
for cat, count in cat_counts.items():
    pct = count / len(output_df) * 100
    print(f"  - {cat:<26}: {count:>3}건 ({pct:>5.1f}%)")

pure_count = output_df["is_pure_trade"].sum()
noise_count = len(output_df) - pure_count
print("-" * 75)
print(f"  [True Positives] Pure Trade/Tariff Policy : {pure_count:,}건 ({pure_count/len(output_df)*100:.1f}%)")
print(f"  [False Positives] Non-Trade Political Noise: {noise_count:,}건 ({noise_count/len(output_df)*100:.1f}%)")
print(f"  [Error Rate] False Positive Rate           : {noise_count/len(output_df)*100:.1f}%")
print("=" * 75)

# Sample false positive inspect
print("\n[Sample False Positive Tweets (Noise Cases)]")
fp_samples = output_df[output_df["is_pure_trade"] == 0].head(5)
for idx, r in fp_samples.iterrows():
    clean_text = r['tweet_text'][:100].replace('\n', ' ')
    print(f"\n[{r['audit_category']}] {r['date_eastern'].strftime('%Y-%m-%d %H:%M')}")
    print(f"  Text: \"{clean_text}...\"")
    print(f"  Reason: {r['noise_reason']}")
