"""
다중검정 한계 보완: 핵심 가설군 보정 + 무작위 배정 위약(placebo) 검정 (병합 기준)

배경
    reanalysis_merged_omissions.py는 비교 하나당 64개(16자산 × 4윈도우)를 한 묶음으로 BH 보정한다.
    이 묶음에는 사전 가설이 없던 자산도 들어 있어, 핵심 결과의 우연 가능성을 따로 점검한다.

1. 핵심 가설군 보정
    가설: "무역 부정 트윗일에 중국 노출 자산이 반응한다" (중국 매출 비중이라는 경제적 근거)
    대상 5개: 보잉·애플·반도체·10년물 금리(당일), 위안화(2일 누적)  ← 순수 부정일 vs 무역 트윗 없는 날
    주의: 이 5개는 데이터를 본 뒤 정했으므로, 64개 보정 결과와 함께 제시한다.
    보정: Bonferroni(0.05/5), Holm, BH(q=0.05, 0.10)

2. 무작위 배정 위약 검정 (N_SIM회, 시드 42)
    순수 부정일(123일) + 무역 트윗 없는 날(656일) = 779일 안에서 '부정일' 이름표를 무작위로 123일에 다시 붙인다.
    두 가지 방식:
      - 단순 무작위: 779일 전체에서 뽑는다
      - 같은 달 안 무작위: 각 달의 실제 부정일 수만큼 그 달 안에서 뽑는다 (시기 효과 통제)
    점검 지표:
      - 자산별 경험적 p: 가설 방향으로 실제 차이 이상이 나온 비율
      - 동시 유의 개수: 5개 중 가설 방향으로 Welch p < 0.05인 자산 수가 실제 이상인 비율

실행
    python scripts/multiple_testing_placebo.py
출력
    docs/reanalysis_2026-11-10/multiple_testing_family.csv
    docs/reanalysis_2026-11-10/placebo_test.csv
"""

import numpy as np
import pandas as pd
from scipy import stats

from reanalysis_merged_omissions import MARKET_PATH, OUT_DIR, comparisons, windows

N_SIM = 1000
SEED = 42
COMP = "A_무역_순수부정_vs_무무역일"
# (자산, 윈도우, 가설 방향: -1 하락, +1 상승)
FAMILY = [("BA", "Day_T", -1), ("AAPL", "Day_T", -1), ("SOXX", "Day_T", -1),
          ("TNX", "Day_T", -1), ("CNY", "CAR[0,+1]", +1)]
NAMES = {"BA": "보잉", "AAPL": "애플", "SOXX": "반도체 ETF", "TNX": "10년물 금리", "CNY": "위안화 약세(USD/CNY)"}


def welch(x: np.ndarray, y: np.ndarray):
    t, p = stats.ttest_ind(x, y, equal_var=False)
    return x.mean() - y.mean(), p


def holm(p: np.ndarray, alpha: float = 0.05) -> np.ndarray:
    order = np.argsort(p)
    passed = np.zeros(len(p), bool)
    for k, i in enumerate(order):
        if p[i] <= alpha / (len(p) - k):
            passed[i] = True
        else:
            break
    return passed


def bh(p: np.ndarray, q: float) -> np.ndarray:
    order = np.argsort(p)
    m = len(p)
    ok = p[order] <= np.arange(1, m + 1) / m * q
    passed = np.zeros(m, bool)
    if ok.any():
        passed[order[: np.max(np.where(ok)[0]) + 1]] = True
    return passed


