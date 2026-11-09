"""
Comparative Analysis:
Existing 1,246 Policy Tweets vs. Expanded 4,377 Candidate Tweets
Testing Welch's t-test and CAR across 16 financial assets.
"""
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

ROOT = Path(r"C:\Users\StoneXI\Agent_Workspace\gam-teamproject")
DATA = ROOT / "data"

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

def main():
    mkt = pd.read_csv(DATA / "trump_market_analysis_input.csv")
    
    # 4377-tweet based pure positive and negative days
    # Pure positive day: positive_event == 1 and negative_event == 0 and mixed_event == 0
    # Pure negative day: negative_event == 1 and positive_event == 0 and mixed_event == 0
    # No event day: positive_event == 0 and negative_event == 0 and mixed_event == 0
    mkt["Add_Pure_Pos"] = (
        (mkt["additional_tone_positive_event"] == 1)
        & (mkt["additional_tone_negative_event"] == 0)
        & (mkt["additional_tone_mixed_event"] == 0)
    ).astype(int)

    mkt["Add_Pure_Neg"] = (
        (mkt["additional_tone_negative_event"] == 1)
        & (mkt["additional_tone_positive_event"] == 0)
        & (mkt["additional_tone_mixed_event"] == 0)
    ).astype(int)

    mkt["Add_No_Signal"] = (
        (mkt["additional_tone_positive_event"] == 0)
        & (mkt["additional_tone_negative_event"] == 0)
        & (mkt["additional_tone_mixed_event"] == 0)
    ).astype(int)

    print("Existing (1,246 tweets) Days:")
    print("  Pure Pos Days:", int(mkt["Policy_Pure_Pos_Dummy"].sum()))
    print("  Pure Neg Days:", int(mkt["Policy_Pure_Neg_Dummy"].sum()))
    none_mask_old = (mkt["Policy_Pos_Dummy"] == 0) & (mkt["Policy_Neg_Dummy"] == 0) & (mkt["Fed_Neg_Dummy"] == 0)
    print("  No Signal Days:", int(none_mask_old.sum()))

    print("\nExpanded (4,377 tweets) Days:")
    print("  Pure Pos Days:", int(mkt["Add_Pure_Pos"].sum()))
    print("  Pure Neg Days:", int(mkt["Add_Pure_Neg"].sum()))
    print("  Both Pos & Neg (Contradictory/Mixed) Days:", int(((mkt['additional_tone_positive_event']==1) & (mkt['additional_tone_negative_event']==1)).sum()))
    print("  No Signal Days:", int(mkt["Add_No_Signal"].sum()))

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

    results = []

    for group, label, ticker in assets:
        r_t = mkt[f"{ticker}_Return"]
        r_t1 = r_t.shift(-1)
        cr_01 = (1 + r_t) * (1 + r_t1) - 1
        car_01 = cr_01 - cr_01.mean()
        r_t2 = r_t.shift(-2)
        cr_02 = (1 + r_t) * (1 + r_t1) * (1 + r_t2) - 1
        car_02 = cr_02 - cr_02.mean()

        windows = {
            "Day_T": r_t * 100,
            "Day_T+1": r_t1 * 100,
            "CAR[0,+1]": car_01 * 100,
            "CAR[0,+2]": car_02 * 100,
        }

        for win, s in windows.items():
            # --- OLD 1246 ---
            old_pos = s[mkt["Policy_Pure_Pos_Dummy"] == 1].dropna()
            old_neg = s[mkt["Policy_Pure_Neg_Dummy"] == 1].dropna()
            t_old, p_old = stats.ttest_ind(old_pos, old_neg, equal_var=False)

            # --- NEW 4377 ---
            new_pos = s[mkt["Add_Pure_Pos"] == 1].dropna()
            new_neg = s[mkt["Add_Pure_Neg"] == 1].dropna()
            t_new, p_new = stats.ttest_ind(new_pos, new_neg, equal_var=False)

            results.append({
                "Group": group,
                "Asset": label,
                "Ticker": ticker,
                "Window": win,
                "Old_Pos_Mean%": old_pos.mean(),
                "Old_Neg_Mean%": old_neg.mean(),
                "Old_Diff%p": old_pos.mean() - old_neg.mean(),
                "Old_p": p_old,
                "Old_Sig": get_sig_stars(p_old),
                "New_Pos_Mean%": new_pos.mean(),
                "New_Neg_Mean%": new_neg.mean(),
                "New_Diff%p": new_pos.mean() - new_neg.mean(),
                "New_p": p_new,
                "New_Sig": get_sig_stars(p_new),
            })

    res_df = pd.DataFrame(results)
    out_path = DATA / "comparison_old1246_vs_new4377.csv"
    res_df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print("\nWrote comparison table to", out_path)

    # Print summary highlights
    for w in ["Day_T", "CAR[0,+1]", "CAR[0,+2]"]:
        print(f"\n==================== Window: {w} ====================")
        sub = res_df[res_df["Window"] == w]
        print(f"{'Asset':<25} | {'Old Diff':>9} ({'p':>6}) {'Old Sig':<12} | {'New Diff':>9} ({'p':>6}) {'New Sig':<12}")
        print("-" * 80)
        for _, r in sub.iterrows():
            print(f"{r['Asset']:<25} | {r['Old_Diff%p']:>+8.3f}%p ({r['Old_p']:.4f}) {r['Old_Sig']:<12} | {r['New_Diff%p']:>+8.3f}%p ({r['New_p']:.4f}) {r['New_Sig']:<12}")

if __name__ == "__main__":
    main()
