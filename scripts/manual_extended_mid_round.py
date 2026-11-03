"""Record conservative decisions for 179 individually displayed source rows."""
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'docs/tweet_audit_2026-11-02'
def main():
    d=pd.read_csv(ROOT/'data/trump_policy_tweets_integrated_review.csv',dtype=str,keep_default_na=False)
    files=['conservative_review_log.csv','conservative_existing_next.csv','conservative_additional_next.csv','conservative_existing_round3.csv','conservative_screen_round3.csv','conservative_extended_round3.csv','conservative_extended_middle_round3.csv','conservative_extended_tail_round3.csv','conservative_extended_last_round3.csv']
    previous=set()
    for name in files:
        path=D/name
        if path.exists():
            previous.update(pd.read_csv(path,dtype=str,keep_default_na=False).raw_row)
    x=d[(d.additional_status=='include_extended') & d.raw_row.astype(int).between(15000,19999) & ~d.raw_row.isin(previous)].copy()
    assert len(x)==179 and x.raw_row.iloc[0]=='18584' and x.raw_row.iloc[-1]=='19999'
    hold=x.text.str.contains(r'https?://|(?:\.\.\.|…)',regex=True) | x.raw_row.isin(['18774'])
    x['decision']='exclude_core'
    x.loc[hold,'decision']='hold'
    x['direction']='uncertain'
    x['reason_ko']='저장 본문의 주제는 예산·세금·고용·보건·선거·국방 등이며 구체적 신규 무역·관세 발표는 확인되지 않음. 보조 분석 대상 여부는 별도.'
    x.loc[hold,'reason_ko']='본문에 연결 자료나 단편이 있어 그 내용 확인 전 무역·관세 핵심 여부 판단을 보류함.'
    out=x[['raw_row','decision','direction','reason_ko']]
    out.to_csv(D/'conservative_extended_mid_continue.csv',index=False,encoding='utf-8-sig')
    print(len(out),out.decision.value_counts().to_dict())
if __name__=='__main__':main()
