"""보존된 감사 결과와 명시적 검토 결정을 연결해 보고서와 검토 원장을 만든다."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "docs/tweet_audit_2026-11-02"


def save(df: pd.DataFrame, name: str) -> None:
    df.to_csv(OUT / name, index=False, encoding="utf-8-sig")


def main() -> None:
    summary = json.loads((OUT / "audit_summary.json").read_text(encoding="utf-8"))
    decisions = json.loads((OUT / "review_decisions.json").read_text(encoding="utf-8"))
    existing = pd.read_csv(OUT / "existing_classification_audit.csv", dtype={"id": str})
    omissions = pd.read_csv(OUT / "omission_candidates.csv", dtype={"id": str})
    raw = pd.read_csv(OUT / "full_corpus_screening.csv", dtype={"id": str})
    mapping = pd.read_csv(OUT / "trading_date_audit.csv")
    cross = pd.read_csv(OUT / "exact_id_crosswalk.csv", dtype={"stored_id": str, "reference_exact_id": str})
    existing["tweet_idx"] = existing.tweet_idx.astype(int)
    existing["review_disposition"] = "본문 검토상 유지(잠정)"
    existing["review_scope"] = "본문 개별 열람; 연결 매체 전수 복원 아님"
    existing["review_issues"] = ""
    existing["review_reason_ko"] = "기존 정의 아래에서 명백한 수정 근거를 특정하지 못함. 독립 정답 라벨·복수 평가자 합의로 검증된 판정은 아님."
    existing["proposed_themes"] = ""
    existing["proposed_direction"] = ""
    for finding in decisions["existing_findings"]:
        assert set(finding["ids"]) <= set(existing.tweet_idx), finding
        mask = existing.tweet_idx.isin(finding["ids"])
        existing.loc[mask, "review_disposition"] = finding["verdict"]
        for col, field in [("review_issues", "issue"), ("review_reason_ko", "reason"), ("proposed_themes", "proposed_theme"), ("proposed_direction", "proposed_direction")]:
            for i in existing.index[mask]:
                prior = existing.at[i, col] if col != "review_reason_ko" or existing.at[i, "review_issues"] != finding["issue"] else ""
                # 多重 테마의 검토 근거를 지우지 않는다.
                if col == "review_reason_ko" and prior.startswith("기존 정의 아래"):
                    prior = ""
                existing.at[i, col] = "; ".join(x for x in [prior, finding[field]] if x)
    # 동명이인·관용구의 기존 Noise 판정을 별도로 명시한다.
    ent = existing.entity_or_idiom_flag & existing.review_issues.eq("")
    existing.loc[ent, "review_reason_ko"] = "원문상 인명·관용구·국경 구조물 등으로 확인. 현재 Noise 유지가 적절하며 테마 키워드 자체를 정책사건으로 사용해서는 안 됨."
    existing.loc[ent, "review_issues"] = "ENTITY_OR_IDIOM_CORRECTLY_EXCLUDED"
    # 검토 이슈가 아닌 유지 확인도 포함하므로, flagged 정의는 판정이 유지가 아닌 행이다.
    flagged = ~existing.review_disposition.eq("본문 검토상 유지(잠정)")
    omissions["review_disposition"] = "추가 판정 보류(소음·낮은 강도·범위 확장 후보 포함)"
    omissions["proposed_themes"] = ""
    omissions["proposed_direction"] = "Unknown"
    omissions["review_reason_ko"] = "확장 규칙으로 검출되어 본문을 열람했으나, 이 검토에서 현행 분석에 포함할 정책사건으로 확정하지 않음. 누락 확정치에 포함하지 않음."
    confirmed = set()
    for finding in decisions["confirmed_omissions"]:
        assert set(finding["raw_rows"]) <= set(omissions.raw_row), finding
        mask = omissions.raw_row.isin(finding["raw_rows"])
        omissions.loc[mask, "review_disposition"] = "현행 범주와 대조한 추가 분류 필요"
        omissions.loc[mask, "proposed_themes"] = finding["theme"]
        omissions.loc[mask, "proposed_direction"] = finding["direction"]
        omissions.loc[mask, "review_reason_ko"] = finding["reason"]
        confirmed.update(finding["raw_rows"])
    # 넓은 검색이 왜 곧바로 정답이 아닌지를 보여 주는 확인 가능한 오탐.
    false_positive_rows = [15262,14520,14512,18860,17611,17398,16641,4619,7317,2946,6577,7763,8467,8619,22396,6802,14734,15947,1304,2055]
    mask = omissions.raw_row.isin(false_positive_rows)
    assert not (mask & omissions.raw_row.isin(confirmed)).any()
    omissions.loc[mask, "review_disposition"] = "확장 검색 오탐 확인·제외 적절"
    omissions.loc[mask, "review_reason_ko"] = "GM=교통기관 직책, Ford=항공모함·인명·의료기관, currency=종교문구, duties=직무, phase 1=백신·건강검진, trade=증인 교환·마약거래·정치적 이동·세계무역센터, Amazon=열대우림 등으로 본문 확인. 기업·무역 정책사건이 아님."

    cross_small = cross[["raw_row", "reference_exact_id", "reference_url", "text_similarity"]]
    existing = existing.merge(cross_small, on="raw_row", how="left", validate="one_to_one")
    omissions = omissions.merge(cross_small, on="raw_row", how="left", validate="one_to_one")
    existing = existing.merge(mapping[["tweet_idx", "snowflake_utc", "timestamp_conflict", "snowflake_actual_close_expected", "snowflake_actual_close_mismatch"]], on="tweet_idx", how="left", validate="one_to_one")
    save(existing, "existing_review_ledger.csv")
    save(omissions, "omission_review_ledger.csv")
    confirmed_df = omissions[omissions.raw_row.isin(confirmed)].copy()
    save(confirmed_df, "confirmed_scope_omissions.csv")
    classified_by_raw = existing.set_index("raw_row")
    omission_by_raw = omissions.set_index("raw_row")
    raw["semantic_review_scope"] = "자동 점검만·의미 미확정"
    raw.loc[raw.raw_row.isin(classified_by_raw.index), "semantic_review_scope"] = "기존 분류 본문 개별 열람"
    raw.loc[raw.raw_row.isin(omission_by_raw.index), "semantic_review_scope"] = "추가 후보 본문 개별 열람"
    save(raw, "full_corpus_review_coverage.csv")

    # 저장된 시각 자체의 오류가 전체 거래일 집계에 미칠 규모를 추가 확인.
    days = pd.DatetimeIndex(pd.to_datetime(pd.read_csv(BASE / "data/trump_market_extended_data.csv").Date))
    def fixed16_map(dates):
        est = dates.dt.tz_convert("America/New_York")
        target = est.dt.tz_localize(None).dt.normalize() + pd.to_timedelta(est.dt.hour.ge(16).astype(int), unit="D")
        return [str(days[i].date()) if i < len(days) else "" for i in days.searchsorted(target)]
    stored_dates = pd.to_datetime(raw.date_utc, utc=True)
    snow_dates = pd.to_datetime(raw.id.map(lambda s: (int(s) >> 22) + 1288834974657), unit="ms", utc=True)
    old_map, new_map = fixed16_map(stored_dates), fixed16_map(snow_dates)
    raw_mapping_changes = sum(x != y for x, y in zip(old_map, new_map))
    pcount = int((existing.context_signal.eq("Positive") & flagged).sum())
    ncount = int((existing.context_signal.eq("Negative") & flagged).sum())
    zcount = int((existing.context_signal.eq("Noise") & flagged).sum())
    # 참조 아카이브의 후보 URL은 텍스트 유사성과 ID 근접도를 함께 사용한 잠정 교차키다.
    extra = {"review_flagged_existing_unique": int(flagged.sum()), "review_retained_existing": int((~flagged).sum()), "review_flags_by_signal": {"Positive": pcount, "Negative": ncount, "Noise": zcount}, "confirmed_scope_omissions": len(confirmed), "confirmed_scope_omission_signal_days_fixed16": len(set(fixed16_map(pd.to_datetime(confirmed_df.date_utc, utc=True)))), "expanded_search_false_positive_examples": int(mask.sum()), "raw_fixed16_trading_date_changes_from_snowflake": raw_mapping_changes, "semantic_existing_texts_read": len(existing), "semantic_omission_candidate_texts_read": len(omissions), "semantic_unreviewed_raw_rows": len(raw) - len(existing) - len(omissions), "independent_reference_matched_raw_rows_by_near_id": int(cross.reference_exact_id.notna().sum()), "independent_reference_text_similarity_ge_08": int(cross.text_similarity.ge(.8).sum())}
    (OUT / "review_summary.json").write_text(json.dumps(extra, ensure_ascii=False, indent=2), encoding="utf-8")

    # 보고서의 테이블은 값 확인·행 추적을 위한 원장 요약이다.
    chunks = []
    tables = []
    def prose(text):
        chunks.append({"kind": "prose", "id": f"audit-prose-{len(chunks):03}", "text": text.strip()})
    def table(title, headers, rows):
        ident = f"audit-table-{len(tables):02}"
        query_id = ident.replace("-", "_")
        columns = [{"key": f"c{i}", "label": h} for i, h in enumerate(headers)]
        records = [{f"c{i}": str(v) for i, v in enumerate(row)} for row in rows]
        item = {"kind": "table", "id": ident, "queryId": query_id, "title": title, "columns": columns, "rows": records}
        chunks.append(item)
        tables.append(item)

    prose(f"""## Executive Summary · 핵심 판단

