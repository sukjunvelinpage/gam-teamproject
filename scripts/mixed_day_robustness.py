"""
혼재일(같은 거래일에 긍정·부정 무역 트윗이 함께 있는 날) 처리 방식에 따른 강건성 점검 (Q&A 대비 자료).

배경
    본 분석은 '순수 부정일'(그날 무역 트윗이 부정만 있는 날, 123일)을 무역 트윗이 없는 날(656일)과 비교한다.
    혼재일 23일은 효과가 상쇄될 수 있어 제외했는데, 이 중에는 2019-05-06(긍정 1·부정 4),
    2019-05-10(긍정 1·부정 22) 같은 무역전쟁 핵심일이 들어 있다.
    → "부정이 압도적인 날을 왜 뺐나?"라는 질문에 대비해, 혼재일 처리 규칙을 바꿔도 결과가 같은지 확인한다.

비교 규칙 (모두 병합 기준 Merged_* 열, 대조군 = 무역 트윗이 없는 날, Welch's t-test)
    1_순수부정일(본분석)      : 부정 > 0, 긍정 = 0
    2_부정우세_혼재일_포함    : 1 + 부정 개수 > 긍정 개수인 혼재일 (다수결 규칙)
    3_부정있는날_전부         : 부정 > 0 (긍정 우세·동수 혼재일까지 포함)
    윈도우: 당일, 익일, CAR[0,+1], CAR[0,+2]  (scripts/reanalysis_merged_omissions.py와 동일 정의)

출력
    docs/reanalysis_2026-11-10/mixed_day_robustness.csv

실행
    python scripts/mixed_day_robustness.py
"""

from pathlib import Path

import pandas as pd

from reanalysis_merged_omissions import MARKET_PATH, OUT_DIR, WINDOWS, welch, windows

ASSETS = ["SP500", "BA", "AAPL", "SOXX", "TNX", "CNY", "FXI"]


def rules(df: pd.DataFrame) -> dict:
    pos, neg = df["Merged_Trade_Pos_Count"], df["Merged_Trade_Neg_Count"]
    return {
        "1_순수부정일(본분석)": (neg > 0) & (pos == 0),
        "2_부정우세_혼재일_포함": (neg > 0) & (neg > pos),
        "3_부정있는날_전부": neg > 0,
    }


def main():
    df = pd.read_csv(MARKET_PATH)
    base = df["Merged_Trade_Tweet_Dummy"] == 0
    rows = []
    for asset in ASSETS:
        for win, s in windows(df[f"{asset}_Return"]).items():
            for name, mask in rules(df).items():
                diff, p, n1, n0 = welch(s, mask, base)
                rows.append({"asset": asset, "window": win, "rule": name,
                             "event_days": n1, "control_days": n0,
                             "diff_pct": round(diff, 4), "p_value": round(p, 4)})
    out = pd.DataFrame(rows)
    out["window"] = pd.Categorical(out["window"], WINDOWS, ordered=True)
    out = out.sort_values(["asset", "window", "rule"])
    path = OUT_DIR / "mixed_day_robustness.csv"
    out.to_csv(path, index=False, encoding="utf-8-sig")

    pos, neg = df["Merged_Trade_Pos_Count"], df["Merged_Trade_Neg_Count"]
    mixed = (pos > 0) & (neg > 0)
    print(f"혼재일 {mixed.sum()}일: 부정 우세 {(mixed & (neg > pos)).sum()} / "
          f"동수 {(mixed & (neg == pos)).sum()} / 긍정 우세 {(mixed & (neg < pos)).sum()}")
    key = out[out["window"].isin(["Day_T", "CAR[0,+1]", "CAR[0,+2]"])]
    print(key.pivot_table(index=["asset", "window"], columns="rule",
                          values=["diff_pct", "p_value"], observed=True).round(3).to_string())
    print(f"saved: {path}")


if __name__ == "__main__":
    main()
