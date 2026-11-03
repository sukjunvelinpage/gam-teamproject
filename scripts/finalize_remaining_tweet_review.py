"""실제 개별 검토 원장 24,556행이 모두 있을 때만 2차 보고서를 갱신한다.

검토 자체를 자동 수행하지 않는다. 누락·중복·불명확 근거가 있으면 저장 전에 실패한다.
"""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/tweet_audit_2026-11-02'
WORK = OUT / 'remaining_review'


def main():
    expected = pd.concat([pd.read_csv(WORK / f'part_{i}.csv', dtype={'id':str}) for i in range(4)], ignore_index=True)
    filenames = ['part_0_decisions.jsonl','part_0_tail_a_decisions.jsonl','part_0_tail_b_decisions.jsonl','part_1_decisions.jsonl','part_2_decisions.jsonl','part_3_decisions.jsonl']
    records=[]
    for name in filenames:
        path=WORK/name
        if not path.exists():
            raise RuntimeError(f'개별 검토 미완료: {name} 없음')
        records.extend(json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip())
    review=pd.DataFrame(records)
    required={'raw_row','status','themes','direction','reason_ko','reviewer','batch_id'}
    assert required<=set(review.columns), '필수 판단근거 열 누락'
    assert len(expected)==24556 and len(review)==24556, f'검토 {len(review)}/24556'
    assert not review.raw_row.duplicated().any(), '중복 판단행'
    assert set(expected.raw_row)==set(review.raw_row), '미검토 또는 범위 밖 행'
    assert review.status.isin(['include_core','include_extended','exclude','needs_context']).all()
    assert review.reason_ko.fillna('').str.len().ge(10).all(), '근거 부족'
    assert review.reviewer.notna().all() and review.batch_id.notna().all()
    merged=expected[['raw_row','audit_key','id','date_utc','text']].merge(review,on='raw_row',validate='one_to_one').sort_values('raw_row')
    merged['themes']=merged.themes.map(lambda value:';'.join(value) if isinstance(value,list) else str(value))
    counts=merged.status.value_counts().to_dict()
    summary={'reviewed_rows':len(merged),'status_counts':counts,'input_parts':json.loads((WORK/'manifest.json').read_text(encoding='utf-8')),'reviewer_counts':merged.reviewer.value_counts().to_dict(),'method':'모든 담당 원문을 도구 출력으로 열람한 뒤 작성한 명시적 행별 판단 연결. 자동 규칙만으로 완료 처리하지 않음.','scope_limit':'본문 전체 개별 판독과 연결 매체 전수 복원은 별개. needs_context 행은 추가 누락을 배제할 수 없으며 별도 미해결 원장에 보존.'}
    # 저장된 1차 입력이 변경되지 않았는지 검사한다.
    first=json.loads((OUT/'audit_summary.json').read_text(encoding='utf-8'))
    for source in first['source_files'].values():
        assert hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256'], '원본 변경 감지'
    merged.to_csv(OUT/'remaining_individual_review_ledger.csv',index=False,encoding='utf-8-sig')
    coverage=pd.read_csv(OUT/'full_corpus_review_coverage.csv',dtype={'id':str})
    coverage=coverage.drop(columns=[c for c in ['second_review_status','second_review_reason_ko','second_review_reviewer'] if c in coverage])
    appendix=review[['raw_row','status','reason_ko','reviewer']].rename(columns={'status':'second_review_status','reason_ko':'second_review_reason_ko','reviewer':'second_review_reviewer'})
    coverage=coverage.merge(appendix,on='raw_row',how='left',validate='one_to_one')
    coverage.loc[coverage.second_review_status.notna(),'semantic_review_scope']='2차 본문 개별 열람 완료·연결 매체는 별도'
    assert len(coverage)==26239 and coverage.second_review_status.notna().sum()==24556
    coverage.to_csv(OUT/'full_corpus_review_coverage.csv',index=False,encoding='utf-8-sig')
    for status,name in [('include_core','additional_core_candidates.csv'),('include_extended','additional_extended_candidates.csv'),('needs_context','remaining_context_required.csv')]:
        merged[merged.status.eq(status)].to_csv(OUT/name,index=False,encoding='utf-8-sig')
    (OUT/'remaining_individual_review_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    report_path=OUT/'REPORT.md'
    baseline=OUT/'REPORT_first_audit_snapshot.md'
    if not baseline.exists(): baseline.write_bytes(report_path.read_bytes())
    first_text=baseline.read_text(encoding='utf-8')
    intro=f'''# 트럼프 트윗 분류·누락 감사 보고서 — 2차 개별 원문 검토

GAM 팀프로젝트 · 검토기간 2026-11-02~2026-11-03 · 원본 데이터 보존

## 2차 검토 결과와 범위

1차에서 개별 의미 판독이 남았던 **24,556건 전부**를 분담하여 본문별로 검토하고 행별 근거를 저장했다. 기존 1,246건 및 1차 추가 후보 437건과 합치면 로컬 모집단 26,239건의 본문을 개별 열람한 범위가 된다. 연결 기사·이미지·영상의 복원까지 모두 완료했다는 뜻은 아니다.

| 2차 판단 | 건수 | 의미 |
| --- | ---: | --- |
| 경제·기업 정책 추가 분류 후보 | {counts.get('include_core',0)} | 무역·통화·외환·농가·기업 정책 관련 본문 및 경계 사례. 신규성·정밀 범주와 이벤트 중복을 확인해야 함 |
| 넓은 경제정책 범위 후보 | {counts.get('include_extended',0)} | 재정·거시·에너지·보건 등. 기존 무역 연구에 자동 합산하지 않음 |
| 본문상 제외 | {counts.get('exclude',0)} | 정치·개인·행사 등으로 판단한 행; 근거는 개별 원장 참조 |
| 문맥 복원 필요 | {counts.get('needs_context',0)} | 링크·인용·생략으로 포함 여부나 부호 미확정. 누락 없음으로 처리하지 않음 |

이 수치는 1차의 추가 분류 필요 59건 및 기존 분류 재검토 152건과 별도 모집단의 결과다. 후보 글 수는 독립된 정책사건 수가 아니며, 재게시·스레드·RT가 포함된다. 시장 반응으로 부호를 정하지 않았고 원본 라벨·시장 자료를 수정하지 않았다.

`include_core`는 후속 분류에서 우선 검토할 경제정책 후보를 뜻한다. 원래의 무역·연준 표본에 모두 자동 편입할 확정 명단은 아니다. 제재·기술규제·기업계약 등 연구 범위의 경계 사례도 테마와 근거를 남겼다. `direction` 역시 사후 주가의 상승·하락이 아니라 본문상 완화·강화·지원·압박 방향의 잠정 판단이다. 소비자와 기업의 이해가 다르거나 대상·조건을 확정할 수 없으면 mixed/uncertain으로 기록했다.

분담 검토는 각 글을 서로 다른 담당자에게 배정한 방식이다. 모든 글에 대한 두 명의 독립 평가·합의를 수행한 것은 아니며, 평가자 간 일치도나 분류 정확도를 산출하지 않았다. 원장에는 판단 당시의 근거를 남겨 재검토할 수 있게 했다.

**해석:** 전량 본문 검토를 마쳤더라도 문맥 복원 필요 행이 있으므로 ‘정책 관련 누락이 더 없다’는 무조건적인 보증은 할 수 없다. 확인된 추가 후보를 분류 대상에 올리고, 미확정 글을 별도 추적하는 것이 감사 결과다.

## 새로 확인한 주요·애매 사례

'''
    cases=[]
    for name in ['part_0_cases.md','part_0_tail_a_cases.md','part_0_tail_b_cases.md','part_1_cases.md','part_2_cases.md','part_3_cases.md']:
        p=WORK/name
        if p.exists():
            case_text=p.read_text(encoding='utf-8')
            case_text=case_text.replace('아래는 완료된 행의 검토 근거이며 담당 전체의 완료를 의미하지 않는다.', '아래는 담당 원문 개별 검토에서 선정한 주요·애매 사례다.')
            cases.append(case_text)
    section='\n\n'.join(cases)
    if not section: raise RuntimeError('사례별 판단근거 문서 없음')
    evidence='''

## 2차 검토 근거와 재현

- `remaining_individual_review_ledger.csv`: 24,556행 원문·검토자·배치·판단·근거.
- `additional_core_candidates.csv`: 기존 범위의 추가 후보.
- `additional_extended_candidates.csv`: 범위 확장 여부를 결정할 글.
- `remaining_context_required.csv`: 연결 원문 복원이 필요한 미확정 글.
- `remaining_individual_review_summary.json`: 판단별 합계와 분담 범위.
- `remaining_review/*_decisions.jsonl`: 배치별 개별 판정 기록.

`python scripts/finalize_remaining_tweet_review.py`는 24,556행의 키·건수·범위·원본 체크섬을 검증한 후 이 보고서를 갱신한다. 의미 판독을 자동으로 재수행하는 스크립트가 아니다.

## 1차 감사 보존 기록

아래는 2차 검토 전 결과의 보존 기록이다. 아래의 ‘24,556행 미검토’라는 문구는 **1차 시점의 상태**이며 현재 상태는 위의 2차 검토표가 대체한다. 기존 분류 1,246건의 문제와 시각 오류·통계 해석에 관한 상세 근거는 계속 유효하다.

'''
    report_path.write_text(intro+section+evidence+first_text,encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
