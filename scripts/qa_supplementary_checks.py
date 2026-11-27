"""
Q&A 대비 보완 분석 (2026-11-27)

예상 질문 중 기존 분석으로 답하기 어려운 항목을 같은 데이터(병합 기준 Merged_*)로 점검한다.
본 분석(Welch t-test, 순수 부정일 123일 vs 무역 트윗 없는 날 656일)의 수치는 바꾸지 않고,
"다른 방식으로 봐도 같은 결론이 나오는가"만 확인한다.

    1. 시장 모형(베타) 조정 초과수익률      → 교수님 질문 P5
       - (a) 대조일(무역 트윗 없는 날)로 추정한 고정 베타
       - (b) 직전 250거래일 롤링 베타 (당일 이전 정보만 사용)
    2. 시차 더미 회귀 + Newey-West 표준오차 → P6, P7
       r_t = a + Σ_k [b_k·Neg(t−k) + 긍정·소음·혼재 더미(t−k)] + e,  k = −1(선행), 0, 1, 2
       - k = −1은 "트윗 전날 이미 움직였나"(사전 움직임) 점검
       - b0+b1, b0+b1+b2는 CAR[0,+1], CAR[0,+2]에 해당하며, 겹치는 윈도우 문제를
         HAC(이분산·자기상관 강건) 표준오차로 처리한다.
    3. 10년물 금리를 bp 변화로 다시 검정     → P10
    4. 원형 이동(circular shift) 위약 검정    → P9
       이벤트 날짜 배열 전체를 k일씩 밀어 군집 구조(트윗이 몰린 모양)를 그대로 유지한 채 1,000회
    5. 이벤트 군집·트윗 시각 분포            → P7, S5

결측 처리: 수익률 결측은 시차 변수 생성 때 생기는 표본 양끝 몇 거래일뿐이며, 원본 데이터는 수정하지 않는다.
난수 시드: 42

실행
    python scripts/qa_supplementary_checks.py
출력
    docs/qa_2026-11-27/qa_supplementary_checks.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
MARKET_PATH = ROOT / "data" / "trump_market_analysis_input.csv"
TWEET_PATH = ROOT / "data" / "trump_tweets_analysis_input.csv"
OMISSION_PATH = ROOT / "data" / "trump_omission_candidates_138_classified.csv"
OUT_DIR = ROOT / "docs" / "qa_2026-11-27"

SEED = 42
N_PLACEBO = 1000
NW_LAGS = 5


# ---------------------------------------------------------------------------
# 공통
# ---------------------------------------------------------------------------
def load_market() -> pd.DataFrame:
    df = pd.read_csv(MARKET_PATH, parse_dates=["Date"]).sort_values("Date").reset_index(drop=True).copy()
    trade = df["Merged_Trade_Tweet_Dummy"] == 1
    pos, neg = df["Merged_Trade_Pos_Count"] > 0, df["Merged_Trade_Neg_Count"] > 0
    df["G_neg"] = (trade & neg & ~pos).astype(int)      # 순수 부정일 (본 분석과 같은 정의)
    df["G_pos"] = (trade & pos & ~neg).astype(int)      # 순수 긍정일
    df["G_noise"] = (trade & ~pos & ~neg).astype(int)   # 소음만 있던 날
    df["G_mix"] = (trade & pos & neg).astype(int)       # 혼재일
    df["G_ctrl"] = (~trade).astype(int)                 # 무역 트윗 없는 날 (대조군)
    df["TNX_bp"] = df["TNX_Close"].diff() * 100         # 10년물 금리 하루 변화 (bp)
    return df


def welch(x: pd.Series, y: pd.Series):
    x, y = x.dropna(), y.dropna()
    return x.mean() - y.mean(), stats.ttest_ind(x, y, equal_var=False).pvalue, len(x), len(y)


def ols_hac(y: np.ndarray, X: np.ndarray, lags: int = NW_LAGS):
    """OLS 계수와 Newey-West(Bartlett 커널) 공분산 행렬."""
    n, k = X.shape
    xtx_inv = np.linalg.inv(X.T @ X)
    beta = xtx_inv @ X.T @ y
    u = y - X @ beta
    xu = X * u[:, None]
    s = xu.T @ xu
    for lag in range(1, lags + 1):
        w = 1 - lag / (lags + 1)
        g = xu[lag:].T @ xu[:-lag]
        s += w * (g + g.T)
    cov = xtx_inv @ s @ xtx_inv * n / (n - k)   # 소표본 보정
    return beta, cov, n


def t_p(est: float, se: float, dof: int) -> float:
    return 2 * stats.t.sf(abs(est / se), dof)


# ---------------------------------------------------------------------------
# 1. 시장 모형(베타) 조정
# ---------------------------------------------------------------------------
def market_model(df: pd.DataFrame) -> list[dict]:
    rows = []
    m = df["SP500_Return"] * 100
    ctrl = df["G_ctrl"] == 1
    for asset in ["BA", "AAPL", "SOXX", "CAT", "XLI", "FXI"]:
        r = df[f"{asset}_Return"] * 100

        # (a) 대조일로 추정한 고정 베타: 이벤트일의 반응이 베타 추정에 섞이지 않게 한다.
        ok = ctrl & r.notna() & m.notna()
        b, a = np.polyfit(m[ok], r[ok], 1)
        ar_fixed = r - (a + b * m)

        # (b) 롤링 베타: t일의 베타는 t−250 ~ t−1일 자료로만 추정 (미래 정보 없음)
        cov = r.rolling(250, min_periods=120).cov(m).shift(1)
        var = m.rolling(250, min_periods=120).var().shift(1)
        b_roll = cov / var
        a_roll = (r.rolling(250, min_periods=120).mean().shift(1)
                  - b_roll * m.rolling(250, min_periods=120).mean().shift(1))
        ar_roll = r - (a_roll + b_roll * m)

        for label, series, beta_note in [("원수익률(본 분석)", r, np.nan),
                                         ("고정 베타 조정", ar_fixed, b),
                                         ("롤링 250일 베타 조정", ar_roll, b_roll.median())]:
            d, p, n1, n2 = welch(series[df["G_neg"] == 1], series[ctrl])
            rows.append({"분석": "1_시장모형", "자산": asset, "방식": label, "윈도우": "Day_T",
                         "추정치": d, "p": p, "N_이벤트": n1, "N_대조": n2, "비고": f"beta={beta_note:.2f}" if pd.notna(beta_note) else ""})
    return rows


# ---------------------------------------------------------------------------
# 2. 시차 더미 회귀 (Newey-West)
# ---------------------------------------------------------------------------
LAGS = [-1, 0, 1, 2]   # −1 = 선행(트윗 전날), 0 = 당일, 1 = 익일, 2 = 이틀 뒤


def lag_regression(df: pd.DataFrame) -> list[dict]:
    rows = []
    groups = ["G_neg", "G_pos", "G_noise", "G_mix"]
    targets = {"SP500": df["SP500_Return"] * 100, "BA": df["BA_Return"] * 100,
               "AAPL": df["AAPL_Return"] * 100, "SOXX": df["SOXX_Return"] * 100,
               "TNX(%변화)": df["TNX_Return"] * 100, "TNX(bp)": df["TNX_bp"],
               "CNY": df["CNY_Return"] * 100, "VIX": df["VIX_Return"] * 100}
    cols = {}
    for g in groups:
        for k in LAGS:
            cols[f"{g}_L{k}"] = df[g].shift(k)   # shift(1): 어제가 이벤트일 → 오늘은 T+1
    X_all = pd.DataFrame(cols)
    for name, y in targets.items():
        data = pd.concat([y.rename("y"), X_all], axis=1).dropna()
        X = np.column_stack([np.ones(len(data)), data[list(cols)].to_numpy()])
        beta, cov, n = ols_hac(data["y"].to_numpy(), X)
        dof = n - X.shape[1]
        idx = {c: i + 1 for i, c in enumerate(cols)}
        for k in LAGS:
            i = idx[f"G_neg_L{k}"]
            label = {-1: "T−1 (선행: 트윗 전날)", 0: "T (당일)", 1: "T+1 (익일)", 2: "T+2 (이틀 뒤)"}[k]
            se = np.sqrt(cov[i, i])
            rows.append({"분석": "2_시차회귀_NW", "자산": name, "방식": "순수 부정일 계수", "윈도우": label,
                         "추정치": beta[i], "p": t_p(beta[i], se, dof), "N_이벤트": int(data["G_neg_L0"].sum()),
                         "N_대조": n, "비고": f"HAC lag={NW_LAGS}, N=회귀 관측치"})
        for label, ks in [("누적 T~T+1 (CAR[0,+1])", [0, 1]), ("누적 T~T+2 (CAR[0,+2])", [0, 1, 2])]:
            w = np.zeros(X.shape[1])
            for k in ks:
                w[idx[f"G_neg_L{k}"]] = 1
            est, se = w @ beta, np.sqrt(w @ cov @ w)
            rows.append({"분석": "2_시차회귀_NW", "자산": name, "방식": "순수 부정일 누적", "윈도우": label,
                         "추정치": est, "p": t_p(est, se, dof), "N_이벤트": int(data["G_neg_L0"].sum()),
                         "N_대조": n, "비고": f"HAC lag={NW_LAGS}"})
    return rows


# ---------------------------------------------------------------------------
# 3. 10년물 금리 bp
# ---------------------------------------------------------------------------
def tnx_bp(df: pd.DataFrame) -> list[dict]:
    rows = []
    neg, ctrl = df["G_neg"] == 1, df["G_ctrl"] == 1
    covid = (df["Date"] >= "2020-02-20") & (df["Date"] <= "2020-06-30")
    pre2020 = df["Date"] < "2020-01-01"
    for label, keep in [("전체 기간", pd.Series(True, index=df.index)),
                        ("코로나 급락기 제외", ~covid), ("2020년 이후 제외", pre2020)]:
        for col, unit in [("TNX_bp", "bp 변화"), ("TNX_Return", "% 변화율")]:
            s = df[col] * (100 if col == "TNX_Return" else 1)
            d, p, n1, n2 = welch(s[neg & keep], s[ctrl & keep])
            rows.append({"분석": "3_금리_bp", "자산": "TNX", "방식": f"{unit} · {label}", "윈도우": "Day_T",
                         "추정치": d, "p": p, "N_이벤트": n1, "N_대조": n2, "비고": ""})
    return rows


# ---------------------------------------------------------------------------
# 4. 원형 이동 위약 검정
# ---------------------------------------------------------------------------
def circular_placebo(df: pd.DataFrame) -> list[dict]:
    rng = np.random.default_rng(SEED)
    n = len(df)
    r1 = df["CNY_Return"].shift(-1)
    c01 = (1 + df["CNY_Return"]) * (1 + r1) - 1
    targets = {"보잉 Day_T": (df["BA_Return"] * 100, -1),
               "10년물 금리 Day_T": (df["TNX_Return"] * 100, -1),
               "위안화 CAR[0,+1]": ((c01 - c01.mean()) * 100, 1),
               "S&P 500 Day_T": (df["SP500_Return"] * 100, -1)}
    neg = df["G_neg"].to_numpy().astype(bool)
    ctrl = df["G_ctrl"].to_numpy().astype(bool)
    shifts = rng.integers(20, n - 20, size=N_PLACEBO)   # 너무 작은 이동(원래 날짜와 거의 겹침)은 제외
    rows = []
    for name, (s, sign) in targets.items():
        v = s.to_numpy()
        actual = np.nanmean(v[neg]) - np.nanmean(v[ctrl])
        sims = np.array([np.nanmean(v[np.roll(neg, k)]) - np.nanmean(v[np.roll(ctrl, k)]) for k in shifts])
        p_emp = (np.sum(sign * sims >= sign * actual) + 1) / (N_PLACEBO + 1)
        rows.append({"분석": "4_원형이동_위약", "자산": name, "방식": f"{N_PLACEBO}회, seed={SEED}", "윈도우": "",
                     "추정치": actual, "p": p_emp, "N_이벤트": int(neg.sum()), "N_대조": int(ctrl.sum()),
                     "비고": f"위약 5~95%: {np.percentile(sims, 5):.3f} ~ {np.percentile(sims, 95):.3f}"})
    return rows


# ---------------------------------------------------------------------------
# 5. 군집·트윗 시각
# ---------------------------------------------------------------------------
def clustering_and_timing(df: pd.DataFrame) -> list[dict]:
    rows = []
    idx = np.flatnonzero(df["G_neg"].to_numpy())
    gaps = np.diff(idx)
    rows.append({"분석": "5_군집", "자산": "순수 부정일", "방식": "다음 순수 부정일이 1~2거래일 안에 오는 비율",
                 "윈도우": "", "추정치": np.mean(gaps <= 2) * 100, "p": np.nan, "N_이벤트": len(idx), "N_대조": np.nan,
                 "비고": f"연속(다음 날) {np.sum(gaps == 1)}회, 2일 이내 {np.sum(gaps <= 2)}회 / 간격 {len(gaps)}개"})

    # 부정 무역 트윗(연준 공격 제외)의 뉴욕 시각 분포
    tw = pd.read_csv(TWEET_PATH, low_memory=False, usecols=["source_group", "date_utc",
                                                            "existing_context_signal", "existing_context_sub_type"])
    a = tw[(tw["source_group"] == "existing_1246") & (tw["existing_context_signal"] == "Negative")
           & (tw["existing_context_sub_type"] != "NEG_Fed_Rate_Attack")]["date_utc"]
    om = pd.read_csv(OMISSION_PATH)
    b = om[(om["signal"] == "Negative") & (om["trade_topic"] == 1)]["date_utc"]
    t = pd.to_datetime(pd.concat([a, b]), utc=True).dt.tz_convert("America/New_York")
    minutes = t.dt.hour * 60 + t.dt.minute
    buckets = {"개장 전 (00:00~09:30)": minutes < 570,
               "정규장 (09:30~16:00)": (minutes >= 570) & (minutes < 960),
               "장 마감 후 (16:00~24:00) → 다음 거래일": minutes >= 960}
    for name, mask in buckets.items():
        rows.append({"분석": "5_트윗시각", "자산": "부정 무역 트윗", "방식": name, "윈도우": "",
                     "추정치": mask.mean() * 100, "p": np.nan, "N_이벤트": int(mask.sum()), "N_대조": len(t),
                     "비고": "추정치 = 비율(%)"})
    return rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_market()
    rows = (market_model(df) + lag_regression(df) + tnx_bp(df)
            + circular_placebo(df) + clustering_and_timing(df))
    out = pd.DataFrame(rows)
    out.to_csv(OUT_DIR / "qa_supplementary_checks.csv", index=False, encoding="utf-8-sig")
    pd.set_option("display.width", 220)
    pd.set_option("display.max_rows", 200)
    for name, g in out.groupby("분석", sort=False):
        print(f"\n=== {name} ===")
        print(g.drop(columns="분석").round(4).to_string(index=False))


if __name__ == "__main__":
    main()