def main():
    df = pd.read_csv(MARKET_PATH)
    ev, ct = comparisons(df, "Merged_")[COMP]
    pool = (ev | ct).to_numpy()
    month = pd.to_datetime(df["Date"]).dt.to_period("M").to_numpy()

    # 자산별 시계열 (pool 안에서 결측 없는 날만 쓰도록 마스크 보관)
    series = {a: windows(df[f"{a}_Return"])[w].to_numpy() for a, w, _ in FAMILY}

    # ---- 1. 실제 결과 + 가설군 보정 ----
    actual = []
    for a, w, sign in FAMILY:
        s = series[a]
        x, y = s[ev.to_numpy() & ~np.isnan(s)], s[ct.to_numpy() & ~np.isnan(s)]
        d, p = welch(x, y)
        actual.append({"자산": a, "이름": NAMES[a], "윈도우": w, "가설방향": sign, "차이": d, "p": p,
                       "N_이벤트": len(x), "N_대조": len(y)})
    fam = pd.DataFrame(actual)
    pv = fam["p"].to_numpy()
    fam["Bonferroni_0.05"] = pv <= 0.05 / len(pv)
    fam["Holm_0.05"] = holm(pv)
    fam["BH_q0.05"] = bh(pv, 0.05)
    fam["BH_q0.10"] = bh(pv, 0.10)
    n_actual_sig = int(((np.sign(fam["차이"]) == fam["가설방향"]) & (fam["p"] < 0.05)).sum())

    # ---- 2. 위약 검정 ----
    rng = np.random.default_rng(SEED)
    pool_idx = np.where(pool)[0]
    n_ev = int(ev.sum())
    ev_months = pd.Series(month[ev.to_numpy()]).value_counts()
    by_month = {m: pool_idx[month[pool_idx] == m] for m in ev_months.index}

    def draw(kind: str) -> np.ndarray:
        if kind == "단순 무작위":
            pick = rng.choice(pool_idx, n_ev, replace=False)
        else:
            pick = np.concatenate([rng.choice(by_month[m], k, replace=False) for m, k in ev_months.items()])
        mask = np.zeros(len(df), bool)
        mask[pick] = True
        return mask

    rows = []
    for kind in ["단순 무작위", "같은 달 안 무작위"]:
        sims = np.zeros((N_SIM, len(FAMILY)))
        sig = np.zeros(N_SIM, int)
        for i in range(N_SIM):
            e = draw(kind)
            c = pool & ~e
            for j, (a, w, sign) in enumerate(FAMILY):
                s = series[a]
                x, y = s[e & ~np.isnan(s)], s[c & ~np.isnan(s)]
                d, p = welch(x, y)
                sims[i, j] = d
                sig[i] += int(np.sign(d) == sign and p < 0.05)
        for j, (a, w, sign) in enumerate(FAMILY):
            act = fam.loc[j, "차이"]
            rows.append({"방식": kind, "지표": f"{NAMES[a]} {w}", "실제값": act,
                         "위약_평균": sims[:, j].mean(), "위약_5%분위": np.percentile(sims[:, j], 5),
                         "위약_95%분위": np.percentile(sims[:, j], 95),
                         "경험적_p(가설방향)": (np.sum(sign * sims[:, j] >= sign * act) + 1) / (N_SIM + 1)})
        rows.append({"방식": kind, "지표": f"5개 중 가설방향 p<0.05 개수 ≥ {n_actual_sig}", "실제값": n_actual_sig,
                     "위약_평균": sig.mean(), "위약_5%분위": np.percentile(sig, 5), "위약_95%분위": np.percentile(sig, 95),
                     "경험적_p(가설방향)": (np.sum(sig >= n_actual_sig) + 1) / (N_SIM + 1)})
        rows.append({"방식": kind, "지표": "5개 중 가설방향 p<0.05 개수 ≥ 3", "실제값": n_actual_sig,
                     "위약_평균": sig.mean(), "위약_5%분위": np.percentile(sig, 5), "위약_95%분위": np.percentile(sig, 95),
                     "경험적_p(가설방향)": (np.sum(sig >= 3) + 1) / (N_SIM + 1)})
    plc = pd.DataFrame(rows)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fam.to_csv(OUT_DIR / "multiple_testing_family.csv", index=False, encoding="utf-8-sig")
    plc.to_csv(OUT_DIR / "placebo_test.csv", index=False, encoding="utf-8-sig")

    pd.set_option("display.width", 250)
    print("1. 핵심 가설군(5개) 보정")
    print(fam.round(4).to_string(index=False))
    print(f"\n2. 위약 검정 ({N_SIM}회, 시드 {SEED})")
    print(plc.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
