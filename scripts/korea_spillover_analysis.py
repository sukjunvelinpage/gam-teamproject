"""
[EXP-02] 한국 시장 전이 분석 (트럼프 1기, 병합 기준 Merged_* 이벤트일)

질문
    무역 갈등 트윗의 충격이 중국 노출 자산에 몰렸다면, 대중 수출·공급망 비중이 큰 한국 자산도 반응했는가?

대상 자산 (yfinance)
    KOSPI(^KS11), 삼성전자(005930.KS), SK하이닉스(000660.KS), 현대차(005380.KS), POSCO홀딩스(005490.KS)
    원/달러 환율(KRW=X, 상승 = 원화 약세), 한국 ETF(EWY, 미국 상장)

시차 정렬 (Look-ahead bias 방지)
    - 미국 거래일 T에 매핑된 트윗은 뉴욕 기준 [T-1 16:00, T 16:00]에 나온 것이다.
      한국 시각으로 [T 06:00, T+1 06:00] (서머타임이면 1시간 앞당김)이다.
    - 한국 장(09:00~15:30 KST)이 이 정보를 '모두' 반영하는 첫 거래일은 날짜가 T보다 뒤인 첫 KRX 개장일이다.
      → 한국 주식의 '당일(Day_T)' = T 이후 첫 KRX 개장일 K의 수익률 (AGENTS.md 시차 원칙, 백로그 EXP-02).
    - 한계: 전날 저녁(뉴욕) 트윗 일부는 한국 T일 장중에 이미 반영됐을 수 있다. 이를 놓치는 쪽(보수적)이며
      미래 정보를 쓰지는 않는다. 그래서 CAR[0,+1], CAR[0,+2]도 함께 본다.
    - 휴장 등으로 서로 다른 미국 거래일이 같은 K로 묶일 수 있다(그대로 둔다, 각 날의 값은 동일).
    - KRW=X와 EWY는 미국 거래일 기준으로 둔다(기존 CNY=X와 같은 방식). EWY는 시차 문제가 없는 교차 확인용이다.

검정 (reanalysis_merged_omissions.py와 같은 비교·윈도우, Welch's t-test)
    비교 5개 × 자산 7개 × 윈도우 4개. 비교 묶음별 28개에 BH 보정(q < 0.10).
    강건성(핵심 결과): 월 고정효과, 코로나 급락기(2020-02-20~06-30) 제외.

이벤트 스냅숏 (기술 통계, 검정 아님)
    한국과 직접 관련된 1기 무역 사건 3개의 한국 자산 누적 수익률을 S&P 500과 나란히 보여준다.

출력
    data/korea_market_data.csv                     : 한국 자산 종가 원자료 (재현용)
    docs/korea_spillover_2026-11-11/korea_full.csv : 전체 검정 결과
    docs/korea_spillover_2026-11-11/korea_robustness.csv
    docs/korea_spillover_2026-11-11/korea_events.csv
    presentation_charts/chart5_korea_spillover.png

실행
    python scripts/korea_spillover_analysis.py            # 저장된 원자료가 있으면 그대로 사용
    python scripts/korea_spillover_analysis.py --refresh  # yfinance에서 다시 받기
"""

import platform
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from reanalysis_merged_omissions import MARKET_PATH, bh, comparisons, welch

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "korea_market_data.csv"
OUT_DIR = ROOT / "docs" / "korea_spillover_2026-11-11"
CHART_PATH = ROOT / "presentation_charts" / "chart5_korea_spillover.png"

KRX_TICKERS = {"KOSPI": "^KS11", "SEC": "005930.KS", "HYNIX": "000660.KS",
               "HMC": "005380.KS", "POSCO": "005490.KS"}
US_TICKERS = {"KRW": "KRW=X", "EWY": "EWY"}
NAMES = {"KOSPI": "KOSPI", "SEC": "삼성전자", "HYNIX": "SK하이닉스", "HMC": "현대차",
         "POSCO": "POSCO홀딩스", "KRW": "원화 약세(USD/KRW)", "EWY": "한국 ETF(EWY)"}
ASSETS = list(KRX_TICKERS) + list(US_TICKERS)
WINDOWS = ["Day_T", "Day_T+1", "CAR[0,+1]", "CAR[0,+2]"]
COMPS = ["A_무역_통합_vs_무무역일", "A_무역_순수긍정_vs_무무역일", "A_무역_순수부정_vs_무무역일",
         "B_정책_순수긍정_vs_순수부정", "C_협상진전_vs_관세위협"]
