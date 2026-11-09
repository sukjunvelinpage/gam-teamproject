"""
발표용 차트 4종 생성 스크립트.

- 입력: data/trump_market_analysis_input.csv (1,007거래일)
- 분류 기준: 기존 1,246건 + 누락 후보 138건을 합친 병합 변수(Merged_*). 먼저 scripts/build_merged_market_variables.py 실행
- 출력: presentation_charts/chart1~4 PNG (300 DPI)
- 모든 수치와 표본 수는 실행 시 데이터에서 계산한다. 차트 안에 값을 직접 적지 않는다.
- 검정: Welch's t-test, 유의수준 표기 p<0.1(*), p<0.05(**), p<0.01(***)
- 수익률 윈도우 정의는 scripts/empirical_context_sentiment.py와 동일하다.
"""

import os
import platform
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

plt.rcParams["font.family"] = "Malgun Gothic" if platform.system() == "Windows" else "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "trump_market_analysis_input.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "presentation_charts")

# 색상은 항목을 따라간다. 같은 항목은 모든 차트에서 같은 색이다.
COLOR_LUMP = "#52514e"  # 통합: 중립 회색
COLOR_POS = "#2a78d6"  # 순수 긍정
COLOR_NEG = "#eb6834"  # 순수 부정
COLOR_NOISE = "#1baf7a"  # 소음만
COLOR_INK = "#0b0b0b"
COLOR_SUB = "#52514e"
COLOR_MUTED = "#898781"
COLOR_GRID = "#e1e0d9"
COLOR_BASE = "#c3c2b7"
COLOR_SURFACE = "#fcfcfb"

BASIS_TRADE = "대조군: 무역 트윗이 없는 날 | Welch's t-test | 가는 선: 95% 신뢰구간 | *p<0.1, **p<0.05, ***p<0.01"
PREFIX = "Merged_"  # 기존 1,246건만 쓰려면 ""로 바꾼다
EXPLORATORY = "검정 64개 BH 보정(q<0.10) 시 통과는 VIX 통합 등 일부뿐이어서 탐색적 결과로 해석"


def windows(returns: pd.Series) -> dict:
    """일별 수익률을 당일과 누적 초과수익률(%)로 변환한다."""
    next_1 = returns.shift(-1)
    cum_01 = (1 + returns) * (1 + next_1) - 1
    return {"당일": returns * 100, "CAR[0,+1]": (cum_01 - cum_01.mean()) * 100}


def stars(p_value: float) -> str:
    if p_value < 0.01:
        return "***"
    if p_value < 0.05:
        return "**"
    if p_value < 0.10:
        return "*"
    return ""


def welch(series: pd.Series, event: pd.Series, control: pd.Series) -> dict:
    """이벤트일 평균 - 대조일 평균의 차이, p값, 95% 신뢰구간을 계산한다."""
    x, y = series[event].dropna(), series[control].dropna()
    p_value = stats.ttest_ind(x, y, equal_var=False).pvalue
    var_x, var_y = x.var(ddof=1) / len(x), y.var(ddof=1) / len(y)
    se = np.sqrt(var_x + var_y)
    dof = (var_x + var_y) ** 2 / (var_x**2 / (len(x) - 1) + var_y**2 / (len(y) - 1))
    half = stats.t.ppf(0.975, dof) * se
    diff = x.mean() - y.mean()
    return {"diff": diff, "p": p_value, "low": diff - half, "high": diff + half, "n": len(x), "n_ctrl": len(y)}


def build_masks(df: pd.DataFrame) -> dict:
    """무역 트윗일(1,246건 + 누락 후보 138건 병합 기준)을 톤별로 나눈다."""
    trade = df[f"{PREFIX}Trade_Tweet_Dummy"] == 1
    has_pos, has_neg = df[f"{PREFIX}Trade_Pos_Count"] > 0, df[f"{PREFIX}Trade_Neg_Count"] > 0
    return {
        "trade": trade,
        "ctrl": ~trade,
        "pos": trade & has_pos & ~has_neg,
        "neg": trade & has_neg & ~has_pos,
        "noise": trade & ~has_pos & ~has_neg,
        "fed": df["Fed_Tweet_Dummy"] == 1,
        "fed_neg": df[f"{PREFIX}Fed_Neg_Dummy"] == 1,
    }