현재 분류는 **동명이인·관용구를 걸러 낸 연구 초안으로 유용하지만, 누락 없는 전수 분류나 일관된 시장 호재·악재 라벨로 확정하기에는 부족하다.** 원본 26,239행을 자동으로 전수 대조하고 기존 분류 1,246행과 추가 후보 437행의 본문을 개별 열람한 결과, 현행 범주와 대조해 추가 분류가 필요한 글을 **{len(confirmed)}건** 특정했다. ‘trade wars’ 복수형, ‘trade deals’ 복수형, KORUS, 회사명 사전 밖 기업 등이 주요 누락 경로이다. 이는 확정된 정책사건 수나 전체 누락률이 아니라 **본문상 포함 검토가 필요한 최소 확인 목록**이다.

기존 분류에서는 **{int(flagged.sum())}건**에 범주 수정, 부호 재설계, 스레드·링크 보완 또는 범위 일관성 검토를 제안했다. 이 숫자는 오분류 확정 건수나 오류율이 아니다. 동명이인·관용구 경보 48건의 기존 Noise 판정은 본문상 타당했다. 가장 큰 해석 문제는 **무역갈등 방향, 국내 산업 수혜, 연준 비판의 어조, 경제 성과 홍보를 같은 Positive/Negative 축에 섞었다는 점**이다.

시각 검증에서는 원본 **311건**, 기존 분류 **19건**의 `date_utc`가 Snowflake 생성 시각과 약 12시간 어긋났다. 실제 NYSE 폐장시각까지 반영하면 기존 분류 **2건**의 거래일 수정이 필요하다. 반면 현재 라벨·저장된 날짜를 그대로 이용한 25개 일별 집계열은 1,007일 모두 일치했다. **내부 집계가 맞는 것과 원문 분류·사건 시각이 맞는 것은 별개**다.

권고는 기존 원본을 보존하고, 분류 기준을 다축으로 재설계한 별도 버전을 만든 뒤 누락·시각·신규성을 함께 정리하는 것이다. 이 감사에서는 라벨이나 시장 데이터를 덮어쓰지 않았고, 수정 전후 시장효과를 새로 확정하지 않았다.""")

    prose("""## 1. ‘전수조사’의 범위와 판단 단위

감사 모집단은 프로젝트에 저장된 트럼프 1기 아카이브 26,239행이다. 리트윗도 포함한다. ‘원글’이라는 표현은 데이터에 보존된 본문을 뜻하며, 트럼프 본인이 새로 쓴 글만을 의미하지 않는다. 본인 작성 글만을 분석할 경우 RT 포함 연구와 별도로 모집단을 다시 정의해야 한다.

