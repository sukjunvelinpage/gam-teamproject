"""Combine conservative review rounds without treating missing reviews as exclusions."""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'docs/tweet_audit_2026-11-02'
def read(path): return pd.read_csv(path, dtype=str, keep_default_na=False)

def main():
    master = read(ROOT/'data/trump_policy_tweets_integrated_review.csv')
    prior = read(D/'conservative_review_log.csv')
    existing = read(D/'conservative_existing_next.csv')
    additional = read(D/'conservative_additional_next.csv')
    evidence = read(D/'conservative_evidence_next.csv')
    core = read(ROOT/'data/trump_trade_conservative_core_provisional.csv')
    for f in [master, prior, existing, additional, core]: assert f.raw_row.is_unique
    assert set(existing.raw_row).isdisjoint(set(prior.raw_row))
    assert set(existing.raw_row).isdisjoint(set(additional.raw_row))
    assert set(prior.raw_row)|set(existing.raw_row)|set(additional.raw_row) <= set(master.raw_row)
    result = master[['raw_row','audit_key','date_utc','text','source_group','existing_context_signal','existing_context_sub_type','existing_timestamp_conflict','restore_restoration_status']].copy()
    result['review_state']='not_reviewed_under_conservative_standard'
    result['review_detail']=''
    result['reason_ko']=''
    result['direction']='unresolved'
    result['review_round']=''
    for r in prior.to_dict('records'):
        ix = result.raw_row.eq(r['raw_row'])
        # Prior generic holds and candidates remain holds until supported.
        state = 'excluded_core' if r['decision'].startswith('exclude') else 'hold'
        result.loc[ix,['review_state','review_detail','reason_ko','review_round']] = [state,r['decision'],r['reason_ko'],'previous']
    for stage, frame in [('existing_next',existing),('additional_next',additional)]:
        for r in frame.to_dict('records'):
            ix = result.raw_row.eq(r['raw_row'])
            state = 'excluded_core' if r['decision'].startswith('exclude') else 'hold'
            result.loc[ix,['review_state','review_detail','reason_ko','direction','review_round']] = [state,r['decision'],r['reason_ko'],r['direction'],stage]
    for name in ['conservative_existing_round3.csv', 'conservative_screen_round3.csv', 'conservative_extended_round3.csv', 'conservative_extended_middle_round3.csv', 'conservative_extended_tail_round3.csv', 'conservative_extended_last_round3.csv', 'conservative_extended_continue.csv', 'conservative_extended_mid_continue.csv', 'conservative_extended_late_continue.csv']:
        path = D/name
        if not path.exists():
            continue
        batch = read(path)
        assert batch.raw_row.is_unique and set(batch.raw_row).issubset(set(master.raw_row))
        for row in batch.to_dict('records'):
            ix = result.raw_row.eq(row['raw_row'])
            assert ix.sum()==1 and result.loc[ix,'review_state'].iloc[0]=='not_reviewed_under_conservative_standard'
            state = 'excluded_core' if row['decision'].startswith('exclude') else 'hold'
            result.loc[ix,['review_state','review_detail','reason_ko','direction','review_round']] = [state,row['decision'],row['reason_ko'],row['direction'],name]
    rereview_path = D/'conservative_hold_manual_continue.csv'
    if rereview_path.exists():
        rereview=read(rereview_path)
        assert rereview.raw_row.is_unique
        for row in rereview.to_dict('records'):
            ix = result.raw_row.eq(row['raw_row'])
            assert ix.sum()==1 and result.loc[ix,'review_state'].iloc[0]=='hold'
            state='excluded_core' if row['decision'].startswith('exclude') else 'hold'
            result.loc[ix,['review_state','review_detail','reason_ko','direction','review_round']] = [state,row['decision'],row['reason_ko'],row['direction'],rereview_path.name]
    # A truncated text may conceal the actual measure; preserve previous reason but do not assert exclusion.
    truncated = result.text.str.contains(r'(?:\.\.\.|…)\s*$', regex=True)
    uncertain_exclusion = result.review_state.eq('excluded_core') & truncated
    result.loc[uncertain_exclusion,'review_state'] = 'hold'
    result.loc[uncertain_exclusion,'review_detail'] = 'truncated_previously_excluded_review_again'
    result.loc[uncertain_exclusion,'reason_ko'] = result.loc[uncertain_exclusion,'reason_ko'] + ' 원문이 잘려 핵심 내용의 완결성을 확인하기 전 보류.'
    # USTR proposal preceded R25116, but the tweet's asserted certainty differs.
    ix=result.raw_row.eq('25116')
    result.loc[ix,['review_state','review_detail','reason_ko','review_round']] = ['hold','prior_proposal_comparison','전날 USTR이 110억 달러 피해 추정과 예비 목록을 공개했으나 트윗의 확정적 표현과 정보 차이는 추가 판단이 필요함.','external_evidence']
    for raw in core.raw_row:
        ix=result.raw_row.eq(raw)
        result.loc[ix,['review_state','review_detail','reason_ko','direction','review_round']] = ['provisional_include','source_supported_novelty_not_exhaustive','명시적 조치 내용은 외부 자료로 지지되나 완전한 선행 공개 부재 및 최종 시점 검증 전 보류','escalation','external_evidence']
    evidence3_path = D/'conservative_evidence_round3.csv'
    if evidence3_path.exists():
        evidence3 = read(evidence3_path)
        counts = pd.concat([evidence[['raw_row']],evidence3[['raw_row']]]).groupby('raw_row').size()
    else:
        counts = evidence.groupby('raw_row').size()
    recovery_path = D/'conservative_recovery_round3.csv'
    if recovery_path.exists():
        recovery = read(recovery_path)
        counts = counts.add(recovery.groupby('raw_row').size(), fill_value=0)
    result['evidence_count']=result.raw_row.map(counts).fillna(0).astype(int)
    result['analysis_ready']='no'
    assert len(result)==26239 and result.raw_row.is_unique and result.audit_key.is_unique
    result.to_csv(D/'conservative_review_integrated_2026-11-03.csv',index=False,encoding='utf-8-sig')
    stats={'rows':len(result),'review_state':result.review_state.value_counts().to_dict(),
           'reviewed_at_least_once':int(result.review_state.ne('not_reviewed_under_conservative_standard').sum()),
           'final_core_included':0,'provisional_include':len(core),'evidence_records':int(counts.sum()),
           'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/'conservative_review_log.csv', D/'conservative_existing_next.csv',D/'conservative_additional_next.csv',D/'conservative_evidence_next.csv',D/'conservative_existing_round3.csv',D/'conservative_screen_round3.csv',D/'conservative_extended_round3.csv',D/'conservative_extended_middle_round3.csv',D/'conservative_extended_tail_round3.csv',D/'conservative_extended_last_round3.csv',D/'conservative_extended_continue.csv',D/'conservative_extended_mid_continue.csv',D/'conservative_extended_late_continue.csv',D/'conservative_hold_manual_continue.csv',D/'conservative_evidence_round3.csv',D/'conservative_recovery_round3.csv'] if p.exists()}}
    (D/'conservative_review_update_summary.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(stats,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