def style_axis(ax, axis: str = "y") -> None:
    """격자와 축은 실선 헤어라인으로 흐리게 둔다."""
    ax.set_facecolor(COLOR_SURFACE)
    for side in ["top", "right", "left", "bottom"]:
        ax.spines[side].set_visible(False)
    ax.grid(axis=axis, color=COLOR_GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, colors=COLOR_SUB, labelsize=11)


def value_label(result: dict) -> str:
    return f"{result['diff']:+.3f} {stars(result['p'])}\np={result['p']:.3f}".replace(" \n", "\n")


def draw_columns(ax, results: list, labels: list, colors: list, title: str) -> None:
    """세로 막대에 95% 신뢰구간과 값, p값을 표시한다."""
    x_pos = np.arange(len(results))
    ax.bar(x_pos, [r["diff"] for r in results], width=0.5, color=colors, zorder=2)
    span = max(r["high"] for r in results + [{"high": 0}]) - min(r["low"] for r in results + [{"low": 0}])
    for i, r in enumerate(results):
        ax.plot([i, i], [r["low"], r["high"]], color=COLOR_INK, linewidth=1, zorder=3)
        # 격자선이 글자를 가르지 않도록 라벨 뒤에 배경색을 깐다
        backing = dict(facecolor=COLOR_SURFACE, edgecolor="none", pad=1.5)
        if r["diff"] >= 0:
            ax.text(i, r["high"] + span * 0.02, value_label(r), ha="center", va="bottom", fontsize=10.5,
                    color=COLOR_INK, bbox=backing, zorder=4)
        else:
            ax.text(i, r["low"] - span * 0.02, value_label(r), ha="center", va="top", fontsize=10.5,
                    color=COLOR_INK, bbox=backing, zorder=4)
    ax.axhline(0, color=COLOR_BASE, linewidth=1.2, zorder=1)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_title(title, fontsize=13, fontweight="bold", color=COLOR_INK, loc="left", pad=10)
    ax.set_ylabel("대조군 대비 차이 (%p)", fontsize=11, color=COLOR_SUB)
    low = min(r["low"] for r in results + [{"low": 0}])
    high = max(r["high"] for r in results + [{"high": 0}])
    ax.set_ylim(low - span * 0.24, high + span * 0.24)
    style_axis(ax)


def finish(fig, title: str, subtitle: str, footer: str, filename: str) -> None:
    """제목과 주석을 붙여 300 DPI PNG로 저장한다."""
    fig.patch.set_facecolor(COLOR_SURFACE)
    fig.text(0.015, 0.975, title, fontsize=17, fontweight="bold", color=COLOR_INK, va="top")
    fig.text(0.015, 0.915, subtitle, fontsize=12, color=COLOR_SUB, va="top")
    fig.text(0.015, 0.018, footer, fontsize=9.5, color=COLOR_MUTED, va="bottom")
    fig.tight_layout(rect=(0.005, 0.06, 0.995, 0.87))
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=300, facecolor=COLOR_SURFACE)
    plt.close(fig)
    print(f"저장: {path}")


def report(chart: str, name: str, r: dict) -> None:
    """차트의 표 보기 역할을 하도록 값을 터미널에 출력한다."""
    print(f"{chart} | {name:28s} | {r['diff']:+.3f}%p {stars(r['p']):3s} p={r['p']:.3f} "
          f"CI[{r['low']:+.3f}, {r['high']:+.3f}] n={r['n']}/{r['n_ctrl']}")


