"""
기존 1,246건 분류에 누락 후보 138건을 합친 일별 변수(Merged_*)를 시장 데이터에 추가한다.

원칙
    - 기존 열은 수정·삭제하지 않는다. 기존 집계(Trade_*, Policy_*, Fed_*, Deal_*, Hard_Tariff_*)에
      누락 후보의 일별 건수를 더한 값을 새 열(Merged_*)로 붙인다.
    - 집계 규칙은 scripts/empirical_context_sentiment.py와 같다.
        Policy 긍정 = POS 세부 유형 3종, Policy 부정 = NEG_Tariff_Threat_Action / NEG_Protectionist_Attack /
        NEG_Company_Tech_Pressure (연준 공격은 Fed_Neg로 따로 센다)
        Trade_* = 무역 트윗(기존 키워드 729건 + 누락 후보 중 trade_topic = 1)
    - 다시 실행해도 같은 결과가 나오도록 기존 Merged_* 열은 지우고 새로 만든다.
    - scripts/build_analysis_ready_tweet_data.py로 시장 파일을 다시 만들면 Merged_* 열이 빠지므로
      그 뒤에 이 스크립트를 다시 실행한다.

입력
    data/trump_market_analysis_input.csv
    data/trump_omission_candidates_138_classified.csv (scripts/classify_omission_candidates.py)

실행
    python scripts/build_merged_market_variables.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MARKET_PATH = ROOT / "data" / "trump_market_analysis_input.csv"
OMISSION_PATH = ROOT / "data" / "trump_omission_candidates_138_classified.csv"

POLICY_POS = {"POS_Deal_Progress", "POS_Purchase_Agri_Support", "POS_US_Industry_Econ_Boom"}
POLICY_NEG = {"NEG_Tariff_Threat_Action", "NEG_Protectionist_Attack", "NEG_Company_Tech_Pressure"}


def daily_omission_counts(om: pd.DataFrame) -> pd.DataFrame:
    trade = om["trade_topic"] == 1
    flags = pd.DataFrame({
        "Date": om["mapped_trading_date"],
        "Trade_Tweet_Count": trade.astype(int),
        "Trade_Pos_Count": (trade & (om["signal"] == "Positive")).astype(int),
        "Trade_Neg_Count": (trade & (om["signal"] == "Negative")).astype(int),
        "Trade_Noise_Count": (trade & (om["signal"] == "Noise")).astype(int),
        "Policy_Pos_Count": om["subtype"].isin(POLICY_POS).astype(int),
        "Policy_Neg_Count": om["subtype"].isin(POLICY_NEG).astype(int),
        "Fed_Neg_Count": (om["subtype"] == "NEG_Fed_Rate_Attack").astype(int),
        "Deal_Pos_Count": (om["subtype"] == "POS_Deal_Progress").astype(int),
        "Hard_Tariff_Neg_Count": (om["subtype"] == "NEG_Tariff_Threat_Action").astype(int),
    })
    return flags.groupby("Date").sum()


def main():
    mkt = pd.read_csv(MARKET_PATH)
    mkt = mkt.drop(columns=[c for c in mkt.columns if c.startswith("Merged_")])
    n_cols = mkt.shape[1]
    om = pd.read_csv(OMISSION_PATH, encoding="utf-8-sig")

    add = daily_omission_counts(om)
    outside = sorted(set(add.index) - set(mkt["Date"]))
    assert not outside, f"시장 데이터에 없는 거래일: {outside}"
    add = add.reindex(mkt["Date"]).fillna(0).astype(int).reset_index(drop=True)

    new = pd.DataFrame(index=mkt.index)
    for col in add.columns:
        new[f"Merged_{col}"] = mkt[col].fillna(0).astype(int) + add[col]
    new["Merged_Trade_Tweet_Dummy"] = (new["Merged_Trade_Tweet_Count"] > 0).astype(int)
    for scope in ["Trade", "Policy"]:
        pos, neg = new[f"Merged_{scope}_Pos_Count"], new[f"Merged_{scope}_Neg_Count"]
        new[f"Merged_{scope}_Pos_Dummy"] = (pos > 0).astype(int)
        new[f"Merged_{scope}_Neg_Dummy"] = (neg > 0).astype(int)
        new[f"Merged_{scope}_Pure_Pos_Dummy"] = ((pos > 0) & (neg == 0)).astype(int)
        new[f"Merged_{scope}_Pure_Neg_Dummy"] = ((neg > 0) & (pos == 0)).astype(int)
        new[f"Merged_{scope}_Net_Signal"] = np.sign(pos - neg).astype(int)
    new["Merged_Fed_Neg_Dummy"] = (new["Merged_Fed_Neg_Count"] > 0).astype(int)
    new["Merged_Deal_Pos_Dummy"] = (new["Merged_Deal_Pos_Count"] > 0).astype(int)
    new["Merged_Hard_Tariff_Neg_Dummy"] = (new["Merged_Hard_Tariff_Neg_Count"] > 0).astype(int)

    out = pd.concat([mkt, new], axis=1)
    assert len(out) == 1007 and out.shape[1] == n_cols + new.shape[1]
    out.to_csv(MARKET_PATH, index=False, encoding="utf-8-sig")  # 원본과 같은 BOM 유지

    print(f"저장: {MARKET_PATH} ({out.shape[0]}거래일 × {out.shape[1]}열, Merged_* {new.shape[1]}열)")
    for old, merged in [
        ("Trade_Tweet_Dummy", "Merged_Trade_Tweet_Dummy"),
        ("Trade_Pure_Pos_Dummy", "Merged_Trade_Pure_Pos_Dummy"),
        ("Trade_Pure_Neg_Dummy", "Merged_Trade_Pure_Neg_Dummy"),
        ("Policy_Pure_Pos_Dummy", "Merged_Policy_Pure_Pos_Dummy"),
        ("Policy_Pure_Neg_Dummy", "Merged_Policy_Pure_Neg_Dummy"),
        ("Deal_Pos_Dummy", "Merged_Deal_Pos_Dummy"),
        ("Hard_Tariff_Neg_Dummy", "Merged_Hard_Tariff_Neg_Dummy"),
        ("Fed_Neg_Dummy", "Merged_Fed_Neg_Dummy"),
    ]:
        print(f"  {old:24s} {int(mkt[old].sum()):4d}일 → {int(out[merged].sum()):4d}일")


if __name__ == "__main__":
    main()