COVID_START, COVID_END = "2020-02-20", "2020-06-30"

# 한국 관련 1기 무역 사건 (미국 거래일 기준 T). 트윗·발표 시각이 모두 뉴욕 장중 또는 장 마감 전후
EVENTS = [
    ("2018-03-01", "철강 25% 관세 발표 (232조)"),
    ("2018-03-28", "KORUS 원칙 합의 트윗 (철강 쿼터로 관세 면제)"),
    ("2019-05-06", "대중 관세 10→25% 인상 예고 트윗 (5/5 일요일)"),
]


def download(refresh: bool) -> pd.DataFrame:
    if RAW_PATH.exists() and not refresh:
        return pd.read_csv(RAW_PATH, parse_dates=["Date"])
    import yfinance as yf
    tickers = {**KRX_TICKERS, **US_TICKERS}
    raw = yf.download(list(tickers.values()), start="2016-12-01", end="2021-02-28",
                      auto_adjust=True, progress=False)["Close"]
    raw = raw.rename(columns={v: k for k, v in tickers.items()})[list(tickers)]
    raw.index.name = "Date"
    out = raw.reset_index()
    out.to_csv(RAW_PATH, index=False)
    return out


def krx_windows(price: pd.Series) -> dict:
    """KRX 달력 기준 수익률 윈도우 (기존 windows()와 같은 정의: CAR는 전체 평균을 뺀 값)."""
    p = price.dropna()
    r = p.pct_change()
    r1, r2 = r.shift(-1), r.shift(-2)
    c01 = (1 + r) * (1 + r1) - 1
    c02 = (1 + r) * (1 + r1) * (1 + r2) - 1
    return {"Day_T": r * 100, "Day_T+1": r1 * 100,
            "CAR[0,+1]": (c01 - c01.mean()) * 100, "CAR[0,+2]": (c02 - c02.mean()) * 100}


def us_windows(price: pd.Series, us_dates: pd.DatetimeIndex) -> dict:
    """미국 거래일로 맞춘 뒤 수익률 윈도우 (기존 CNY 처리와 같은 방식)."""
    p = price.reindex(us_dates).ffill()
    r = p.pct_change()
    r1, r2 = r.shift(-1), r.shift(-2)
    c01 = (1 + r) * (1 + r1) - 1
    c02 = (1 + r) * (1 + r1) * (1 + r2) - 1
    return {"Day_T": r * 100, "Day_T+1": r1 * 100,
            "CAR[0,+1]": (c01 - c01.mean()) * 100, "CAR[0,+2]": (c02 - c02.mean()) * 100}


def build_series(raw: pd.DataFrame, us_dates: pd.DatetimeIndex) -> dict:
    """자산 → 윈도우 → 미국 거래일 인덱스 Series (RangeIndex로 시장 데이터와 맞춤)."""
    px = raw.set_index("Date")
    out = {}
    for a in KRX_TICKERS:
        w = krx_windows(px[a])
        krx_days = w["Day_T"].index
        # T보다 날짜가 뒤인 첫 KRX 개장일
        pos = krx_days.searchsorted(us_dates, side="right")
        valid = pos < len(krx_days)
        k = pd.DatetimeIndex([krx_days[i] if v else pd.NaT for i, v in zip(pos, valid)])
        out[a] = {win: pd.Series(s.reindex(k).to_numpy(), index=range(len(us_dates))) for win, s in w.items()}
        out[a]["_K"] = k
    for a in US_TICKERS:
        w = us_windows(px[a], us_dates)
        out[a] = {win: pd.Series(s.to_numpy(), index=range(len(us_dates))) for win, s in w.items()}
    return out


def full_table(df: pd.DataFrame, series: dict) -> pd.DataFrame:
    comps = comparisons(df, "Merged_")
    rows = []
    for name in COMPS:
        ev, ct = comps[name]
        for a in ASSETS:
            for win in WINDOWS:
                diff, p, n1, n2 = welch(series[a][win], ev, ct)
                rows.append({"비교": name, "자산": a, "자산명": NAMES[a], "윈도우": win,
                             "차이": diff, "p": p, "N_이벤트": n1, "N_대조": n2})
    out = pd.DataFrame(rows)
    out["BH_통과"] = out.groupby("비교")["p"].transform(bh)
    return out


