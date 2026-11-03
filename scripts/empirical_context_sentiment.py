"""
Full-Context Tweet Signal Classification Merger & Multi-Lag Empirical Analysis
------------------------------------------------------------------------------
1. Merges full-context tweet classifications (Positive / Negative / Noise) across
   all 1,246 economic/policy tweets (1,237 audit set + 9 pipeline overlap).
2. Updates:
   - data/trade_tweets_raw_audit.csv (preserving existing columns + adding context columns)
   - data/trump_market_extended_data.csv (preserving all 95 base columns + adding context signal columns)
3. Evaluates Welch's t-test (equal_var=False) across multi-day lag structures:
   - Day T, Day T+1, CAR[0, +1], CAR[0, +2]
   - Compares Positive Signal vs Negative Signal vs Non-Signal Trading Days.
"""

import os
import json
import numpy as np
import pandas as pd
from scipy import stats

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DRAFT_DIR = os.path.join(BASE_DIR, "Draft")

MARKET_CSV = os.path.join(DATA_DIR, "trump_market_extended_data.csv")
AUDIT_CSV = os.path.join(DATA_DIR, "trade_tweets_raw_audit.csv")
DRAFT_AUDIT_CSV = os.path.join(DRAFT_DIR, "trade_tweets_raw_audit.csv")
FULL_CONTEXT_TWEETS_CSV = os.path.join(DATA_DIR, "trump_policy_tweets_context_classified.csv")
SUMMARY_OUTPUT_CSV = os.path.join(DATA_DIR, "context_sentiment_empirical_summary.csv")

SCRATCH_DIR = r"C:\Users\StoneXI\.gemini\antigravity\brain\152489a7-01df-4aee-80e9-a9dc0b5abcee\scratch"


def get_sig_stars(p_val: float) -> str:
    if pd.isna(p_val):
        return "Not Sig"
    if p_val < 0.01:
        return "*** (p<0.01)"
    elif p_val < 0.05:
        return "** (p<0.05)"
    elif p_val < 0.10:
        return "* (p<0.10)"
    return "Not Sig"


