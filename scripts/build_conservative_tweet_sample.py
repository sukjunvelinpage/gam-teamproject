"""Produce a small evidence-backed provisional sample and transparent review ledger."""
from pathlib import Path
import json
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'docs/tweet_audit_2026-11-02'
def read(p): return pd.read_csv(p,dtype=str,keep_default_na=False)
def main():
    allrows=read(ROOT/'data/trump_policy_tweets_integrated_review.csv')
    existing=read(D/'conservative_existing_review.csv')
    extra=read(D/'conservative_additional_review.csv')
    ext=read(D/'conservative_extended_review.csv')
    logs=[]
    for r in existing.to_dict('records'):
        logs.append({'raw_row':r['raw_row'],'stage':'기존 분류 개별 사례','decision':r['decision'],'reason_ko':r['reason_ko']})
    for r in extra.to_dict('records'):
        logs.append({'raw_row':r['raw_row'],'stage':'추가 후보 검토','decision':r['review_status'],'reason_ko':r['reason_ko']})
    for r in ext.to_dict('records'):
        logs.append({'raw_row':r['raw_row'],'stage':'복원·확장 후보 확인','decision':r['decision'],'reason_ko':r['reason_ko']})
    log=pd.DataFrame(logs)
    log=log.merge(allrows[['raw_row','audit_key','date_utc','text','source_group']],on='raw_row',how='left',validate='many_to_one')
    assert log.audit_key.ne('').all()
    log.to_csv(D/'conservative_review_log.csv',index=False,encoding='utf-8-sig')
    evidences=[
      {'raw_row':'24641','evidence_url':'https://www.piie.com/sites/default/files/documents/trump-trade-war-timeline.pdf','evidence_summary':'미중 협상 중 관세 인상을 2019-05-05 트윗으로 발표하고 이후 공식 확인했다는 연혁. 앞선 보도 부재의 완전한 증명은 아님.','source_tweet_url':'https://twitter.com/realDonaldTrump/status/1125069835044573186','why_selected':'중국산 2천억 달러 상품의 기존 10% 관세를 금요일 25%로 인상하겠다고 구체적으로 예고. 핵심 문장은 보존됐으나 다음 문장은 잘려 있음.'},
      {'raw_row':'5605','evidence_url':'https://www.presidency.ucsb.edu/documents/tweets-december-2-2019','evidence_summary':'해당 날짜 게시물과 핵심 조치 문구를 확인. 당시 보도 https://www.investing.com/news/economy/trump-says-he-will-restore-tariffs-on-brazil-argentina-metal-imports-tweet-2031393 도 트윗 발표로 설명. 앞선 보도 부재의 완전한 증명은 아님.','source_tweet_url':'https://twitter.com/realDonaldTrump/status/1201455858636472320','why_selected':'브라질·아르헨티나산 철강·알루미늄 관세의 즉시 복원을 선언. 관세가 실제 발효됐다는 뜻은 아님.'}
    ]
    e=pd.DataFrame(evidences)
    out=e.merge(allrows[['raw_row','audit_key','date_utc','text','existing_snowflake_utc','existing_timestamp_conflict']],on='raw_row',validate='one_to_one')
    assert len(out)==2 and (out.existing_timestamp_conflict.str.lower()=='false').all()
    out['topic']='trade_tariff'; out['trade_direction']='escalation'; out['decision']='provisional_include'; out['novelty_confidence']='source_supported_not_exhaustively_verified'; out['trading_date']=''; out['analysis_ready']='no'
    out.to_csv(ROOT/'data/trump_trade_conservative_core_provisional.csv',index=False,encoding='utf-8-sig')
    summary={'review_log_entries':len(log),'reviewed_unique_raw_rows':int(log.raw_row.nunique()),'provisional_included':len(out),'final_included':0,'corpus_rows':len(allrows),'remaining_not_reviewed_by_new_standard':int(len(allrows)-log.raw_row.nunique()),'warning':'기록된 보류는 확정 제외가 아니며 후보 2건은 자료로 뒷받침되나 선행 공개 전수확인 및 최종 시점 정렬 미완료'}
    (D/'conservative_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