**전수 완료 범위:** 모든 행의 원문·작성시각·식별자·기존 분류 포함 여부·확장 테마 경보·RT/단편 여부를 자동 검사했다. 분류된 1,246행은 본문 전체를 열람했고, 기존 분류 밖 437개 추가 후보도 본문을 열람해 확인 목록을 작성했다. 라벨은 검토 제안이며 복수 독립 평가자가 만든 정답지가 아니다.

**완료하지 않은 범위:** 무경보 23,698행과 거시·재정 범위만 검출된 858행, 합계 24,556행은 개별 의미 판독을 끝내지 않았다. 연결된 기사·인용글·이미지·영상·전체 RT 원문의 전수 복원도 실시하지 않았다. 따라서 ‘26,239개 원글을 모두 의미 판독했고 누락이 더 없다’는 결론을 내릴 수 없다. 이 제한은 특히 키워드가 전혀 없는 후속 스레드와 링크·영상만 있는 글에서 중요하다.

본문의 C번호는 `tweet_idx`(0부터 시작), R번호는 원본 CSV 데이터 행의 0기반 위치다. CSV 물리적 줄 번호는 본문 줄바꿈 때문에 다를 수 있다. 연결키는 날짜+정규화 본문의 SHA-256이며 손상된 ID에 의존하지 않는다. 검토에 시장 수익률이나 사후 VIX 급등 여부를 사용하지 않았다.""")
    table("감사 범위와 확인 결과", ["점검", "범위·결과", "해석"], [
        ["전체 원문", "26,239행", "자동 전수 점검; 모두 개별 의미 판독한 것은 아님"],
        ["기존 분류", "1,246행 / 원문 대조 불일치 0", "357 Positive + 421 Negative + 468 Noise"],
        ["확장 테마 추가 후보", "437행", f"그중 {len(confirmed)}행 추가 분류 필요; 나머지는 소음·보류·범위 후보"],
        ["거시·재정만 검출", "858행", "정책 모집단 확대 여부 결정 후 개별 판독 필요"],
        ["확장 규칙 무경보", "23,698행", "무경보가 정책 관련 글 부재를 보증하지 않음"],
        ["시장 자료", "1,007일 × 120열", "NYSE 거래일 누락·추가 0; 원본 열 보존"],
        ["집계 연결", "25열 × 1,007일 = 25,175셀, 불일치 0", "현재 라벨·저장된 매핑을 재현한 결과"],
        ["의미 검토 유지/추가 점검", f"유지 {int((~flagged).sum())} / 추가 점검 {int(flagged.sum())}", "정확도 산출용 독립 정답 판정이 아님"],
    ])

    prose("""## 2. 누락은 존재하며, 검색 범위를 넓히는 것만으로 해결되지는 않는다

기존 `audit_trade_tweets.py`는 `trade war`, `trade deal`을 단어 경계로 검색한다. 이 설정은 `trade wars`, `trade deals`의 끝 경계와 맞지 않아 다른 키워드가 없으면 글을 놓친다. KORUS, WTO, 무역 관련 일반 `trade`, President Xi의 축약형, GM·Ford·Harley·TikTok·Amazon 등도 기존 1차 사전에 충분히 들어 있지 않다. 반면 최종 분류에는 GM·Google·Qualcomm·Harley 등 사전 밖 기업을 이미 포함한 사례가 있어, 최종 분류 범위와 후보 추출 범위가 어긋난다.

누락 후보 437건을 그대로 누락 확정치로 보고하지 않았다. 확대 검색에서는 World Trade Center, Witness Trade, drug trade, duties(직무), GM(교통기관 general manager), Ford(항공모함·인명·병원), Amazon(열대우림), phase one(건강검진·백신 임상)이 새 오탐으로 들어온다. 이 가운데 20건을 명확한 제외 예시로 원장에 기록했다.

누락의 의미도 구분해야 한다. 원본에 존재하지만 분류 파일에 없는 **후보 선택 누락**, 아카이브 자체에 빠진 **수집 누락**, 정책 문맥은 있지만 신호·방향을 정하기 어려운 **판정 보류**는 서로 다르다. 아래 목록은 첫 번째 문제를 확인한 것이며, 연결 매체와 신규성 검토까지 마친 사건 정답지는 아니다.""")
    selected_omissions = [18710,18565,16605,16920,23057,17703,10866,8886,3829,4806,7436,13537,23404]
    omission_titles = {
        18710: "복수형 trade wars 때문에 빠진 대표적 보호무역 수사",
        18565: "한미 FTA(KORUS) 합의 발표 누락",
        16605: "한미 FTA 서명식 공지 누락",
        16920: "캐나다 협상 미타결이라는 악재 누락",
        23057: "WTO 시정조치 지시 누락",
        17703: "Harley 이전 시 과세 위협 누락",
        10866: "GM·Ford에 대한 인공호흡기 생산 요구 누락",
        8886: "Amazon 배송료 인상 요구 누락",
        3829: "TikTok 행정명령 RT 누락",
        4806: "코로나 여행제한의 무역 적용 배제 정정 누락",
        7436: "캐나다 국경폐쇄와 상품무역을 구분한 글 누락",
        13537: "Broadcom 미국 투자·생산 관련 발표 누락",
        23404: "Facebook Libra 규제 문맥 누락",
    }
    def evidence(row, prefix):
        text = re.sub(r"\s+", " ", str(row["text"])).strip()
        ref = row.get("reference_url")
        score = row.get("text_similarity", 0)
        link = f" [독립 아카이브의 원글 링크]({ref})" if isinstance(ref, str) and ref.startswith("https://") and score >= .65 else " 원글 링크는 정확한 ID 복원이 확인되지 않아 생략했다."
        return f"**추적:** {prefix} · 저장 UTC {row['date_utc']} · 원문+시각 연결키 `{row['audit_key']}`.{link}\n\n> {text}\n\n"
    for rid in selected_omissions:
        row = confirmed_df[confirmed_df.raw_row.eq(rid)].iloc[0]
        prose(f"### R{rid}. {omission_titles[rid]}\n\n" + evidence(row, f"R{rid}") + f"**판정:** {row.proposed_themes} / {row.proposed_direction}. {row.review_reason_ko}")

    prose("""## 3. 동명이인·관용구는 대체로 잘 제거되어 있다