def robustness(df: pd.DataFrame, series: dict, full: pd.DataFrame) -> pd.DataFrame:
    """p < 0.10인 결과만 월 고정효과·코로나 제외로 다시 본다."""
    date = pd.to_datetime(df["Date"])
    month = date.dt.to_period("M")
    covid = (date >= COVID_START) & (date <= COVID_END)
    comps = comparisons(df, "Merged_")
    rows = []
    for _, r in full[full["p"] < 0.10].iterrows():
        ev, ct = comps[r["비교"]]
        s = series[r["자산"]][r["윈도우"]]
        fe = s - s.groupby(month.to_numpy()).transform("mean")
        d1, p1, _, _ = welch(fe, ev, ct)
        d2, p2, _, _ = welch(s, ev & ~covid, ct & ~covid)
        rows.append({**r[["비교", "자산", "자산명", "윈도우", "N_이벤트", "차이", "p", "BH_통과"]].to_dict(),
                     "월FE_차이": d1, "월FE_p": p1, "코로나제외_차이": d2, "코로나제외_p": p2})
    return pd.DataFrame(rows)


def event_snapshot(raw: pd.DataFrame, df: pd.DataFrame, us_dates: pd.DatetimeIndex) -> pd.DataFrame:
    """사건별 3거래일 누적 수익률 (한국 주식은 T 이후 첫 KRX 개장일부터)."""
    px = raw.set_index("Date")
    sp = df.set_index(pd.to_datetime(df["Date"]))["SP500_Return"]
    rows = []
    for d, label in EVENTS:
        t = pd.Timestamp(d)
        row = {"미국거래일_T": d, "사건": label}
        i = sp.index.get_loc(t)
        row["S&P500_CAR3(%)"] = ((1 + sp.iloc[i:i + 3]).prod() - 1) * 100
        for a in KRX_TICKERS:
            p = px[a].dropna()
            j = p.index.searchsorted(t, side="right")
            row[f"{NAMES[a]}_CAR3(%)"] = (p.iloc[j + 2] / p.iloc[j - 1] - 1) * 100
            if a == "KOSPI":
                row["한국_첫반응일_K"] = p.index[j].date().isoformat()
        for a in US_TICKERS:
            p = px[a].reindex(us_dates).ffill()
            k = p.index.get_loc(t)
            row[f"{NAMES[a]}_CAR3(%)"] = (p.iloc[k + 2] / p.iloc[k - 1] - 1) * 100
        rows.append(row)
    return pd.DataFrame(rows)


def stars(p: float) -> str:
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""


