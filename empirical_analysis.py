"""
Empirical Statistical Analysis: Trump 1st Term Tweets vs Financial Markets
---------------------------------------------------------------------------
Analyzes the impact of Trade/Tariff and Fed tweets on:
1. S&P 500 Daily Return
2. VIX Volatility (Level & Daily Change)
3. US Dollar Index (DXY) Return
"""

import os
import pandas as pd
import numpy as np
from scipy import stats

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trump_market_event_data.csv")

def run_analysis():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Run pipeline.py first.")

    df = pd.read_csv(DATA_PATH)
    print("=" * 75)
    print("EMPIRICAL TEST: TRUMP TWEETS VS FINANCIAL MARKET METRICS (2017-2021)")
    print(f"Total Trading Sessions: {len(df):,} days")
    print("=" * 75)

    def test_impact(metric_name: str, dummy_col: str, label: str):
        g_event = df[df[dummy_col] == 1][metric_name].dropna()
        g_none = df[df[dummy_col] == 0][metric_name].dropna()

        t_stat, p_val = stats.ttest_ind(g_event, g_none, equal_var=False)
        mean_event = g_event.mean() * 100
        mean_none = g_none.mean() * 100
        diff = mean_event - mean_none

        print(f"\n[{label}] Metric: {metric_name}")
        print(f"  * Event Days (N={len(g_event)}): Mean = {mean_event:+.3f}%, Std = {g_event.std()*100:.3f}%")
        print(f"  * Other Days (N={len(g_none)}): Mean = {mean_none:+.3f}%, Std = {g_none.std()*100:.3f}%")
        print(f"  * Difference: {diff:+.3f}%p | t-stat: {t_stat:+.3f} | p-value: {p_val:.4f}")
        
        signif = ""
        if p_val < 0.01:
            signif = " *** (p < 0.01: Highly Significant)"
        elif p_val < 0.05:
            signif = " ** (p < 0.05: Significant)"
        elif p_val < 0.10:
            signif = " * (p < 0.10: Marginally Significant)"
        else:
            signif = " (Not Statistically Significant at 10%)"
        print(f"  * Result:{signif}")

    print("\n--- [1] TRADE & TARIFF TWEET IMPACT ---")
    test_impact("SP500_Return", "Trade_Tweet_Dummy", "S&P 500 Daily Return")
    test_impact("VIX_Return", "Trade_Tweet_Dummy", "VIX Daily Change (%)")
    test_impact("VIX_Close", "Trade_Tweet_Dummy", "VIX Closing Level")
    test_impact("DXY_Return", "Trade_Tweet_Dummy", "Dollar Index (DXY) Return")

    print("\n--- [2] FED & MONETARY POLICY TWEET IMPACT ---")
    test_impact("SP500_Return", "Fed_Tweet_Dummy", "S&P 500 Daily Return")
    test_impact("VIX_Return", "Fed_Tweet_Dummy", "VIX Daily Change (%)")
    test_impact("VIX_Close", "Fed_Tweet_Dummy", "VIX Closing Level")
    test_impact("DXY_Return", "Fed_Tweet_Dummy", "Dollar Index (DXY) Return")
    print("=" * 75)

if __name__ == "__main__":
    run_analysis()
