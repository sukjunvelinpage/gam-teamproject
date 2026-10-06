"""
Generates clean, high-resolution visualization charts for 15-minute GAM presentation.
Pure matplotlib (no seaborn dependency) with polished financial aesthetics.
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial"]
plt.rcParams["axes.unicode_minus"] = False

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trump_market_extended_data.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presentation_charts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
ev_mask = df["Trade_Tweet_Dummy"] == 1
no_mask = df["Trade_Tweet_Dummy"] == 0
fed_ev = df["Fed_Tweet_Dummy"] == 1
fed_no = df["Fed_Tweet_Dummy"] == 0

# -----------------------------------------------------------------------------
# Chart 1: The Core Puzzle (S&P 500 Return vs VIX Volatility)
# -----------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5), dpi=300)

# S&P 500
sp_ev = df.loc[ev_mask, "SP500_Return"].mean() * 100
sp_no = df.loc[no_mask, "SP500_Return"].mean() * 100
bars1 = ax1.bar(["Trade Tweet Day\n(N=337)", "Other Days\n(N=707)"], [sp_ev, sp_no], color=["#e74c3c", "#3498db"], width=0.55)
ax1.set_title("S&P 500 Daily Return\n(Market Direction: No Impact)", fontsize=12, fontweight="bold", pad=12)
ax1.set_ylabel("Daily Return (%)", fontsize=11)
ax1.axhline(0, color="gray", linestyle="--", linewidth=0.8)
ax1.set_ylim(-0.02, 0.12)
for b in bars1:
    h = b.get_height()
    ax1.text(b.get_x() + b.get_width()/2, h + 0.005, f"{h:+.3f}%", ha="center", fontweight="bold", fontsize=11)
ax1.text(0.5, 0.02, "Diff: -0.070%p (p = 0.458)\n→ Statistically Insignificant", ha="center",
         bbox=dict(boxstyle="round,pad=0.4", facecolor="#f8f9fa", edgecolor="#ced4da"), fontsize=10)

# VIX
vix_ev = df.loc[ev_mask, "VIX_Return"].mean() * 100
vix_no = df.loc[no_mask, "VIX_Return"].mean() * 100
bars2 = ax2.bar(["Trade Tweet Day\n(N=337)", "Other Days\n(N=707)"], [vix_ev, vix_no], color=["#e74c3c", "#3498db"], width=0.55)
ax2.set_title("VIX Daily Change\n(Market Fear: Huge Impact!)", fontsize=12, fontweight="bold", pad=12, color="#c0392b")
ax2.set_ylabel("Daily Change (%)", fontsize=11)
ax2.axhline(0, color="gray", linestyle="--", linewidth=0.8)
ax2.set_ylim(-0.3, 1.8)
for b in bars2:
    h = b.get_height()
    ax2.text(b.get_x() + b.get_width()/2, h + 0.05, f"{h:+.2f}%", ha="center", fontweight="bold", fontsize=11)
ax2.text(0.5, 0.7, "★ Diff: +1.33%p (p = 0.028)\n→ Statistically Significant!", ha="center",
         color="#c0392b", fontweight="bold",
         bbox=dict(boxstyle="round,pad=0.4", facecolor="#fdf2e9", edgecolor="#e67e22"), fontsize=10)

plt.suptitle("The Core Puzzle: Trump Tweets Spiked Fear, Not the Macro Index", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "chart1_core_puzzle.png"), bbox_inches="tight")
plt.close()

# -----------------------------------------------------------------------------
# Chart 2: US Industry & Firm Asymmetry (The Offsetting Mechanism)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

assets = [
    "Boeing (BA)\n[Target & Retaliation]",
    "Semis (SOXX)\n[Tech War Victim]",
    "Caterpillar (CAT)\n[Export Machinery]",
    "Industrials (XLI)\n[Tariff Impact]",
    "Apple (AAPL)\n[Supply Chain]",
    "S&P 500\n[Macro Benchmark]"
]
cols = ["BA_Return", "SOXX_Return", "CAT_Return", "XLI_Return", "AAPL_Return", "SP500_Return"]

deltas = [(df.loc[ev_mask, c].mean() - df.loc[no_mask, c].mean()) * 100 for c in cols]
y_pos = np.arange(len(assets))
colors = ["#c0392b", "#d35400", "#e67e22", "#f39c12", "#f1c40f", "#7f8c8d"]

bars = ax.barh(y_pos, deltas, color=colors, height=0.55)
ax.set_yticks(y_pos)
ax.set_yticklabels(assets, fontsize=10, fontweight="bold")
ax.invert_yaxis()
ax.axvline(0, color="black", linewidth=1)
ax.set_xlabel("Relative Performance on Trade Tweet Days (Δ %p vs Other Days)", fontsize=11, fontweight="bold")
ax.set_title("Where Did the Impact Go? High-Exposure US Sectors & Firms Lagged", fontsize=13, fontweight="bold", pad=15)

for b in bars:
    w = b.get_width()
    ax.text(w - 0.005, b.get_y() + b.get_height()/2, f"{w:+.3f}%p",
            ha="right", va="center", fontsize=10, fontweight="bold", color="black")

ax.set_xlim(-0.25, 0.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "chart2_industry_asymmetry.png"), bbox_inches="tight")
plt.close()

# -----------------------------------------------------------------------------
# Chart 3: Fed Tweets vs 10Y Yield & Bonds
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)

fed_assets = ["10Y Yield Change (TNX)", "Financials ETF (XLF)", "S&P 500 (Fed Tweet Days)"]
fed_cols = ["TNX_Return", "XLF_Return", "SP500_Return"]

fed_deltas = [(df.loc[fed_ev, c].mean() - df.loc[fed_no, c].mean()) * 100 for c in fed_cols]
x_pos = np.arange(len(fed_assets))
bars_fed = ax.bar(x_pos, fed_deltas, color=["#2980b9", "#8e44ad", "#95a5a6"], width=0.45)
ax.axhline(0, color="gray", linestyle="--")
ax.set_xticks(x_pos)
ax.set_xticklabels(fed_assets, fontsize=11, fontweight="bold")
ax.set_ylabel("Yield / Return Difference (Δ %p)", fontsize=11, fontweight="bold")
ax.set_title("Fed & Interest Rates: 10Y Yield Compressed under Tweet Pressure", fontsize=13, fontweight="bold", pad=15)

for b in bars_fed:
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2, h - 0.02 if h < 0 else h + 0.01, f"{h:+.3f}%p",
            ha="center", va="top" if h < 0 else "bottom", fontsize=11, fontweight="bold")

ax.set_ylim(-0.28, 0.05)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "chart3_fed_bonds.png"), bbox_inches="tight")
plt.close()

# -----------------------------------------------------------------------------
# Chart 4: China Spillover & Gold Safe Haven
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)

intl_assets = ["Gold ETF (GLD)\n[Safe Haven Inflow]", "USD/CNY Rate\n[Yuan Depreciation]", "S&P 500\n[US Macro Index]"]
intl_deltas = [
    (df.loc[ev_mask, "GLD_Return"].mean() - df.loc[no_mask, "GLD_Return"].mean()) * 100,
    (df.loc[ev_mask, "CNY_Return"].mean() - df.loc[no_mask, "CNY_Return"].mean()) * 100,
    (df.loc[ev_mask, "SP500_Return"].mean() - df.loc[no_mask, "SP500_Return"].mean()) * 100,
]

x_pos = np.arange(len(intl_assets))
colors_intl = ["#f39c12", "#e67e22", "#7f8c8d"]
bars_intl = ax.bar(x_pos, intl_deltas, color=colors_intl, width=0.45)
ax.axhline(0, color="gray", linestyle="--")
ax.set_xticks(x_pos)
ax.set_xticklabels(intl_assets, fontsize=11, fontweight="bold")
ax.set_ylabel("Difference vs Other Days (Δ %p)", fontsize=11, fontweight="bold")
ax.set_title("International Spillover: Safe Haven Inflow & Currency Stress", fontsize=13, fontweight="bold", pad=15)

for b in bars_intl:
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2, h + 0.008 if h >= 0 else h - 0.015, f"{h:+.3f}%p",
            ha="center", va="bottom" if h >= 0 else "top", fontsize=11, fontweight="bold")

ax.set_ylim(-0.11, 0.12)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "chart4_international_spillover.png"), bbox_inches="tight")
plt.close()

print("All 4 GAM presentation charts generated successfully in presentation_charts/!")
