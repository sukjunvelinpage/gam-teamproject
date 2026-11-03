"""Build a provisional, traceable corpus-level classification; preserve inputs."""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'docs/tweet_audit_2026-11-02'
OUT = ROOT / 'data/trump_policy_tweets_integrated_review.csv'

def read(path):
    return pd.read_csv(path, dtype=str, keep_default_na=False)

def join(base, frame, columns, prefix):
    assert frame.raw_row.is_unique
    cols = ['raw_row', 'audit_key'] + columns
    subset = frame[cols].rename(columns={c: prefix+c for c in columns})
    result = base.merge(subset, on=['raw_row','audit_key'], how='left', validate='one_to_one', indicator='_match')
    assert (result._match == 'both').sum() == len(subset)
    return result.drop(columns='_match').fillna('')

def main():
    coverage = read(AUDIT/'full_corpus_review_coverage.csv')
    a = read(AUDIT/'existing_review_ledger.csv')
    b = read(AUDIT/'omission_review_ledger.csv')
    c = read(AUDIT/'remaining_individual_review_ledger.csv')
    archive = read(AUDIT/'restoration/combined_restoration_ledger.csv')
    for t in [coverage,a,b,c,archive]: assert t.raw_row.is_unique
    assert len(coverage)==26239 and len(a)==1246 and len(b)==437 and len(c)==24556
    assert set(a.raw_row).isdisjoint(b.raw_row) and set(a.raw_row).isdisjoint(c.raw_row) and set(b.raw_row).isdisjoint(c.raw_row)
    assert set(a.raw_row)|set(b.raw_row)|set(c.raw_row)==set(coverage.raw_row)
    out = coverage[['raw_row','audit_key','id','date_utc','text','isRetweet','tweet_idx','mapped_trading_date']].copy()
    out = join(out,a,['context_signal','context_sub_type','context_reason_ko','review_disposition','review_issues','review_reason_ko','proposed_themes','proposed_direction','timestamp_conflict','snowflake_utc','snowflake_actual_close_expected','snowflake_actual_close_mismatch'], 'existing_')
    out = join(out,b,['review_disposition','proposed_themes','proposed_direction','review_reason_ko'], 'screened_')
    out = join(out,c,['status','themes','direction','reason_ko','reviewer','review_method'], 'additional_')
    out = join(out,archive,['restoration_status','archived_full_text','source_tweet_url','verified_proposed_status','verified_proposed_direction','verified_reason_ko','candidate_reference_text','candidate_reference_tweet_url','candidate_policy_relevance','candidate_proposed_direction','candidate_reasoning_ko','candidate_restoration_completeness'], 'restore_')
    out['source_group'] = 'additional_24556'
    out.loc[out.raw_row.isin(a.raw_row),'source_group'] = 'existing_1246'
    out.loc[out.raw_row.isin(b.raw_row),'source_group'] = 'screened_437'
    out['scope_status'] = 'review_required'
    out.loc[out.additional_status=='exclude','scope_status']='provisional_exclude'
    out.loc[out.additional_status=='needs_context','scope_status']='context_required'
    out.loc[out.additional_status.isin(['include_core','include_extended']),'scope_status']='candidate_needs_scope_review'
    out.loc[out.source_group=='existing_1246','scope_status']='existing_label_needs_scope_review'
    out.loc[out.screened_review_disposition.str.contains('오탐 확인',na=False),'scope_status']='provisional_exclude'
    out.loc[out.screened_review_disposition.str.contains('추가 분류 필요',na=False),'scope_status']='candidate_needs_scope_review'
    out['scope_basis'] = out.additional_reason_ko
    out.loc[out.source_group=='existing_1246','scope_basis'] = out.existing_review_reason_ko
    out.loc[out.source_group=='screened_437','scope_basis'] = out.screened_review_reason_ko
    out['topic_evidence'] = out.additional_themes
    out.loc[out.source_group=='existing_1246','topic_evidence'] = out.existing_proposed_themes.where(out.existing_proposed_themes.ne(''),out.existing_context_sub_type)
    out.loc[out.source_group=='screened_437','topic_evidence'] = out.screened_proposed_themes
    out['trade_conflict_direction'] = 'unresolved'
    out['direction_note'] = '기존 긍정·부정을 갈등 방향으로 자동 변환하지 않음'
    out['review_update'] = ''
    out.loc[out.raw_row=='14666',['scope_status','topic_evidence','scope_basis','review_update']] = ['candidate_needs_scope_review','Trade_Diplomacy','복원 본문은 한국과 미국 기업·노동자의 공정경쟁 여건을 언급하나 관세 변화를 명시하지 않음','확장 원문 대조; 추가 범위 판정 필요']
    out.loc[out.raw_row=='15263',['scope_status','topic_evidence','scope_basis','review_update']] = ['provisional_exclude','Political_Cabinet_Confirmation','복원 본문은 내각 인준 지연을 둘러싼 정치적 비판이며 경제정책 조치가 명시되지 않음','확장 원문 대조; 잠정 제외']
    cases = {
      '25890':('Trade_Protectionism;Industry','관세의 철강산업 효과를 자찬한 회고; 신규 관세 발표나 갈등 방향을 자동으로 확정하지 않음.'),
      '17252':('Trade_Protectionism;Industry','관세 효과 회고의 후속 단편; 산업 수혜 주장과 무역갈등 방향은 별개.'),
      '25291':('Monetary_Personnel','연준 인선 발표이므로 통화정책 관련 후보; 인선 자체로 완화·긴축이나 산업 호재를 확정할 수 없음.'),
      '23715':('ECB_Monetary_Commentary','ECB의 금리 전망 인용이며 미국 연준에 대한 공격으로 분류할 수 없음.'),
      '18106':('Company_Tech_Sanctions','ZTE 영업재개와 벌금·조건이 함께 있어 제재 방향을 하나로 단정하기 어려움.'),
      '13476':('Diplomatic_Courtesy','미중 관계 개선에 대한 덕담만으로 무역합의 진전 또는 정책 발표를 확정할 수 없음.'),
      '23622':('Campaign_Economic_Rhetoric','농민 지지율을 홍보한 글이며 농가 구매나 지원 조치를 직접 밝히지 않음.'),
      '60':('Trade_Brexit','브렉시트 관련 재게시물이지만 잘린 원문과 링크 확인 전 내용·신규성을 확정하지 않음.'),
      '4198':('Government_Contracts','정부계약 배제 제안의 대상 기업과 기술이 불명확하며 연결 자료 확인 필요.')}
    for raw,(topic,reason) in cases.items():
        mask=out.raw_row.eq(raw)
        assert mask.sum()==1
        out.loc[mask,['topic_evidence','scope_basis','review_update']] = [topic,reason,'연구 범위에 따른 추가 검토; 분류 확정 전 추가 확인']
        out.loc[mask,'scope_status'] = 'context_required' if raw in ['60','4198'] else 'candidate_needs_scope_review'
    sample_path = AUDIT/'generic_theme_manual_review_40.csv'
    if sample_path.exists():
        sample = read(sample_path)
        assert len(sample)==40 and sample.raw_row.is_unique
        status_map = {'include_candidate':'candidate_needs_scope_review', 'performance':'performance_commentary',
                      'exclude':'provisional_exclude', 'needs_context':'context_required'}
        for row in sample.to_dict('records'):
            mask=out.raw_row.eq(row['raw_row']) & out.audit_key.eq(row['audit_key'])
            assert mask.sum()==1 and row['scope_proposal'] in status_map
            out.loc[mask,['scope_status','topic_evidence','scope_basis','review_update']] = [status_map[row['scope_proposal']],row['topic_proposal'],row['reason_new_ko'],'새 연구 범위에 따른 개별 재검토; 잠정']
    # Include optional individually reviewed cases; no other automatic candidate promotion.
    manual_path = AUDIT/'integrated_manual_review.csv'
    if manual_path.exists():
        manual=read(manual_path)
        assert manual.raw_row.is_unique
        for row in manual.to_dict('records'):
            mask=out.raw_row.eq(row['raw_row']) & out.audit_key.eq(row['audit_key'])
            assert mask.sum()==1
            for source,target in [('scope_status','scope_status'),('topic','topic_evidence'),('reason_ko','scope_basis')]: out.loc[mask,target]=row[source]
            out.loc[mask,'review_update']='새 연구 범위에 따른 개별 재검토; 잠정'
    out['analysis_ready'] = 'no'
    out['time_note'] = '저장된 UTC/기존 거래일은 검증 전 원값; 거래일 재계산 필요'
    assert len(out)==26239 and out.raw_row.is_unique and out.audit_key.is_unique
    assert not out.trade_conflict_direction.ne('unresolved').any()
    out.to_csv(OUT,index=False,encoding='utf-8-sig')
    stats={'rows':len(out),'source_groups':out.source_group.value_counts().to_dict(),'scope_status':out.scope_status.value_counts().to_dict(),'analysis_ready':out.analysis_ready.value_counts().to_dict(),'review_update_count':int(out.review_update.ne('').sum()),'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [AUDIT/'full_corpus_review_coverage.csv',AUDIT/'existing_review_ledger.csv',AUDIT/'omission_review_ledger.csv',AUDIT/'remaining_individual_review_ledger.csv']}}
    (AUDIT/'integrated_classification_summary.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(stats,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