def chart(full: pd.DataFrame, events: pd.DataFrame) -> None:
    plt.rcParams["font.family"] = "Malgun Gothic" if platform.system() == "Windows" else "AppleGothic"
    plt.rcParams["axes.unicode_minus"] = False
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(14, 5.8), gridspec_kw={"width_ratios": [1, 1.25]})

    # 왼쪽: 일별 평균 반응 (부정 트윗일 vs 무역 트윗 없는 날)
    order = ["KOSPI", "SEC", "HYNIX", "HMC", "POSCO", "EWY", "KRW"]
    sub = full[(full["비교"] == "A_무역_순수부정_vs_무무역일") & (full["윈도우"] == "Day_T")].set_index("자산").loc[order]
    colors = ["#b3261e" if (v < 0 and p < 0.1) else "#1f5fa8" if (v > 0 and p < 0.1) else "#a8a8a8"
              for v, p in zip(sub["차이"], sub["p"])]
    y = np.arange(len(order))
    ax.barh(y, sub["차이"], color=colors)
    ax.axvline(0, color="#333", lw=0.8)
    for yi, (v, p) in enumerate(zip(sub["차이"], sub["p"])):
        ax.text(v + (0.01 if v >= 0 else -0.01), yi, f"{v:+.2f}%p {stars(p)} (p={p:.3f})",
                va="center", ha="left" if v >= 0 else "right", fontsize=9)
    ax.set_xlim(-0.75, 0.5)
    ax.set_yticks(y, [NAMES[a] for a in order])
    ax.invert_yaxis()
    ax.set_title("① 일별 평균: 무역 갈등 트윗일(123일) vs 무역 트윗 없는 날(656일)\n"
                 "한국 주식은 T 이후 첫 개장일, EWY·환율은 미국 T일", fontsize=10.5)
    ax.set_xlabel("평균 수익률 차이 (%p)  ·  빨강 = p<0.1 하락, 회색 = 비유의")
    ax.grid(axis="x", alpha=0.3)

    # 오른쪽: 한국 관련 큰 사건 3개, 3거래일 누적 수익률
    cols = ["S&P500_CAR3(%)", "KOSPI_CAR3(%)", "삼성전자_CAR3(%)", "현대차_CAR3(%)", "POSCO홀딩스_CAR3(%)"]
    labels = ["S&P 500", "KOSPI", "삼성전자", "현대차", "POSCO홀딩스"]
    palette = ["#555555", "#1f5fa8", "#6c9bd2", "#e08a2c", "#8c5a3c"]
    x = np.arange(len(events))
    w = 0.16
    for i, (c, lab, col) in enumerate(zip(cols, labels, palette)):
        vals = events[c].to_numpy()
        bars = ax2.bar(x + (i - 2) * w, vals, w, label=lab, color=col)
        for b, v in zip(bars, vals):
            ax2.text(b.get_x() + b.get_width() / 2, v + (0.15 if v >= 0 else -0.15), f"{v:+.1f}",
                     ha="center", va="bottom" if v >= 0 else "top", fontsize=8)
    ax2.axhline(0, color="#333", lw=0.8)
    ax2.set_xticks(x, [f"{d}\n{s}" for d, s in zip(events["미국거래일_T"], events["사건"].str.replace(" (", "\n(", regex=False))],
                   fontsize=8.5)
    ax2.set_ylabel("3거래일 누적 수익률 (%)")
    ax2.set_ylim(min(-7.5, events[cols].min().min() - 1), max(3, events[cols].max().max() + 1))
    ax2.set_title("② 큰 사건 스냅숏 (기술 통계, 검정 아님)\n한국은 T 이후 첫 개장일부터 3거래일", fontsize=10.5)
    ax2.legend(fontsize=8.5, ncol=5, loc="lower center", bbox_to_anchor=(0.5, -0.36), frameon=False)
    ax2.grid(axis="y", alpha=0.3)

    fig.suptitle("한국 시장은 '트윗 하루하루'엔 조용했고, 큰 관세 사건엔 미국보다 크게 흔들렸다 (트럼프 1기)",
                 fontsize=13, fontweight="bold")
    fig.text(0.5, 0.005, "Welch t-test, 병합 기준 이벤트일 · p<0.1 *, <0.05 **, <0.01 *** · 원/달러 상승 = 원화 약세 · "
             "BH 보정(28개 묶음) 통과 결과 없음", ha="center", fontsize=8.5, color="#555")
    fig.tight_layout(rect=[0, 0.03, 1, 0.94])
    CHART_PATH.parent.mkdir(exist_ok=True)
    fig.savefig(CHART_PATH, dpi=300)
    plt.close(fig)


def main():
    raw = download("--refresh" in sys.argv)
    df = pd.read_csv(MARKET_PATH)
    assert len(df) == 1007
    us_dates = pd.DatetimeIndex(pd.to_datetime(df["Date"]))
    series = build_series(raw, us_dates)

    full = full_table(df, series)
    rob = robustness(df, series, full)
    events = event_snapshot(raw, df, us_dates)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    full.to_csv(OUT_DIR / "korea_full.csv", index=False, encoding="utf-8-sig")
    rob.to_csv(OUT_DIR / "korea_robustness.csv", index=False, encoding="utf-8-sig")
    events.to_csv(OUT_DIR / "korea_events.csv", index=False, encoding="utf-8-sig")
    chart(full, events)

    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    print("== 결측 확인: 한국 주식 매핑이 비는 미국 거래일 수 ==")
    print({a: int(series[a]["Day_T"].isna().sum()) for a in ASSETS})
    print("\n== p < 0.10 결과 + 강건성 ==")
    print(rob.round(3).to_string(index=False))
    print("\n== 이벤트 스냅숏 ==")
    print(events.round(2).T.to_string())


if __name__ == "__main__":
    main()