def tone_labels(m: dict) -> list:
    return [f"통합\n({m['trade'].sum()}일)", f"순수 긍정\n({m['pos'].sum()}일)",
            f"순수 부정\n({m['neg'].sum()}일)", f"소음만\n({m['noise'].sum()}일)"]


def chart1_core_puzzle(df: pd.DataFrame, m: dict) -> None:
    """S&P 500과 VIX를 통합 및 톤별로 비교한다."""
    panels = [("SP500", "당일", "S&P 500 당일 수익률"),
              ("SP500", "CAR[0,+1]", "S&P 500 CAR[0,+1]"),
              ("VIX", "당일", "VIX 당일 변화율")]
    fig, axes = plt.subplots(1, 3, figsize=(15, 6.2))
    for ax, (ticker, window, title) in zip(axes, panels):
        series = windows(df[f"{ticker}_Return"])[window]
        results = [welch(series, m[k], m["ctrl"]) for k in ["trade", "pos", "neg", "noise"]]
        draw_columns(ax, results, tone_labels(m), [COLOR_LUMP, COLOR_POS, COLOR_NEG, COLOR_NOISE], title)
        for key, r in zip(["통합", "긍정", "부정", "소음"], results):
            report("chart1", f"{title} {key}", r)
    finish(fig, "지수는 무덤덤했고, VIX 상승은 톤으로 설명되지 않는다",
           "VIX는 부정 트윗일과 시장 무관 소음일에 거의 같은 폭으로 상승",
           f"{BASIS_TRADE}\n패널마다 세로축 범위가 다름 | {EXPLORATORY}", "chart1_core_puzzle.png")


