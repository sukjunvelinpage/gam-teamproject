"""
Extended Empirical Analysis: Cross-Asset & Sector Impact of Trump Tweets
------------------------------------------------------------------------
Tests hypotheses across:
1. Baseline: S&P 500, VIX, DXY
2. US Sectors & Firms (Trade Tweets): Steel (NUE, SLX) vs Victims (XLI, SOXX, AAPL, BA, CAT)
3. Fed & Bonds (Fed Tweets): 10Y Yield (TNX), 1-3Y Treasury (SHY), Financials (XLF)
4. International & Safe Haven (Trade Tweets): China ETF (FXI), USD/CNY (CNY), Gold (GLD)
"""

import os
import pandas as pd
import numpy as np
from scipy import stats

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trump_market_extended_data.csv")

def run_extended_analysis():
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    print("=" * 80)
    print("EXTENDED EMPIRICAL STATISTICAL TEST RESULTS (2017 - 2021)")
    print(f"Total Trading Sessions: {len(df):,} days")
    print(f"Trade Tweet Days: {df['Trade_Tweet_Dummy'].sum()} | Fed Tweet Days: {df['Fed_Tweet_Dummy'].sum()}")
    print("=" * 80)

    results = []

    def evaluate_metric(dummy_col: str, metric_col: str, group_name: str, asset_label: str):
        sub = df.dropna(subset=[dummy_col, metric_col]).copy()
        ev = sub[sub[dummy_col] == 1][metric_col]
        no = sub[sub[dummy_col] == 0][metric_col]

        t_stat, p_val = stats.ttest_ind(ev, no, equal_var=False)
        ev_mean = ev.mean() * 100
        no_mean = no.mean() * 100
        diff = ev_mean - no_mean

        signif = "Not Sig"
        if p_val < 0.01:
            signif = "*** (p<0.01)"
        elif p_val < 0.05:
            signif = "** (p<0.05)"
        elif p_val < 0.10:
            signif = "* (p<0.10)"

        results.append({
            "Group": group_name,
            "Asset": asset_label,
            "Metric": metric_col,
            "Event_Mean%": ev_mean,
            "None_Mean%": no_mean,
            "Diff%p": diff,
            "t_stat": t_stat,
            "p_val": p_val,
            "Significance": signif,
            "N_Event": len(ev),
            "N_None": len(no)
        })

    # 1. Baseline
    evaluate_metric("Trade_Tweet_Dummy", "SP500_Return", "1. Baseline (Trade)", "S&P 500 Return")
    evaluate_metric("Trade_Tweet_Dummy", "VIX_Return", "1. Baseline (Trade)", "VIX Daily Change")
    evaluate_metric("Trade_Tweet_Dummy", "DXY_Return", "1. Baseline (Trade)", "Dollar Index Return")

    # 2. US Sector / Firm Asymmetry (Trade Tweets)
    # Tariff Protection Beneficiaries
    evaluate_metric("Trade_Tweet_Dummy", "NUE_Return", "2. US Sector - Protected", "Nucor Steel (NUE)")
    evaluate_metric("Trade_Tweet_Dummy", "SLX_Return", "2. US Sector - Protected", "Steel ETF (SLX)")

    # Tariff Victims (Sectors)
    evaluate_metric("Trade_Tweet_Dummy", "XLI_Return", "2. US Sector - Hurt", "Industrials ETF (XLI)")
    evaluate_metric("Trade_Tweet_Dummy", "SOXX_Return", "2. US Sector - Hurt", "Semiconductors (SOXX)")

    # Direct Target Companies
    evaluate_metric("Trade_Tweet_Dummy", "AAPL_Return", "2. Target US Firms", "Apple (AAPL)")
    evaluate_metric("Trade_Tweet_Dummy", "BA_Return", "2. Target US Firms", "Boeing (BA)")
    evaluate_metric("Trade_Tweet_Dummy", "CAT_Return", "2. Target US Firms", "Caterpillar (CAT)")

    # 3. Fed & Bonds (Fed Tweets)
    evaluate_metric("Fed_Tweet_Dummy", "TNX_Return", "3. Fed & Monetary", "10Y Treasury Yield Chg")
    evaluate_metric("Fed_Tweet_Dummy", "SHY_Return", "3. Fed & Monetary", "1-3Y Short Treasury (SHY)")
    evaluate_metric("Fed_Tweet_Dummy", "XLF_Return", "3. Fed & Monetary", "Financials ETF (XLF)")
    evaluate_metric("Fed_Tweet_Dummy", "SP500_Return", "3. Fed & Monetary", "S&P 500 (Fed Tweet)")

    # 4. China Spillover & Safe Haven (Trade Tweets)
    evaluate_metric("Trade_Tweet_Dummy", "FXI_Return", "4. China & Safe Haven", "China Large-Cap (FXI)")
    evaluate_metric("Trade_Tweet_Dummy", "CNY_Return", "4. China & Safe Haven", "USD/CNY (Yuan Deprec.)")
    evaluate_metric("Trade_Tweet_Dummy", "GLD_Return", "4. China & Safe Haven", "Gold ETF (GLD)")

    res_df = pd.DataFrame(results)
    
    # Print formatted table
    for grp, group_df in res_df.groupby("Group", sort=False):
        print(f"\n[{grp}]")
        print(f"{'Asset':<25} | {'Event Mean':>11} | {'None Mean':>11} | {'Diff':>10} | {'t-stat':>8} | {'p-val':>7} | {'Sig'}")
        print("-" * 88)
        for _, r in group_df.iterrows():
            print(f"{r['Asset']:<25} | {r['Event_Mean%']:>+10.3f}% | {r['None_Mean%']:>+10.3f}% | {r['Diff%p']:>+9.3f}%p | {r['t_stat']:>+8.3f} | {r['p_val']:>7.4f} | {r['Significance']}")

    # Also compute 2-day CAR for key assets
    print("\n" + "=" * 80)
    print("2-DAY EVENT WINDOW [T, T+1] CAR COMPARISON: S&P 500 vs FXI (China) vs CAT vs NUE")
    print("=" * 80)

    for asset in ["SP500", "FXI", "CAT", "BA", "AAPL", "NUE", "SOXX", "GLD"]:
        r_t = df[f"{asset}_Return"]
        r_t1 = df[f"{asset}_Return"].shift(-1)
        cr = (1 + r_t) * (1 + r_t1) - 1
        mean_cr = cr.mean()
        car = cr - mean_cr

        sub = df.dropna(subset=["Trade_Tweet_Dummy"]).copy()
        sub["CAR"] = car
        sub = sub.dropna(subset=["CAR"])

        ev = sub[sub["Trade_Tweet_Dummy"] == 1]["CAR"] * 100
        no = sub[sub["Trade_Tweet_Dummy"] == 0]["CAR"] * 100
        t_stat, p_val = stats.ttest_ind(ev, no, equal_var=False)

        sig = "Not Sig"
        if p_val < 0.05: sig = "** (p<0.05)"
        elif p_val < 0.10: sig = "* (p<0.10)"

        print(f"{asset:<8} 2-Day CAR: Event = {ev.mean():+.3f}%, None = {no.mean():+.3f}%, Diff = {ev.mean()-no.mean():+.3f}%p | t = {t_stat:+.3f}, p = {p_val:.4f} | {sig}")

    res_df.to_csv("extended_empirical_summary.csv", index=False)
    print("\nSummary saved to extended_empirical_summary.csv")

if __name__ == "__main__":
    run_extended_analysis()