def build_and_merge_datasets():
    print("=" * 85)
    print("[Step 1] Loading Full-Context Classifications for All 1,246 Tweets")
    print("=" * 85)

    if os.path.exists(FULL_CONTEXT_TWEETS_CSV) and not os.path.exists(os.path.join(SCRATCH_DIR, "all_1246_tweets.csv")):
        merged_tweets = pd.read_csv(FULL_CONTEXT_TWEETS_CSV)
    else:
        all_tweets = pd.read_csv(os.path.join(SCRATCH_DIR, "all_1246_tweets.csv"))
        classified = []
        for i in range(1, 6):
            batch_path = os.path.join(SCRATCH_DIR, f"classified_batch_{i}.json")
            with open(batch_path, "r", encoding="utf-8") as f:
                classified.extend(json.load(f))

        clf_df = pd.DataFrame(classified).sort_values("tweet_idx").reset_index(drop=True)
        clf_df = clf_df.rename(
            columns={
                "signal": "context_signal",
                "sub_type": "context_sub_type",
                "reason_ko": "context_reason_ko",
            }
        )
        polarity_map = {"Positive": 1, "Negative": -1, "Noise": 0}
        clf_df["signal_polarity_score"] = clf_df["context_signal"].map(polarity_map).fillna(0).astype(int)

        merged_tweets = all_tweets.merge(clf_df, on="tweet_idx", how="left")
        merged_tweets.to_csv(FULL_CONTEXT_TWEETS_CSV, index=False, encoding="utf-8-sig")

    print(f"Total tweets classified in full context: {len(merged_tweets):,}")
    print(merged_tweets["context_signal"].value_counts().to_string())
    print("\nGranular contextual sub-types:")
    print(merged_tweets["context_sub_type"].value_counts().to_string())

    # 1b. Update data/trade_tweets_raw_audit.csv and Draft/trade_tweets_raw_audit.csv
    lookup = merged_tweets[["tweet_text", "context_signal", "context_sub_type", "context_reason_ko", "signal_polarity_score"]].drop_duplicates(subset=["tweet_text"])

    for audit_path in [AUDIT_CSV, DRAFT_AUDIT_CSV]:
        if os.path.exists(audit_path):
            adf = pd.read_csv(audit_path)
            drop_cols = [c for c in ["context_signal", "context_sub_type", "context_reason_ko", "signal_polarity_score"] if c in adf.columns]
            if drop_cols:
                adf = adf.drop(columns=drop_cols)
            adf = adf.merge(lookup, on="tweet_text", how="left")
            adf.to_csv(audit_path, index=False, encoding="utf-8-sig")
            print(f"Updated contextual columns in: {audit_path} ({len(adf):,} rows)")

    # 2. Aggregate to 1,007 Trading Days in data/trump_market_extended_data.csv
    print("\n" + "=" * 85)
    print("[Step 2] Aggregating Contextual Positive/Negative Signals to 1,007 Trading Days")
    print("=" * 85)

    mkt_df = pd.read_csv(MARKET_CSV)
    # Keep only the original 95 base columns before appending
    base_cols = mkt_df.columns[:95].tolist()
    mkt_base = mkt_df[base_cols].copy()

    valid = merged_tweets.dropna(subset=["mapped_trading_date"]).copy()

    # A. Base Pipeline Trade Tweets (729 tweets) split by Full Context
    valid["is_trade_pos"] = ((valid["is_pipeline_trade"] == 1) & (valid["context_signal"] == "Positive")).astype(int)
    valid["is_trade_neg"] = ((valid["is_pipeline_trade"] == 1) & (valid["context_signal"] == "Negative")).astype(int)
    valid["is_trade_noise"] = ((valid["is_pipeline_trade"] == 1) & (valid["context_signal"] == "Noise")).astype(int)

    # B. Base Pipeline Fed Tweets (175 tweets) split by Full Context
    valid["is_fed_pos"] = ((valid["is_pipeline_fed"] == 1) & (valid["context_signal"] == "Positive")).astype(int)
    valid["is_fed_neg"] = (
        ((valid["is_pipeline_fed"] == 1) & (valid["context_signal"] == "Negative"))
        | (valid["context_sub_type"] == "NEG_Fed_Rate_Attack")
    ).astype(int)

    # C. Expanded Policy Tweets (Trade / Tariff / Industry / Company / Agriculture) split by Full Context
    valid["is_policy_pos"] = (
        (valid["context_signal"] == "Positive")
        & (valid["context_sub_type"].isin(["POS_Deal_Progress", "POS_Purchase_Agri_Support", "POS_US_Industry_Econ_Boom"]))
    ).astype(int)
    valid["is_policy_neg"] = (
        (valid["context_signal"] == "Negative")
        & (valid["context_sub_type"].isin(["NEG_Tariff_Threat_Action", "NEG_Protectionist_Attack", "NEG_Company_Tech_Pressure"]))
    ).astype(int)
    valid["is_all_neg"] = (valid["context_signal"] == "Negative").astype(int)
    valid["is_hard_tariff_neg"] = (valid["context_sub_type"] == "NEG_Tariff_Threat_Action").astype(int)
    valid["is_deal_pos"] = (valid["context_sub_type"] == "POS_Deal_Progress").astype(int)

    daily = valid.groupby("mapped_trading_date").agg(
        Trade_Pos_Count=("is_trade_pos", "sum"),
        Trade_Neg_Count=("is_trade_neg", "sum"),
        Trade_Noise_Count=("is_trade_noise", "sum"),
        Fed_Pos_Count=("is_fed_pos", "sum"),
        Fed_Neg_Count=("is_fed_neg", "sum"),
        Policy_Pos_Count=("is_policy_pos", "sum"),
        Policy_Neg_Count=("is_policy_neg", "sum"),
        Hard_Tariff_Neg_Count=("is_hard_tariff_neg", "sum"),
        Deal_Pos_Count=("is_deal_pos", "sum"),
        Policy_Pos_Retweet_Sum=("retweet_count", lambda s: s[valid.loc[s.index, "is_policy_pos"] == 1].sum()),
        Policy_Neg_Retweet_Sum=("retweet_count", lambda s: s[valid.loc[s.index, "is_policy_neg"] == 1].sum()),
    )

    # Construct new columns DataFrame aligned to mkt_base['Date']
    aligned_daily = daily.reindex(mkt_base["Date"]).fillna(0).astype(int).reset_index(drop=True)

    # Dummies and Pure Dummies (removing same-day offsetting ambiguity)
    aligned_daily["Trade_Pos_Dummy"] = (aligned_daily["Trade_Pos_Count"] > 0).astype(int)
    aligned_daily["Trade_Neg_Dummy"] = (aligned_daily["Trade_Neg_Count"] > 0).astype(int)
    aligned_daily["Trade_Pure_Pos_Dummy"] = ((aligned_daily["Trade_Pos_Count"] > 0) & (aligned_daily["Trade_Neg_Count"] == 0)).astype(int)
    aligned_daily["Trade_Pure_Neg_Dummy"] = ((aligned_daily["Trade_Neg_Count"] > 0) & (aligned_daily["Trade_Pos_Count"] == 0)).astype(int)
    aligned_daily["Trade_Net_Signal"] = np.sign(aligned_daily["Trade_Pos_Count"] - aligned_daily["Trade_Neg_Count"]).astype(int)

    aligned_daily["Fed_Pos_Dummy"] = (aligned_daily["Fed_Pos_Count"] > 0).astype(int)
    aligned_daily["Fed_Neg_Dummy"] = (aligned_daily["Fed_Neg_Count"] > 0).astype(int)

    aligned_daily["Policy_Pos_Dummy"] = (aligned_daily["Policy_Pos_Count"] > 0).astype(int)
    aligned_daily["Policy_Neg_Dummy"] = (aligned_daily["Policy_Neg_Count"] > 0).astype(int)
    aligned_daily["Policy_Pure_Pos_Dummy"] = ((aligned_daily["Policy_Pos_Count"] > 0) & (aligned_daily["Policy_Neg_Count"] == 0)).astype(int)
    aligned_daily["Policy_Pure_Neg_Dummy"] = ((aligned_daily["Policy_Neg_Count"] > 0) & (aligned_daily["Policy_Pos_Count"] == 0)).astype(int)
    aligned_daily["Policy_Net_Signal"] = np.sign(aligned_daily["Policy_Pos_Count"] - aligned_daily["Policy_Neg_Count"]).astype(int)

    aligned_daily["Hard_Tariff_Neg_Dummy"] = (aligned_daily["Hard_Tariff_Neg_Count"] > 0).astype(int)
    aligned_daily["Deal_Pos_Dummy"] = (aligned_daily["Deal_Pos_Count"] > 0).astype(int)

    final_mkt_df = pd.concat([mkt_base, aligned_daily], axis=1)
    final_mkt_df.to_csv(MARKET_CSV, index=False, encoding="utf-8-sig")

    print(f"Updated {MARKET_CSV}")
    print(f"Shape: {final_mkt_df.shape[0]} trading days x {final_mkt_df.shape[1]} columns (95 original + {aligned_daily.shape[1]} new context columns)")
    return final_mkt_df