def chart2_industry_asymmetry(df: pd.DataFrame, m: dict) -> None:
    """기업·섹터의 당일 반응을 통합과 순수 부정으로 비교한다."""
    assets = [("BA", "보잉"), ("SOXX", "반도체 ETF"), ("AAPL", "애플"), ("CAT", "캐터필러"),
              ("XLI", "산업재 ETF"), ("NUE", "Nucor 철강"), ("SLX", "철강 ETF")]
    fig, ax = plt.subplots(figsize=(13, 7.4))
    y_pos = np.arange(len(assets))
    height = 0.34
    all_results = []
    for i, (ticker, name) in enumerate(assets):
        series = windows(df[f"{ticker}_Return"])["당일"]
        lump = welch(series, m["trade"], m["ctrl"])
        neg = welch(series, m["neg"], m["ctrl"])
        report("chart2", f"{name} 통합", lump)
        report("chart2", f"{name} 부정", neg)
        for r, offset, color in [(lump, -height / 2 - 0.01, COLOR_LUMP), (neg, height / 2 + 0.01, COLOR_NEG)]:
            y = i + offset
            ax.barh(y, r["diff"], height=height, color=color, zorder=2)
            ax.plot([r["low"], r["high"]], [y, y], color=COLOR_INK, linewidth=1, zorder=3)
            sign = stars(r["p"])
            text = f"{r['diff']:+.3f}{' ' + sign if sign else ''} (p={r['p']:.3f})"
            ax.text(r["low"] - 0.02, y, text, ha="right", va="center", fontsize=10.5, color=COLOR_INK,
                    bbox=dict(facecolor=COLOR_SURFACE, edgecolor="none", pad=1.5), zorder=4)
            all_results.append(r)
    ax.axvline(0, color=COLOR_BASE, linewidth=1.2, zorder=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([name for _, name in assets], fontsize=12, color=COLOR_INK)
    ax.invert_yaxis()
    ax.set_xlabel("대조군 대비 당일 수익률 차이 (%p)", fontsize=11, color=COLOR_SUB)
    ax.set_xlim(min(r["low"] for r in all_results) - 0.36, max(r["high"] for r in all_results) + 0.05)
    style_axis(ax, axis="x")
    ax.barh([np.nan], [np.nan], color=COLOR_LUMP, label=f"통합 ({m['trade'].sum()}일)")
    ax.barh([np.nan], [np.nan], color=COLOR_NEG, label=f"순수 부정 ({m['neg'].sum()}일)")
    ax.legend(loc="upper right", frameon=False, fontsize=11, ncol=2, bbox_to_anchor=(1.0, 1.07))
    finish(fig, "통합 분석에 가려졌던 부정 트윗일의 당일 약세",
           "보잉·반도체·애플이 p<0.05로 약세. 관세 수혜주로 예상한 철강도 오르지 않고 약세 경향",
           f"{BASIS_TRADE}\n{EXPLORATORY}", "chart2_industry_asymmetry.png")


def chart3_fed_bonds(df: pd.DataFrame, m: dict) -> None:
    """금리 변화율 반응을 연준 트윗과 무역 트윗으로 비교한다."""
    series = windows(df["TNX_Return"])["당일"]
    results = [welch(series, m["fed"], ~m["fed"]), welch(series, m["fed_neg"], ~m["fed_neg"]),
               welch(series, m["pos"], m["ctrl"]), welch(series, m["neg"], m["ctrl"])]
    names = ["연준 트윗일", "연준 공격 트윗일", "무역 순수 긍정", "무역 순수 부정"]
    labels = [f"{name}\n({r['n']}일)" for name, r in zip(names, results)]
    for name, r in zip(names, results):
        report("chart3", name, r)
    fig, ax = plt.subplots(figsize=(11, 6.4))
    draw_columns(ax, results, labels, [COLOR_LUMP, COLOR_LUMP, COLOR_POS, COLOR_NEG], "미국 10년물 금리 당일 변화율")
    finish(fig, "금리 하락은 연준 트윗일이 아니라 무역 부정 트윗일에 관측됐다",
           "연준 트윗일은 신뢰구간이 넓어 효과를 확인하지 못했고, 무역 순수 부정일에만 유의한 하락",
           "대조군: 연준 항목은 해당 트윗이 없는 날, 무역 항목은 무역 트윗이 없는 날 | Welch's t-test | "
           f"가는 선: 95% 신뢰구간\n금리 수준(%)의 일별 변화율 기준이며 bp 변화가 아님 | {EXPLORATORY}",
           "chart3_fed_bonds.png")


def chart4_international_spillover(df: pd.DataFrame, m: dict) -> None:
    """위안화, 중국 주식, 금의 반응을 톤별로 비교한다."""
    panels = [("CNY", "CAR[0,+1]", "USD/CNY CAR[0,+1]"),
              ("FXI", "CAR[0,+1]", "중국 대형주(FXI) CAR[0,+1]"),
              ("GLD", "당일", "금(GLD) 당일")]
    labels = tone_labels(m)[:3]
    fig, axes = plt.subplots(1, 3, figsize=(15, 6.2))
    for ax, (ticker, window, title) in zip(axes, panels):
        series = windows(df[f"{ticker}_Return"])[window]
        results = [welch(series, m[k], m["ctrl"]) for k in ["trade", "pos", "neg"]]
        draw_columns(ax, results, labels, [COLOR_LUMP, COLOR_POS, COLOR_NEG], title)
        for key, r in zip(["통합", "긍정", "부정"], results):
            report("chart4", f"{title} {key}", r)
    finish(fig, "위안화는 부정 트윗일에 약세, 중국 주식의 긍정일 강세는 약하다",
           "USD/CNY 상승은 위안화 약세를 뜻함. FXI 긍정일 반응은 p<0.1 수준이며, 금은 톤별 차이가 뚜렷하지 않음",
           f"{BASIS_TRADE}\n패널마다 세로축 범위가 다름 | {EXPLORATORY}", "chart4_international_spillover.png")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")  # 파이프 출력에서도 한글이 깨지지 않게 한다
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.read_csv(DATA_PATH)
    masks = build_masks(df)
    chart1_core_puzzle(df, masks)
    chart2_industry_asymmetry(df, masks)
    chart3_fed_bonds(df, masks)
    chart4_international_spillover(df, masks)


if __name__ == "__main__":
    main()
