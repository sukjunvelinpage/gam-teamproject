"""
기존 1,246건 기준 결과와, 누락 후보 138건을 합친 병합 기준(Merged_*) 결과를 나란히 비교한다.

비교 설계 (모두 Welch's t-test, equal_var=False)
    A. 무역 트윗일 분리: 통합 / 순수 긍정 / 순수 부정 / 소음만  vs  무역 트윗이 없는 날
    B. 정책 트윗: 순수 긍정 vs 순수 부정, 각각 vs 무신호일(정책 긍·부정과 연준 공격이 모두 없는 날)
    C. 협상 진전일 vs 관세 위협일 (서로 겹치지 않는 날)
    윈도우: 당일(Day_T), 익일(Day_T+1), CAR[0,+1], CAR[0,+2]  (scripts/empirical_context_sentiment.py와 동일)

강건성 점검 (핵심 결과에만)
    - 월 고정효과: 각 날의 값에서 같은 달 평균을 뺀 뒤 같은 검정
    - 2020년 이후 제외
    - 다중검정: 비교 묶음별 64개(16자산 × 4윈도우)에 BH 보정(q < 0.10)

출력
    docs/reanalysis_2026-11-10/reanalysis_full.csv     : 전체 검정 결과 (기존 vs 병합)
    docs/reanalysis_2026-11-10/reanalysis_robustness.csv : 핵심 결과의 강건성 점검

실행
    python scripts/build_merged_market_variables.py   # Merged_* 열이 없을 때 먼저 실행
    python scripts/reanalysis_merged_omissions.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
MARKET_PATH = ROOT / "data" / "trump_market_analysis_input.csv"
OUT_DIR = ROOT / "docs" / "reanalysis_2026-11-10"

ASSETS = ["SP500", "VIX", "DXY", "NUE", "SLX", "XLI", "SOXX", "AAPL", "BA", "CAT",
          "TNX", "SHY", "XLF", "FXI", "CNY", "GLD"]
WINDOWS = ["Day_T", "Day_T+1", "CAR[0,+1]", "CAR[0,+2]"]


def windows(r: pd.Series) -> dict:
    r1, r2 = r.shift(-1), r.shift(-2)
    c01 = (1 + r) * (1 + r1) - 1
    c02 = (1 + r) * (1 + r1) * (1 + r2) - 1
    return {"Day_T": r * 100, "Day_T+1": r1 * 100,
            "CAR[0,+1]": (c01 - c01.mean()) * 100, "CAR[0,+2]": (c02 - c02.mean()) * 100}


def welch(s: pd.Series, a: pd.Series, b: pd.Series):
    x, y = s[a].dropna(), s[b].dropna()
    return x.mean() - y.mean(), stats.ttest_ind(x, y, equal_var=False).pvalue, len(x), len(y)


def bh(p: pd.Series, q: float = 0.10) -> pd.Series:
    """Benjamini-Hochberg: 보정 후 통과 여부."""
    order = p.sort_values()
    m = len(order)
    passed = order <= (np.arange(1, m + 1) / m) * q
    k = passed[passed].index.max() if passed.any() else None
    cutoff = order.loc[k] if k is not None else -1
    return p <= cutoff


def comparisons(df: pd.DataFrame, prefix: str) -> dict:
    """비교 이름 → (이벤트 마스크, 대조 마스크). prefix는 '' (기존) 또는 'Merged_' (병합)."""
    g = lambda c: df[f"{prefix}{c}"]
    trade = g("Trade_Tweet_Dummy") == 1
    tpos, tneg = g("Trade_Pos_Count") > 0, g("Trade_Neg_Count") > 0
    ppos, pneg = g("Policy_Pure_Pos_Dummy") == 1, g("Policy_Pure_Neg_Dummy") == 1
    none = (g("Policy_Pos_Dummy") == 0) & (g("Policy_Neg_Dummy") == 0) & (g("Fed_Neg_Dummy") == 0)
    deal = (g("Deal_Pos_Dummy") == 1) & (g("Hard_Tariff_Neg_Dummy") == 0)
    hard = (g("Hard_Tariff_Neg_Dummy") == 1) & (g("Deal_Pos_Dummy") == 0)
    return {
        "A_무역_통합_vs_무무역일": (trade, ~trade),
        "A_무역_순수긍정_vs_무무역일": (trade & tpos & ~tneg, ~trade),
        "A_무역_순수부정_vs_무무역일": (trade & tneg & ~tpos, ~trade),
        "A_무역_소음만_vs_무무역일": (trade & ~tpos & ~tneg, ~trade),
        "B_정책_순수긍정_vs_순수부정": (ppos, pneg),
        "B_정책_순수긍정_vs_무신호일": (ppos, none),
        "B_정책_순수부정_vs_무신호일": (pneg, none),
        "C_협상진전_vs_관세위협": (deal, hard),
    }


def full_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for label, prefix in [("기존", ""), ("병합", "Merged_")]:
        for name, (ev, ct) in comparisons(df, prefix).items():
            for asset in ASSETS:
                for win, s in windows(df[f"{asset}_Return"]).items():
                    diff, p, n1, n2 = welch(s, ev, ct)
                    rows.append({"기준": label, "비교": name, "자산": asset, "윈도우": win,
                                 "차이": diff, "p": p, "N_이벤트": n1, "N_대조": n2})
    out = pd.DataFrame(rows)
    out["BH_통과"] = out.groupby(["기준", "비교"])["p"].transform(bh)
    return out


# 발표에 쓰는 핵심 결과: (비교, 자산, 윈도우)
KEY = [
    ("A_무역_통합_vs_무무역일", "SP500", "Day_T"),
    ("A_무역_통합_vs_무무역일", "VIX", "Day_T"),
    ("A_무역_순수부정_vs_무무역일", "VIX", "Day_T"),
    ("A_무역_소음만_vs_무무역일", "VIX", "Day_T"),
    ("A_무역_순수부정_vs_무무역일", "SP500", "CAR[0,+1]"),
    ("A_무역_순수부정_vs_무무역일", "BA", "Day_T"),
    ("A_무역_순수부정_vs_무무역일", "AAPL", "Day_T"),
    ("A_무역_순수부정_vs_무무역일", "SOXX", "Day_T"),
    ("A_무역_순수긍정_vs_무무역일", "AAPL", "Day_T"),
    ("A_무역_순수부정_vs_무무역일", "NUE", "Day_T"),
    ("A_무역_순수부정_vs_무무역일", "TNX", "Day_T"),
    ("A_무역_순수부정_vs_무무역일", "CNY", "CAR[0,+1]"),
    ("A_무역_순수긍정_vs_무무역일", "FXI", "Day_T"),
    ("A_무역_순수긍정_vs_무무역일", "FXI", "CAR[0,+1]"),
    ("A_무역_순수부정_vs_무무역일", "GLD", "Day_T"),
    ("B_정책_순수긍정_vs_순수부정", "SP500", "Day_T"),
    ("B_정책_순수긍정_vs_순수부정", "AAPL", "Day_T"),
    ("B_정책_순수긍정_vs_순수부정", "BA", "Day_T"),
    ("B_정책_순수긍정_vs_순수부정", "SOXX", "Day_T"),
    ("B_정책_순수긍정_vs_순수부정", "CNY", "CAR[0,+1]"),
    ("B_정책_순수부정_vs_무신호일", "BA", "Day_T"),
    ("B_정책_순수부정_vs_무신호일", "TNX", "Day_T"),
    ("B_정책_순수부정_vs_무신호일", "CNY", "CAR[0,+1]"),
    ("C_협상진전_vs_관세위협", "FXI", "CAR[0,+1]"),
    ("C_협상진전_vs_관세위협", "TNX", "CAR[0,+1]"),
    ("C_협상진전_vs_관세위협", "SLX", "CAR[0,+1]"),
    ("C_협상진전_vs_관세위협", "CNY", "CAR[0,+1]"),
]


def robustness(df: pd.DataFrame) -> pd.DataFrame:
    month = pd.to_datetime(df["Date"]).dt.to_period("M")
    pre2020 = pd.to_datetime(df["Date"]) < "2020-01-01"
    rows = []
    for label, prefix in [("기존", ""), ("병합", "Merged_")]:
        comps = comparisons(df, prefix)
        for name, asset, win in KEY:
            ev, ct = comps[name]
            s = windows(df[f"{asset}_Return"])[win]
            fe = s - s.groupby(month).transform("mean")
            d0, p0, n1, n2 = welch(s, ev, ct)
            d1, p1, _, _ = welch(fe, ev, ct)
            d2, p2, _, _ = welch(s, ev & pre2020, ct & pre2020)
            rows.append({"기준": label, "비교": name, "자산": asset, "윈도우": win, "N_이벤트": n1, "N_대조": n2,
                         "차이": d0, "p": p0, "월FE_차이": d1, "월FE_p": p1, "2020제외_차이": d2, "2020제외_p": p2})
    return pd.DataFrame(rows)


def main():
    df = pd.read_csv(MARKET_PATH)
    assert "Merged_Trade_Tweet_Dummy" in df.columns, "먼저 scripts/build_merged_market_variables.py를 실행하세요"
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    full = full_table(df)
    full.to_csv(OUT_DIR / "reanalysis_full.csv", index=False, encoding="utf-8-sig")
    rob = robustness(df)
    rob.to_csv(OUT_DIR / "reanalysis_robustness.csv", index=False, encoding="utf-8-sig")

    pd.set_option("display.width", 250)
    wide = rob.pivot_table(index=["비교", "자산", "윈도우"], columns="기준",
                           values=["차이", "p", "월FE_p", "2020제외_p", "N_이벤트"], sort=False)
    print(wide.round(3).to_string())
    print("\nBH(q<0.10) 통과 건수:")
    print(full.groupby(["비교", "기준"])["BH_통과"].sum().unstack().to_string())


if __name__ == "__main__":
    main()