def run_statistical_tests(df: pd.DataFrame):
    print("\n" + "=" * 85)
    print("[Step 3] Welch's t-test Analysis: Positive vs Negative Tweet Signals (Multi-Lag)")
    print("=" * 85)

    assets = [
        ("1. Macro & Sentiment", "S&P 500 (^GSPC)", "SP500"),
        ("1. Macro & Sentiment", "VIX Volatility (^VIX)", "VIX"),
        ("1. Macro & Sentiment", "Dollar Index (DXY)", "DXY"),
        ("2. US Sector - Protected", "Nucor Steel (NUE)", "NUE"),
        ("2. US Sector - Protected", "Steel ETF (SLX)", "SLX"),
        ("2. US Sector - Hurt", "Industrials ETF (XLI)", "XLI"),
        ("2. US Sector - Hurt", "Semiconductors ETF (SOXX)", "SOXX"),
        ("3. Target US Firms", "Apple (AAPL)", "AAPL"),
        ("3. Target US Firms", "Boeing (BA)", "BA"),
        ("3. Target US Firms", "Caterpillar (CAT)", "CAT"),
        ("4. Fed & Bonds", "10Y Treasury Yield (^TNX)", "TNX"),
        ("4. Fed & Bonds", "1-3Y Short Treasury (SHY)", "SHY"),
        ("4. Fed & Bonds", "Financials ETF (XLF)", "XLF"),
        ("5. China & Safe Haven", "China Large-Cap ETF (FXI)", "FXI"),
        ("5. China & Safe Haven", "USD/CNY Exchange Rate", "CNY"),
        ("5. China & Safe Haven", "Gold Safe Haven (GLD)", "GLD"),
    ]

    summary_rows = []
    none_mask = (df["Policy_Pos_Dummy"] == 0) & (df["Policy_Neg_Dummy"] == 0) & (df["Fed_Neg_Dummy"] == 0)

    for group_name, label, ticker in assets:
        r_t = df[f"{ticker}_Return"]
        r_t1 = r_t.shift(-1)
        cr_01 = (1 + r_t) * (1 + r_t1) - 1
        car_01 = cr_01 - cr_01.mean()
        r_t2 = r_t.shift(-2)
        cr_02 = (1 + r_t) * (1 + r_t1) * (1 + r_t2) - 1
        car_02 = cr_02 - cr_02.mean()

        lag_series = {
            "Day_T": r_t * 100,
            "Day_T+1": r_t1 * 100,
            "CAR[0,+1]": car_01 * 100,
            "CAR[0,+2]": car_02 * 100,
        }

        for window_name, s in lag_series.items():
            # 1) Policy Pure Positive vs Pure Negative
            pos_s = s[df["Policy_Pure_Pos_Dummy"] == 1].dropna()
            neg_s = s[df["Policy_Pure_Neg_Dummy"] == 1].dropna()
            non_s = s[none_mask].dropna()

            # Deal Progress vs Hard Tariff Shock
            deal_s = s[(df["Deal_Pos_Dummy"] == 1) & (df["Hard_Tariff_Neg_Dummy"] == 0)].dropna()
            hard_s = s[(df["Hard_Tariff_Neg_Dummy"] == 1) & (df["Deal_Pos_Dummy"] == 0)].dropna()

            t_pn, p_pn = stats.ttest_ind(pos_s, neg_s, equal_var=False)
            t_po, p_po = stats.ttest_ind(pos_s, non_s, equal_var=False)
            t_no, p_no = stats.ttest_ind(neg_s, non_s, equal_var=False)
            t_dh, p_dh = stats.ttest_ind(deal_s, hard_s, equal_var=False)

            summary_rows.append({
                "Group": group_name,
                "Asset": label,
                "Ticker": ticker,
                "Window": window_name,
                "Pure_Pos_Mean%": pos_s.mean(),
                "Pure_Neg_Mean%": neg_s.mean(),
                "No_Signal_Mean%": non_s.mean(),
                "Pos_vs_Neg_Diff%p": pos_s.mean() - neg_s.mean(),
                "Pos_vs_Neg_t": t_pn,
                "Pos_vs_Neg_p": p_pn,
                "Pos_vs_Neg_Sig": get_sig_stars(p_pn),
                "Pos_vs_None_Diff%p": pos_s.mean() - non_s.mean(),
                "Pos_vs_None_t": t_po,
                "Pos_vs_None_p": p_po,
                "Pos_vs_None_Sig": get_sig_stars(p_po),
                "Neg_vs_None_Diff%p": neg_s.mean() - non_s.mean(),
                "Neg_vs_None_t": t_no,
                "Neg_vs_None_p": p_no,
                "Neg_vs_None_Sig": get_sig_stars(p_no),
                "DealPos_Mean%": deal_s.mean(),
                "HardTariffNeg_Mean%": hard_s.mean(),
                "Deal_vs_Hard_Diff%p": deal_s.mean() - hard_s.mean(),
                "Deal_vs_Hard_t": t_dh,
                "Deal_vs_Hard_p": p_dh,
                "Deal_vs_Hard_Sig": get_sig_stars(p_dh),
                "N_Pure_Pos": len(pos_s),
                "N_Pure_Neg": len(neg_s),
                "N_No_Signal": len(non_s),
                "N_Deal_Pos": len(deal_s),
                "N_Hard_Neg": len(hard_s),
            })

    sum_df = pd.DataFrame(summary_rows)
    sum_df.to_csv(SUMMARY_OUTPUT_CSV, index=False, encoding="utf-8-sig")

    # Print Day_T and CAR[0,+1] highlights
    for win in ["Day_T", "CAR[0,+1]", "CAR[0,+2]"]:
        print(f"\n--- [{win}] Pure Positive (N=137) vs Pure Negative (N=113) vs No-Signal ---")
        sub = sum_df[sum_df["Window"] == win]
        print(f"{'Asset':<26} | {'Pos Mean':>9} | {'Neg Mean':>9} | {'Pos-Neg':>9} ({'p-val':>6}) | {'Neg-None':>9} ({'p-val':>6}) | {'Deal-Hard':>9} ({'p-val':>6})")
        print("-" * 105)
        for _, r in sub.iterrows():
            print(
                f"{r['Asset']:<26} | {r['Pure_Pos_Mean%']:>+8.3f}% | {r['Pure_Neg_Mean%']:>+8.3f}% | "
                f"{r['Pos_vs_Neg_Diff%p']:>+8.3f}%p ({r['Pos_vs_Neg_p']:.4f}) | "
                f"{r['Neg_vs_None_Diff%p']:>+8.3f}%p ({r['Neg_vs_None_p']:.4f}) | "
                f"{r['Deal_vs_Hard_Diff%p']:>+8.3f}%p ({r['Deal_vs_Hard_p']:.4f})"
            )

    print(f"\nSaved full multi-lag statistical summary to: {SUMMARY_OUTPUT_CSV}")


if __name__ == "__main__":
    df_merged = build_and_merge_datasets()
    run_statistical_tests(df_merged)
