"""
팀원이 채운 라벨링 엑셀과 LLM 1차 분류(legacy_signal)의 일치율을 계산한다.

계산 항목
    - 단순 일치율: 100건 중 몇 건이 같은가
    - Cohen's kappa: 우연히 맞을 확률을 뺀 일치도 (0.61~0.80 '상당한 일치', 0.81 이상 '거의 완전한 일치', Landis & Koch 1977)
    - 혼동표(사람 분류 × LLM 분류)
    - '확실'로 표시한 건만 따로 본 일치율
    - 불일치 목록 CSV (팀 토의용)

실행 (한국어판·베트남어판 모두 같은 명령)
    python scripts/score_label_check.py                       # 기본 경로의 한국어판 엑셀 사용
    python scripts/score_label_check.py 채운파일.xlsx           # 다른 파일 지정 (예: ..._vi.xlsx)
"""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TWEETS_PATH = ROOT / "data" / "trump_tweets_analysis_input.csv"
DEFAULT_XLSX = ROOT / "docs" / "label_check" / "label_check_sample_100.xlsx"
OUT_DIR = ROOT / "docs" / "label_check"

LLM_TO_KO = {"Positive": "긍정", "Negative": "부정", "Noise": "소음"}
LABELS = ["긍정", "부정", "소음"]


def cohen_kappa(a: pd.Series, b: pd.Series) -> float:
    po = (a == b).mean()
    pe = sum((a == k).mean() * (b == k).mean() for k in LABELS)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


# 베트남어판 드롭다운 값 → 한국어 코드 (build_label_check_sample.LABELS와 같아야 함)
VI_TO_KO = {"Tích cực": "긍정", "Tiêu cực": "부정", "Nhiễu": "소음", "Chắc chắn": "확실", "Phân vân": "애매"}
# 라벨링 시트 열 배치 (한국어판·베트남어판 공통, 헤더 언어와 무관하게 위치로 읽는다)
COLS = ["번호", "작성시각", "RT", "트윗 원문", "번역", "당시 맥락", "내 분류", "확신도", "한 줄 근거", "audit_key"]


def main(xlsx_path: Path):
    sheets = pd.read_excel(xlsx_path, sheet_name=None)
    sheet = next(name for name in sheets if name.startswith("4_"))
    human = sheets[sheet].iloc[:, : len(COLS)]
    human.columns = COLS
    for col in ["내 분류", "확신도"]:
        human[col] = human[col].astype("string").str.strip().replace(VI_TO_KO)

    blank = human["내 분류"].isna().sum()
    bad = human[human["내 분류"].notna() & ~human["내 분류"].isin(LABELS)]
    if blank or len(bad):
        print(f"[확인 필요] 빈 칸 {blank}건, 잘못된 값 {len(bad)}건 (번호: {bad['번호'].tolist()})")
    done = human[human["내 분류"].isin(LABELS)].copy()

    tweets = pd.read_csv(TWEETS_PATH, low_memory=False, usecols=["audit_key", "legacy_signal", "legacy_subtype", "existing_context_reason_ko"])
    merged = done.merge(tweets, on="audit_key", how="left", validate="one_to_one")
    assert merged["legacy_signal"].notna().all(), "audit_key가 원본과 맞지 않는 행이 있습니다 (열을 수정했는지 확인)"
    merged["LLM 분류"] = merged["legacy_signal"].map(LLM_TO_KO)
    merged["일치"] = merged["내 분류"] == merged["LLM 분류"]

    n = len(merged)
    agree = int(merged["일치"].sum())
    kappa = cohen_kappa(merged["내 분류"], merged["LLM 분류"])
    sure = merged[merged["확신도"] == "확실"]

    print(f"\n검수 완료 {n}건 중 일치 {agree}건 → 일치율 {agree / n:.1%}")
    print(f"Cohen's kappa = {kappa:.3f}")
    if len(sure):
        print(f"'확실' 표시 {len(sure)}건만 보면 일치율 {sure['일치'].mean():.1%}, kappa {cohen_kappa(sure['내 분류'], sure['LLM 분류']):.3f}")

    table = pd.crosstab(merged["내 분류"], merged["LLM 분류"], margins=True, margins_name="합계")
    table = table.reindex(index=LABELS + ["합계"], columns=LABELS + ["합계"], fill_value=0)
    print("\n혼동표 (행: 사람, 열: LLM)")
    print(table.to_string())

    print("\nLLM 분류별 사람 일치율")
    for k in LABELS:
        g = merged[merged["LLM 분류"] == k]
        if len(g):
            print(f"  LLM '{k}' {len(g)}건 → 사람도 '{k}' {int(g['일치'].sum())}건 ({g['일치'].mean():.0%})")

    diff = merged[~merged["일치"]][["번호", "트윗 원문", "내 분류", "확신도", "한 줄 근거", "LLM 분류", "legacy_subtype", "existing_context_reason_ko"]]
    diff = diff.rename(columns={"legacy_subtype": "LLM 세부유형", "existing_context_reason_ko": "LLM 판정 사유"})
    diff_path = OUT_DIR / f"label_check_disagreements_{xlsx_path.stem}.csv"
    diff.to_csv(diff_path, index=False, encoding="utf-8-sig")
    print(f"\n불일치 {len(diff)}건 저장: {diff_path} (팀 토의용)")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_XLSX)
