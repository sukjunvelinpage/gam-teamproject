"""
누락 후보 138건(같은 문장 중복을 빼면 132건)을 팀원이 직접 분류하는 블라인드 검수 엑셀을 만든다.

- 기존 100건 검수(scripts/build_label_check_sample.py)와 같은 시트 구성·분류 기준·예시·열 배치를 쓴다.
- LLM 분류(data/trump_omission_candidates_138_classified.csv)는 엑셀에 넣지 않는다.
- 순서는 random_state=42로 섞는다. 한국어판과 베트남어판은 같은 132건·같은 순서다.
- 번역·당시 맥락은 scripts/omission_label_context.py에 있다 (AI 작성, 참고용).

출력
    docs/label_check/omission_label_check_132.xlsx     : 한국어판
    docs/label_check/omission_label_check_132_vi.xlsx  : 베트남어판
    docs/label_check/omission_context_ko.csv / _vi.csv : 번역·맥락 (audit_key 기준)

채점
    python scripts/score_label_check.py docs/label_check/omission_label_check_132.xlsx

실행
    python scripts/build_omission_label_check.py          # 두 언어 모두
    python scripts/build_omission_label_check.py ko       # 한국어판만
"""

import copy
import sys
from pathlib import Path

import pandas as pd

import build_label_check_sample as base
from omission_label_context import CONTEXT

ROOT = Path(__file__).resolve().parents[1]
OMISSION_PATH = ROOT / "data" / "trump_omission_candidates_138_classified.csv"
OUT_DIR = ROOT / "docs" / "label_check"
FILES = {
    "ko": {"xlsx": OUT_DIR / "omission_label_check_132.xlsx", "context": OUT_DIR / "omission_context_ko.csv"},
    "vi": {"xlsx": OUT_DIR / "omission_label_check_132_vi.xlsx", "context": OUT_DIR / "omission_context_vi.csv"},
}

# 안내 문구 중 분량만 바꾼다 (나머지 기준·예시는 100건 검수와 같다)
VOLUME = {
    "ko": ("트윗 100건. 1건당 30초~1분, 전체 1~1.5시간 정도 걸립니다.",
           "트윗 132건. 1건당 30초~1분, 전체 1.5~2시간 정도 걸립니다. 기존 분석에서 빠졌던 트윗을 새로 분류하는 작업입니다."),
    "vi": ("100 tweet. Mỗi tweet khoảng 30 giây – 1 phút, tổng cộng khoảng 1 – 1,5 giờ.",
           "132 tweet. Mỗi tweet khoảng 30 giây – 1 phút, tổng cộng khoảng 1,5 – 2 giờ. Đây là các tweet bị sót trong phân tích trước, nay được phân loại mới."),
}


def load_sample() -> pd.DataFrame:
    om = pd.read_csv(OMISSION_PATH, encoding="utf-8-sig")
    assert len(om) == 138, f"누락 후보는 138건이어야 합니다 (현재 {len(om)})"
    # 공백만 다른 같은 문장(예: 21124/21125)도 한 번만 넣는다
    om["_norm"] = om["text"].str.split().str.join(" ")
    sample = om.sort_values("raw_row").drop_duplicates("_norm").drop(columns="_norm")
    assert len(sample) == 132, f"중복 제외 후 132건이어야 합니다 (현재 {len(sample)})"
    missing = set(sample["raw_row"]) - set(CONTEXT)
    assert not missing, f"번역·맥락이 없는 행: {sorted(missing)}"
    sample = sample.sample(frac=1, random_state=base.SEED).reset_index(drop=True)
    sample["번호"] = range(1, len(sample) + 1)
    ny = pd.to_datetime(sample["date_utc"], utc=True).dt.tz_convert("America/New_York")
    sample["작성시각_뉴욕"] = ny.dt.strftime("%Y-%m-%d %H:%M")
    sample["리트윗"] = sample["isRetweet"].map({"t": "RT", "f": ""}).fillna("")
    return sample


def write_context(sample: pd.DataFrame, lang: str) -> Path:
    i = 0 if lang == "ko" else 2
    ctx = pd.DataFrame({
        "번호": sample["번호"],
        "audit_key": sample["audit_key"],
        "번역": sample["raw_row"].map(lambda r: CONTEXT[r][i]),
        "당시_맥락": sample["raw_row"].map(lambda r: CONTEXT[r][i + 1]),
    })
    path = FILES[lang]["context"]
    ctx.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def patch_text(lang: str):
    """build_label_check_sample.TEXT의 분량 문구만 바꾼 사본을 쓴다."""
    old, new = VOLUME[lang]
    text = copy.deepcopy(base.TEXT)
    rows = text[lang]["guide"]
    hits = [k for k, row in enumerate(rows) if len(row) > 1 and row[1] == old]
    assert len(hits) == 1, "분량 안내 문구를 찾지 못했습니다 (build_label_check_sample.py 문구 변경 확인)"
    rows[hits[0]][1] = new
    return text


def main(langs):
    sample = load_sample()
    legacy = base.load_existing_1246()  # 예시 트윗은 기존 1,246건에서 가져온다
    print(f"검수 대상 {len(sample)}건 (중복 문장 제외 전 138건)")
    for lang in langs:
        ctx_path = write_context(sample, lang)
        original = base.TEXT
        base.TEXT = patch_text(lang)
        try:
            wb = base.build_workbook(base.attach_context(sample, ctx_path), base.find_example_rows(legacy, lang), lang)
        finally:
            base.TEXT = original
        wb.save(FILES[lang]["xlsx"])
        print(f"[{lang}] 저장: {FILES[lang]['xlsx']}")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main(sys.argv[1:] or ["ko", "vi"])