48개 명시적 동명이인·관용구 경보는 모두 현재 Noise이며, 본문 검토상 유지가 적절하다. Sidney Powell·Colin Powell·Dina Powell을 Jerome Powell로 오인하거나, Shawn Steel을 철강산업으로 연결한 흔적은 이 경보군에서 찾지 못했다. `fed up`, `being fed`, `apple cart`, `man of steel`, 국경의 steel slats/barrier도 실제 정책 테마와 구분되어 있다. 경보 규칙이 모든 동음이의어를 포괄한다는 뜻은 아니다.

이 결과는 1차 키워드 사전의 오탐이 최종 문맥 분류에서 상당 부분 교정됐다는 근거다. 다만 기존 `Trade_Tweet_Dummy`, `Fed_Tweet_Dummy`는 원래 키워드 기준을 그대로 보존하므로, 최종 Noise가 기존 더미 분석에서 자동으로 제외된 것은 아니다. 두 종류의 분석을 발표에서 혼용하면 안 된다.""")
    for cid, title in [(29, "Shawn Steel은 사람 이름"), (494, "Sidney Powell은 Flynn의 변호사"), (1053, "Colin Powell은 연준 의장이 아님"), (146, "apple cart는 관용구"), (208, "man of steel은 골퍼 묘사"), (300, "steel slats는 국경 구조물")]:
        row = existing[existing.tweet_idx.eq(cid)].iloc[0]
        prose(f"### C{cid}. {title}\n\n" + evidence(row, f"C{cid}, R{row.raw_row}") + "**판정:** 현재 Noise 유지. 본문의 고유명사·관용적 의미를 우선하고 키워드 일치 자체를 경제정책 신호로 취급하지 않는다.")

    prose(f"""## 4. 긍정·부정의 가장 큰 문제는 ‘무엇에 대한 방향인가’가 섞였다는 점이다

기존 라벨 357 Positive·421 Negative·468 Noise 가운데 추가 점검 대상으로 특정한 글은 각각 **{pcount}·{ncount}·{zcount}건**이다. 검토 이슈는 범주 불일치, 정의 문제, 혼합 신호, 본문 부족, 낮은 신규성을 포함하며 전부 오류는 아니다. 유지로 남긴 글도 완전한 정확성을 보증하지 않는다.

현재 정의는 ‘정책 불확실성 완화/고조’와 ‘미국 산업 성장’, ‘발화의 비난 어조’를 결합한다. 그 결과 관세가 철강업을 살렸다는 유사한 문장이 어떤 날은 Positive, 어떤 날은 Negative가 된다. 연준 금리 인하 요구는 Fed에 대한 비판일 수 있으나 주식·채권·달러에 동일한 부호를 갖는 악재라고 미리 정할 수 없다. 사후 주가 등락으로 라벨을 정하는 방법 역시 결과변수에 의한 선택 편향을 만든다.

권고하는 방향은 Positive/Negative를 기계적으로 뒤집는 것이 아니다. **테마, 정책 갈등 방향, 통화정책 방향, 개별 자산 노출, 발표 강도, 신규성, 불확실성**을 분리해야 한다. ‘Noise’도 ‘어떤 시장에도 영향 없음’이 아니라 ‘이번 연구의 사전 정의 밖이거나 관련 정보 부족’으로 정의하는 편이 정확하다.""")
    table("세부유형별 기존 건수와 추가 점검 건수", ["기존 세부유형", "전체", "추가 점검", "주의"], [
        [subtype, len(g), int((~g.review_disposition.eq("본문 검토상 유지(잠정)")).sum()), "정의·범주·문맥 이슈를 포함; 오류율 아님"]
        for subtype, g in existing.groupby("context_sub_type", sort=True)
    ])
    case_ids = [499,519,355,497,1234,330,199,145,55,598,770,273,1006,530,568,458,824,794,1077,1236,1233,370]
    case_titles = {
        499: "Michael Steel 인용과 거시 낙관론: 회사·산업 키워드가 아님",
        519: "농민 지지율은 농산물 구매·농가 지원이 아님",
        355: "연준 인선을 산업 호재로 처리한 비대칭",
        497: "ECB 금리 인하 전망을 Fed 공격으로 분류",
        1234: "1832년 Andrew Jackson의 중앙은행 대립",
        330: "관세의 철강산업 수혜를 Positive로 판정한 사례",
        199: "관세의 철강산업 수혜를 Negative로 판정한 유사 사례",
        145: "ZTE 제재 조건과 영업재개 완화가 함께 있는 글",
        55: "중국과의 관계 덕담을 무역합의 진전으로 분류",
        598: "홍콩 시위 해결 제안을 무역합의 진전으로 분류",
        770: "Powell과의 회동을 무역합의 진전으로 분류",
        273: "#USMCA와 링크만 있는 글",
        1006: "코로나 비난을 하드 관세 위협으로 분류",
        530: "농산물 구매 실망과 직접 관세 선포의 차이",
        568: "낙관적인 후속 문장이 하드 관세 악재가 된 사례",
        458: "관세가 제거될 조건을 적은 후속 문장",
        824: "Fake News 표현이 있어도 실제 관세 보도 부인일 수 있음",
        794: "USMCA 붕괴 가능성을 Noise로 제외한 애매한 사례",
        1077: "방역·사망률 찬사를 산업 호재로 처리",
        1236: "백신 보급 성과를 산업 호재로 처리하고 조기폐장도 놓침",
        1233: "직접 재정 지급 요구를 Noise로 처리",
        370: "보잉 개선 조언과 강제정책·제재의 경계",
    }
    for cid in case_ids:
        row = existing[existing.tweet_idx.eq(cid)].iloc[0]
        rationale = row.review_reason_ko
        if cid == 499:
            rationale = "인용자의 성이 Steel이며 철강산업 발언이 아니다. 본문은 일반적인 고용·성장 평가이므로 광의의 Macro_Commentary로 보존할 수는 있다. 그러나 이 글을 포함하려면 회사명·산업 키워드가 없는 동일한 경기 낙관론도 같은 모집단에서 추출해야 한다. 따라서 동명이인만으로 Noise 확정하지 않고 범위 선택 편향을 지적한다."
        prose(f"### C{cid}. {case_titles[cid]}\n\n" + evidence(row, f"C{cid}, R{row.raw_row}") + f"**기존:** {row.context_signal} / `{row.context_sub_type}`.\n\n**검토:** {rationale}")

    prose("""## 5. 스레드·리트윗·정보 강도를 별도 관리해야 한다

기존 분류 1,246행 중 RT 표시 또는 RT 접두어가 있는 글은 268행이다. 원본 전체에는 9,787행이 있다. RT는 트럼프가 다시 배포한 정보라는 의미가 있지만, 본인이 새 조치를 발표한 글과 동일한 정보 충격으로 간주할 수 없다. 원문 작성시각과 트럼프의 재전달시각을 둘 다 보존하고, 동일 정책사건에 `event_id`를 부여해 최초 공개와 반복 노출을 구분해야 한다.

529행은 본문의 앞 또는 끝에 `...`/`…`가 있다. 이는 **단편·생략 가능성 경보**이며 529개 모두 데이터가 잘렸다는 뜻은 아니다. 작성자가 이어 쓴 스레드, RT의 표시 길이 제한, 의도적인 말줄임이 섞여 있다. C567의 신규 관세 조치와 C568의 낙관적 후속 글을 하나의 사건으로 연결할 수 있지만, 서로의 단독 문장 부호까지 같아야 하는 것은 아니다.

정확한 반복 본문은 추가 19행이며 동일 본문에 신호나 세부유형이 다르게 붙은 사례는 없었다. 그렇더라도 문구를 조금 고친 재게시·RT·하루 사이의 사건 중첩은 남는다. 단순 개수 차이의 Net Signal은 같은 정책을 길게 나눠 쓴 사람이 더 강한 충격을 준 것처럼 보이게 할 수 있다.

스레드 복원에는 시간 제약이 필요하다. 뒤에 게시된 글을 이용해 앞선 시점의 정보집합을 완성하면 사후 정보가 섞인다. 최초로 조치가 확인되는 시각에서 사건을 발생시키고, 후속 글은 추가 정보로만 집계해야 한다. 날짜를 먼저 고친 뒤 가까운 시각의 스레드를 연결해야 12시간 오류 때문에 엉뚱한 글을 연결하는 문제도 줄일 수 있다.

아카이브의 최종 retweet/favorite 수는 발표 시점에 알려진 값이 아니다. 동시점 수집 이력이 없다면 설명용 인기도 지표로만 사용하고, 충격 표본 선정·사전 강도·포트폴리오 신호에는 사용하지 않아야 한다. VIX나 사후 수익률이 크게 움직인 날만 ‘진짜 충격’으로 선별하는 방식도 피해야 한다.""")

    prose(f"""## 6. 시각과 거래일: 현재 집계는 재현되지만 원천 오류가 남아 있다

### 6.1 손상된 식별자와 원본 수집 범위

26,239개 ID가 모두 끝 두 자리 `00`으로 저장되어 있고, 서로 다른 두 RT가 같은 ID·같은 초를 갖는다. 작성시각+본문 조합의 중복은 0개이다. 64비트 Snowflake는 문자열로 보관해야 한다는 [X 공식 문서](https://docs.x.com/fundamentals/x-ids)와도 부합하는 문제다. 다만 각 ID의 원래 하위 자릿수는 이 파일만으로 복구할 수 없으므로 기존 숫자를 그대로 X 링크로 조립하지 않았다.

프로젝트의 [기존 공개 원본 JSON](https://github.com/ttzztztz/TrumpTwitterArchive)을 다시 내려받아 기간을 동일하게 제한했을 때, 로컬과 날짜+본문의 다중집합이 **26,239행 전부 일치**했다. 이는 로컬 추출이 해당 원본을 빠뜨리지 않았다는 뜻이며, 그 원본이 실제 트윗 전체를 완전히 보존했다는 독립 증명은 아니다. ID·시각 오류도 상위 원본에 이미 존재한다.

[별도 아카이브](https://github.com/MarkHershey/CompleteTrumpTweetsArchive)의 23,075행(고유 URL 23,065개)과 추가 대조하여 ID 근접 후보 **23,050행**의 교차키를 만들었다. 본문 유사도 0.8 이상은 **19,204행**이다. 나머지는 RT 길이·문자 인코딩·반복 문장 등이 달라 잠정 링크로만 보존한다. 별도 아카이브에서 근접 ID로 연결되지 않은 15행은 수집 범위·삭제·잘림 차이가 있는 미해결 대조 항목이며 곧바로 15개 누락 확정으로 세지 않았다. 두 아카이브는 같은 Twitter Archive 계열 자료일 수 있으므로 완전히 독립된 정답 자료라고 가정하지 않았다.

관측된 최종 게시일은 2021-01-08이다. 별도 아카이브도 같은 날의 계정 정지를 설명한다. 따라서 1월 20일까지 매일 트윗이 있어야 한다고 판단하면 안 된다. 반대로 UTC 자정부터 재임기간을 잡아 취임식(2017-01-20 17:00 UTC) 이전 글 3개를 포함한 경계는 연구 모집단 정의에 명시해야 한다.

### 6.2 12시간 어긋난 시각은 원천 파싱 문제를 시사한다

생성시각은 `((int(id) >> 22) + 1288834974657)` 밀리초로 재구성했다. 비트 배치와 epoch는 [Twitter의 원 구현](https://raw.githubusercontent.com/twitter-archive/snowflake/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala)에서 확인했다. 하위 ID 반올림 손상은 초 경계 주변의 밀리초 오차를 만들 수 있지만 12시간 차이를 설명하지 못한다. 그래서 2초 초과를 충돌 기준으로 사용했다.

원본 311행은 약 ±43,200초 차이가 나며, 기존 분류 안에는 19행이 있다. AM/PM 혼동과 일치하는 패턴이지만 당시 수집·변환 로그가 없어 **구체적인 발생 원인은 가설**로 남긴다. 원본 전체를 16시 기준으로 다시 매핑하면 **{raw_mapping_changes}행**의 거래일이 달라진다. 기존 분류에서는 아래 C466 한 행이 해당한다. 원본 전체의 거래일 변경에는 기존 분류 밖 글도 포함되므로, 19개 분류 시각 오류가 모두 이벤트일을 바꿨다고 표현하면 안 된다.

### 6.3 고정 16시 규칙과 실제 조기폐장을 구분

저장된 `date_utc`를 신뢰하면 1,246건 모두 프로젝트의 고정 16시 규칙을 정확히 재현한다. 그러나 NYSE의 실제 폐장시각을 적용하면 C1236은 다음 거래일로 이동해야 한다. 2020-12-24 13시 조기폐장은 [NYSE/ICE 당시 공식 공지](https://ir.theice.com/press/news-details/2019/NYSE-Group-Announces-2020-2021-and-2022-Holiday-and-Early-Closings-Calendar/default.aspx)와 대조했다. 시각 오류와 조기폐장을 함께 반영할 때 거래일 변경 대상은 총 2건이다.""")
    table("거래일 변경이 필요한 기존 분류", ["글", "저장 UTC", "검증 UTC·사유", "기존 거래일", "권고 거래일"], [
        ["C466 농가 재난지원법", "2019-06-03 11:58:38", "Snowflake 23:58:38 UTC → NY 19:58, 장 마감 후", "2019-06-03", "2019-06-04"],
        ["C1236 백신 보급", "2020-12-24 20:30:57", "NY 15:30; 당일 13시 조기폐장 이후", "2020-12-24", "2020-12-28"],
    ])
    prose("""C1236은 분류 자체도 산업정책 호재로 보기 어려우므로, 향후 수정에서는 ‘날짜 이동’과 ‘분석 범위 제외/보건 테마 분리’를 따로 기록해야 한다. 현재 자료에서 매핑된 2행은 모두 Positive지만 실제 수정 후 신호일 수의 변화는 다른 글과의 동시 발생 여부에 따라 달라진다.

### 6.4 25개 집계열의 일치는 라벨의 타당성을 보장하지 않는다

원문 분류에서 Trade/Fed/Policy/Hard Tariff/Deal 관련 Count·Dummy·Pure Dummy·Net Signal·Retweet Sum을 독립 재집계했으며 25,175셀의 차이는 0이었다. 시장자료의 1,007개 거래일도 NYSE 일정과 일치한다. 반면 기존 라벨에서 발견한 범주·부호·누락 문제는 그대로 집계에 전달된다.

추가로 Policy Pure Positive 137일 중 13일에는 Fed_Neg_Dummy도 1이다. Policy Pure Negative 113일 중 14일도 Fed 공격과 겹친다. 이는 ‘순수’가 **모든 정책 테마를 통틀어 호재만/악재만 있다는 뜻이 아니라, 현재 Policy 정의 안에서 반대 신호가 없다는 뜻**임을 보여 준다. 연준과 무역을 별도 층으로 분석하고 교차 노출을 통제해야 한다. 특히 Powell과의 우호적 회동이 Policy Positive에 포함되고 Fed 공격은 Policy Negative에서 제외되는 비대칭은 먼저 해소할 필요가 있다.""")

    prose("""## 7. 기존 시장효과 해석에서 유지할 것과 다시 검증할 것

이 감사는 분류·연결 품질 검토이며 새 시장효과 추정이 아니다. 앞선 결과의 p값을 그대로 재인용해 수정된 라벨에서도 결론이 유지된다고 주장하지 않았다. S&P 500의 비유의는 ‘효과 없음’이나 ‘산업 간 상쇄가 입증됨’과 같지 않다. 표본 선택·신호 정의·산업별 차이·시각 오차가 정리된 후 다시 비교해야 한다.

`empirical_context_sentiment.py`는 2·3일 복리수익률에서 전체 표본의 평균 복리수익률을 빼서 CAR라고 부른다. 고정 평균을 빼는 것은 같은 기간의 두 집단 평균차에는 영향을 주지 않지만, 사건별 기대수익률 모형에 기반한 표준적인 비정상수익률과는 다르다. 발표에서는 ‘전체 표본 평균을 차감한 누적수익률’로 명시하거나, 사건 전 추정구간으로 기대수익률을 추정하는 별도 모형을 사용해야 한다. 전체 표본 평균에는 사건 이후 정보가 들어가므로 실시간 전략 신호로 쓰지 않는다.

TNX_Return은 금리 수준의 상대적 변화율이다. TNX_Return의 집단 평균차가 −0.573%p라고 해서 10년물 금리가 57.3bp 떨어졌다는 뜻은 아니다. 금리 충격은 `100 × (TNX_Close[t] − TNX_Close[t−1])` bp로 별도 계산해야 한다. CNY=X와 다른 자산도 각자의 세션·가격 확정 시각을 확인해야 하며 미국 16시 일괄 매핑이 모든 글로벌 자산에 정확하다고 가정해서는 안 된다.

재추정 시에는 프로젝트 기준대로 T, T+1, CAR[0,+1], CAR[0,+2]를 모두 비교하고 Welch 검정(`equal_var=False`)을 유지한다. 신호가 연속한 날에는 누적 창이 겹치므로 관측 독립성 문제가 생긴다. 사건 클러스터 또는 시계열 블록을 반영한 추론을 보완하고, 다수 자산·기간·비교의 다중검정도 표시해야 한다. 부호와 표본을 시장 결과를 보고 조정하지 않는 것이 우선이다.""")

    prose("""## 8. 권고 분류체계와 수정 순서

하나의 글에 하나의 유형·부호만 강제하기보다, 독립적인 필드를 두는 것이 재현성과 금융 해석을 함께 개선한다. 기존 열은 보존하고 새 버전의 감사 열을 추가하는 방식이 적절하다.""")
    table("권고 분류 필드", ["필드", "허용값·설계", "목적"], [
        ["themes", "Trade / Fed / ECB / FX / Firm / Farm / Fiscal / Health / Geopolitics (다중 선택)", "복합 주제 강제 단일화 방지"],
        ["trade_stance", "Escalation / Deescalation / Mixed / Neutral / Uncertain / NA", "협상갈등 방향을 별도 기록"],
        ["monetary_stance", "Easing / Tightening / Neutral / Uncertain / NA", "Fed 비난 어조와 정책방향 분리"],
        ["action_stage", "Implemented / Announced / Conditional_Threat / Investigation / Talks / Advocacy / Commentary", "직접 조치와 수사·기대 구분"],
        ["novelty", "New / Update / Repeat / Retrospective / Unknown", "사후 홍보와 새 정보 구분"],
        ["asset_exposure", "수혜·피해 기업/산업을 텍스트 근거로 복수 기록", "시장 전체 단일 부호 강제 금지"],
        ["context_status", "Sufficient / Thread_Required / Link_Required / Media_Required", "본문 부족을 Noise와 분리"],
        ["speaker_type", "Trump_Original / Self_RT / Third_Party_RT / Quote", "최초 발언과 재배포 구분"],
        ["source_time_verified", "원시 문자열 + Snowflake + 검증 근거", "정확한 정보집합 시점 보존"],
        ["event_id / event_first_public_at", "동일 정책사건 묶음 / 최초 공개시각", "스레드·재게시 중복과 시점 편향 관리"],
        ["review_state", "Retain / Revise / Ambiguous / Context_Required / Out_Of_Scope", "미확정을 확정값으로 덮지 않음"],
    ])
    prose("""수정은 다음 순서로 진행하는 것이 타당하다.

1. 기존 세 파일의 체크섬을 고정하고, 원래 ID와 문자열 정밀 ID·감사용 복합키를 별도 보관한다. 생성시각과 충돌하는 311행 및 조기폐장일의 매핑부터 정리한다.
2. 기존 연구의 범위를 무역·연준 중심으로 둘지, 기업·거시·재정·보건까지 포함할지 명시한다. 연구 범위를 넓히면 거시·재정 후보 858건뿐 아니라 키워드 없는 글도 포함한 전체 텍스트 분류가 필요하다.
3. 추가 분류 필요 목록과 기존 수정 권고를 다축 체계로 재코딩한다. 애매한 글은 Uncertain/Context_Required로 남기고, 독립 평가자 2인이 같은 코드북으로 판단한 뒤 불일치를 조정한다. 현재 감사만으로 평가자 간 일치도·정확도를 산출하지 않는다.
4. 같은 정책의 반복 게시와 스레드를 사건 단위로 연결하되 최초 공개시각을 보존한다. 최종 RT 수·VIX·수익률을 사건 선정 기준으로 쓰지 않는다.
5. 1,007일의 기존 열을 보존한 파생 데이터에 재집계하고, 동일 표본·기간·단위를 유지해 T/T+1/2일/3일 반응과 표본수 변화를 함께 보고한다. 재추정 전에는 기존 발표 결론을 강화하는 근거로 이 감사를 사용하지 않는다.""")

    prose("""## 9. 재현 방법과 산출물

저장소 루트에서 `python scripts/audit_tweet_archive_sources.py`로 저장된 공개 참조 사본과의 교차키를 재현하고, `python scripts/audit_context_classification.py`를 실행하면 원본·분류·시장의 자동 감사 CSV와 JSON이 생성된다. 그 뒤 `python scripts/build_tweet_audit_report.py`를 실행하면 명시적 검토 결정과 연결한 원장 및 이 보고서가 생성된다. 참조 사본이 없을 때만 첫 스크립트에 `--download-missing`을 지정해 공개 URL에서 받는다. NYSE 일정 검증에는 requirements에 명시한 `pandas_market_calendars`를 사용한다. 난수 시드는 42이며 표본 추출은 하지 않았다.

검토 결정은 `review_decisions.json`에 기록되어 있고, 원문 1,246건을 검토했다는 서술은 이 작업의 실제 열람 기록을 뜻한다. 재실행 스크립트가 의미 판독을 다시 수행하는 것은 아니다. 기존 판정 근거를 데이터에 연결해 재현할 뿐이다. 원본 스냅샷이나 결정 파일이 바뀌면 보고서의 버전과 수치를 함께 갱신해야 한다.

공개 원본과 별도 아카이브는 이 폴더에 참조용 사본을 저장했다. 다운받은 시점의 파일 해시를 manifest에 보관했으며, 정밀 ID 교차키는 근접 ID와 본문 유사도에 기초한 잠정 연결이다. 링크 열람 성공이나 26,239건의 정확한 ID 복원을 주장하지 않는다. 기사·영상·보호된 데이터에 대한 접근을 우회하지 않았다.""")
    table("검토 근거 파일", ["파일", "내용"], [
        ["full_corpus_review_coverage.csv", "26,239행 전수 스크리닝과 개별 의미 열람 여부"],
        ["existing_review_ledger.csv", "1,246행 기존 라벨·제안·이유·원문·시각 검증"],
        ["omission_review_ledger.csv", "437행 확대 후보, 포함 필요·제외 예시·보류 구분"],
        ["confirmed_scope_omissions.csv", f"추가 분류가 필요한 {len(confirmed)}행 최소 확인 목록"],
        ["raw_timestamp_audit.csv", "모든 원문 시각과 Snowflake 차이, 311행 경보"],
        ["trading_date_audit.csv", "고정 16시·실제 NYSE 폐장·Snowflake별 매핑 비교"],
        ["daily_aggregation_mismatches.csv", "현재 라벨을 재집계한 25열 불일치 목록(0행)"],
        ["exact_id_crosswalk.csv", "별도 아카이브와의 근접 ID·본문 유사도·URL 대조"],
        ["audit_summary.json / review_summary.json", "자동 및 개별 검토의 집계값"],
        ["review_decisions.json", "명시적 범주 수정·애매 사례·추가 분류 필요 결정"],
        ["source_manifest.json", "입력·외부 참조의 SHA-256 및 출처"],
    ])
    prose("""## 10. 출처와 증거 한계

**[S1] 로컬 원문** `data/trump_tweets_1st_term_raw.csv`. 저장된 게시시각 기준 2017-01-20~2021-01-08, 26,239행. 입력 원문을 그대로 보존했다.

**[S2] 기존 문맥 분류** `data/trump_policy_tweets_context_classified.csv`, 1,246행. 기존 신호·세부유형·한국어 근거는 감사 대상이지 독립 정답이 아니다. 본문의 모든 트윗 인용은 사용자가 제공한 로컬 원문에서 가져왔다.

**[S3] 시장 자료와 생성 코드** `data/trump_market_extended_data.csv`, `scripts/audit_trade_tweets.py`, `scripts/empirical_context_sentiment.py`, `scripts/pipeline_extended.py`. 현재 집계·후보 선택·CAR 정의를 확인했다. 시장 가격을 새로 내려받거나 원자료의 가격 정확성까지 감사하지 않았다.

**[S4] 기존 수집 원본** [ttzztztz/TrumpTwitterArchive](https://github.com/ttzztztz/TrumpTwitterArchive). 공개 JSON을 내려받아 기간 제한 후 날짜·본문 다중집합을 로컬과 대조했다. 상위 원본과의 동일성만 확인한 것이며, 공통 오류까지 제거되는 것은 아니다.

**[S5] 보조 아카이브** [MarkHershey/CompleteTrumpTweetsArchive](https://github.com/MarkHershey/CompleteTrumpTweetsArchive). 공개 CSV의 문자열 URL 및 본문으로 ID 교차키를 작성했다. 인코딩·잘림·중복·수집 범위가 달라 독립 정답으로 간주하지 않았다.

**[S6] X 식별자 문서 및 Twitter 원 구현** [X IDs](https://docs.x.com/fundamentals/x-ids), [IdWorker.scala](https://raw.githubusercontent.com/twitter-archive/snowflake/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala). ID의 정밀 보관 원칙과 생성시각 계산식을 검증했다.

**[S7] 거래소 일정** [NYSE/ICE 2020~2022 휴장·조기폐장 공지](https://ir.theice.com/press/news-details/2019/NYSE-Group-Announces-2020-2021-and-2022-Holiday-and-Early-Closings-Calendar/default.aspx), [NYSE 정규 거래시간](https://www.nyse.com/trade/hours-calendars). 2020-12-24 조기폐장 사례와 정규 16시 마감을 확인했다. 전체 일정 재계산에는 설치된 NYSE 캘린더 패키지를 사용했으며 모든 과거 날짜를 별도 공식 공지와 하나씩 대조한 것은 아니다.

**감사일:** 2026-11-02, Asia/Seoul. 현재 보고서의 완성은 정해진 감사 범위의 결과를 문서화했다는 의미다. 원글 전량의 의미 판정, 모든 매체 복원, 수정 라벨 확정, 수정 후 시장효과 검증이 모두 완료됐다는 뜻은 아니다.""")

    # Markdown은 저장소 검토용 원문, HTML은 동일 내용을 공유 컴포넌트로 제공한다.
    md = ["# 트럼프 트윗 분류·누락 감사 보고서\n\nGAM 팀프로젝트 · 감사일 2026-11-02 · 원본 보존 검토\n"]
    for chunk in chunks:
        if chunk["kind"] == "prose":
            md.append(chunk["text"])
        else:
            esc = lambda v: str(v).replace("|", "\\|").replace("\n", " ")
            md.append("### " + chunk["title"] + "\n\n| " + " | ".join(c["label"] for c in chunk["columns"]) + " |\n| " + " | ".join("---" for _ in chunk["columns"]) + " |\n" + "\n".join("| " + " | ".join(esc(r[c["key"]]) for c in chunk["columns"]) + " |" for r in chunk["rows"]))
    (OUT / "REPORT.md").write_text("\n\n".join(md) + "\n", encoding="utf-8")

    app = OUT / "report_app"
    snapshot_path = app / "src/data.json"
    if app.exists():
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        snapshot["title"] = "트럼프 트윗 분류·누락 감사 보고서"
        snapshot["buildStatus"] = "complete"
        snapshot["report"] = {"asOf": "2026-11-02"}
        for t in tables:
            snapshot["queries"][t["queryId"]] = {"rows": t["rows"], "source": {"label": t["title"], "files": ["docs/tweet_audit_2026-11-02/audit_summary.json", "docs/tweet_audit_2026-11-02/review_summary.json", "docs/tweet_audit_2026-11-02/review_decisions.json"], "description": "원문 대조·검토 원장에서 작성한 감사 결과. 분류 정확도나 누락률의 추정치가 아님.", "methodology": "scripts/audit_context_classification.py + 명시적 review_decisions.json + scripts/build_tweet_audit_report.py", "caveats": [decisions["coverage_note"]]}}
        snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
        (app / "src/content/report/audit-content.json").write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
    source_paths = list(summary["source_files"].values())
    external = []
    for filename, url in [("archive_reference.json", "https://raw.githubusercontent.com/ttzztztz/TrumpTwitterArchive/master/trump.json"), ("independent_archive_reference.csv", "https://raw.githubusercontent.com/MarkHershey/CompleteTrumpTweetsArchive/master/data/realDonaldTrump_in_office.csv")]:
        path = OUT / filename
        external.append({"file": filename, "url": url, "retrieved_date": "2026-11-02", "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest = {"audit_date": "2026-11-02", "input_files": source_paths, "external_snapshots": external, "review_decisions_sha256": hashlib.sha256((OUT / "review_decisions.json").read_bytes()).hexdigest(), "review_summary": extra, "coverage_note": decisions["coverage_note"]}
    (OUT / "source_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(extra, ensure_ascii=False, indent=2))
    print(f"Report: {OUT / 'REPORT.md'} ({len(chunks)} content blocks)")


if __name__ == "__main__":
    main()
