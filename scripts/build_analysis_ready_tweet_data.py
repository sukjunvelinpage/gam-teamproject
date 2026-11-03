"""Prepare transparent tweet-level and daily analysis inputs; unknowns remain null."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import pandas_market_calendars as mcal

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'data'
AUDIT = ROOT/'docs/tweet_audit_2026-11-02'

def read(path): return pd.read_csv(path, dtype=str, keep_default_na=False)

def main():
    np.random.seed(42)
    master = read(DATA/'trump_policy_tweets_integrated_review.csv')
    review = read(AUDIT/'conservative_review_integrated_2026-11-03.csv')
    times = read(AUDIT/'raw_timestamp_audit.csv')
    market = read(DATA/'trump_market_extended_data.csv')
    assert len(master)==len(review)==len(times)==26239
    assert all(x.raw_row.is_unique and x.audit_key.is_unique for x in (master,review,times))
    assert len(market)==1007 and market.Date.is_unique
    m = master.copy()
    m = m.merge(review[['raw_row','audit_key','review_state','review_detail','reason_ko','direction','evidence_count']].rename(columns={'review_state':'strict_review_state','review_detail':'strict_review_detail','reason_ko':'strict_reason_ko','direction':'strict_direction','evidence_count':'strict_evidence_count'}),on=['raw_row','audit_key'],validate='one_to_one')
    m = m.merge(times[['raw_row','audit_key','snowflake_utc','stored_minus_snowflake_seconds','timestamp_conflict']].rename(columns={'snowflake_utc':'id_time_approx_utc','timestamp_conflict':'time_conflict'}),on=['raw_row','audit_key'],validate='one_to_one')
    flag = pd.Series(pd.NA,index=m.index,dtype='Int64')
    flag.loc[m.strict_review_state.eq('excluded_core')]=0
    flag.loc[m.strict_review_state.eq('provisional_include')]=1
    m['strict_provisional_flag']=flag
    m['strict_confirmed_flag']=pd.Series(pd.NA,index=m.index,dtype='Int64')
    m['strict_direction'] = m.strict_direction.where(m.strict_review_state.eq('provisional_include') & m.strict_direction.isin(['escalation','deescalation','mixed']),pd.NA)
    m['legacy_signal']=m.existing_context_signal.replace('',pd.NA)
    m['legacy_subtype']=m.existing_context_sub_type.replace('',pd.NA)
    m['legacy_signal_is_original_scope']=m.source_group.eq('existing_1246').astype(int)
    # Separate literal tone from prior policy-direction labels; only manually reviewed rows receive a value.
    eligible=m.additional_status.isin(['include_core','include_extended']) | m.screened_review_disposition.str.contains('추가 분류 필요',na=False)
    tone_files=[AUDIT/'tone_core_manual.csv',AUDIT/'tone_extended_a.csv',AUDIT/'tone_extended_b.csv',AUDIT/'tone_extended_c.csv',AUDIT/'tone_screen_manual.csv']
    parts=[read(p) for p in tone_files if p.exists()]
    manual=pd.concat(parts,ignore_index=True) if parts else pd.DataFrame(columns=['raw_row','tone','tone_reason_ko'])
    assert manual.raw_row.is_unique and set(manual.raw_row).issubset(set(m.loc[eligible,'raw_row']))
    assert set(manual.tone).issubset({'positive','negative','mixed','neutral','unknown'})
    assert manual.tone_reason_ko.ne('').all()
    m=m.merge(manual,on='raw_row',how='left',validate='one_to_one')
    m['additional_tone_scope']=np.where(eligible,'candidate_eligible','out_of_scope')
    m['additional_tone_status']=np.where(~eligible,'out_of_scope',np.where(m.tone.isna(),'not_reviewed',np.where(m.tone.eq('unknown'),'undetermined','reviewed')))
    m['additional_tone']=m.tone.where(m.tone.isin(['positive','negative','mixed','neutral']),pd.NA)
    m['additional_tone_reason_ko']=m.tone_reason_ko
    m=m.drop(columns=['tone','tone_reason_ko'])
    # NYSE trading sessions, including early closes; time at exact close maps forward.
    days=pd.DatetimeIndex(pd.to_datetime(market.Date))
    schedule=mcal.get_calendar('NYSE').schedule(start_date=days.min(),end_date=days.max())
    assert set(schedule.index.strftime('%Y-%m-%d')) == set(market.Date)
    close=pd.DatetimeIndex(schedule.market_close)
    def map_times(values):
        parsed=pd.to_datetime(values,utc=True,errors='coerce',format='mixed')
        out=pd.Series(pd.NA,index=m.index,dtype='string')
        valid=parsed.notna()
        pos=close.searchsorted(parsed[valid],side='right')
        rows=parsed[valid].index
        in_range=pos<len(close)
        out.loc[rows[in_range]]=schedule.index[pos[in_range]].strftime('%Y-%m-%d')
        return out
    stored=map_times(m.date_utc)
    derived=map_times(m.id_time_approx_utc)
    conflict=m.time_conflict.str.lower().isin(['true','1'])
    no_id=m.id_time_approx_utc.eq('')
    # Stop at the uncertain close boundary; timestamp disagreement always remains unresolved.
    parsed=pd.to_datetime(m.date_utc,utc=True,errors='coerce',format='mixed')
    boundary=pd.Series(False,index=m.index)
    close_nanos=close.as_unit('ns').asi8
    val=parsed.notna()
    event_nanos=parsed[val].dt.as_unit('ns').astype('int64').to_numpy()
    pos=np.searchsorted(close_nanos,event_nanos)
    nearest=np.minimum(pos,len(close_nanos)-1)
    prev=np.maximum(pos-1,0)
    arr=event_nanos
    delta=np.minimum(np.abs(close_nanos[nearest]-arr),np.abs(close_nanos[prev]-arr))
    boundary.loc[parsed[val].index]=delta<=2_000_000_000
    uncertain=conflict|boundary|no_id|parsed.isna()
    m['stored_time_trading_date_candidate']=stored
    m['id_time_trading_date_candidate']=derived
    m['trading_date']=stored.mask(uncertain,pd.NA)
    m['time_assignment_status']=np.select([conflict,boundary,no_id,parsed.isna()],['time_conflict_unresolved','near_close_unresolved','id_time_missing','time_missing'],default='stored_and_id_approximately_match')
    # unresolved rows could belong to either candidate day; mark both as possibly affected.
    unknown=m.strict_provisional_flag.isna()|m.trading_date.isna()
    time_before=map_times(parsed-pd.Timedelta(seconds=2))
    time_after=map_times(parsed+pd.Timedelta(seconds=2))
    candidates=pd.concat([pd.DataFrame({'raw_row':m.loc[unknown,'raw_row'],'Date':stored.loc[unknown]}),pd.DataFrame({'raw_row':m.loc[unknown,'raw_row'],'Date':derived.loc[unknown]}),pd.DataFrame({'raw_row':m.loc[boundary,'raw_row'],'Date':time_before.loc[boundary]}),pd.DataFrame({'raw_row':m.loc[boundary,'raw_row'],'Date':time_after.loc[boundary]})],ignore_index=True).dropna().drop_duplicates()
    unknown_count=candidates.groupby('Date').raw_row.nunique()
    observed=m[m.strict_provisional_flag.eq(1).fillna(False)&m.trading_date.notna()].groupby('trading_date').raw_row.nunique()
    daily=market.copy()
    # The 120 legacy columns are left as-is and retained for baseline comparison.
    daily['strict_provisional_known_count']=daily.Date.map(observed).fillna(0).astype(int)
    daily['strict_unresolved_possible_count']=daily.Date.map(unknown_count).fillna(0).astype(int)
    daily['strict_provisional_event']=pd.Series(pd.NA,index=daily.index,dtype='Int64')
    daily.loc[daily.strict_provisional_known_count.gt(0),'strict_provisional_event']=1
    daily.loc[daily.strict_provisional_known_count.eq(0)&daily.strict_unresolved_possible_count.eq(0),'strict_provisional_event']=0
    daily['strict_confirmed_event']=pd.Series(pd.NA,index=daily.index,dtype='Int64')
    daily['strict_confirmed_event_note']='확정 사건 0건; 잠정·보류 행은 0이 아님'
    # Event counts cover added candidates only. Unknown tone/date leaves an unknown binary signal.
    tone_pending=eligible & (m.additional_tone.isna() | m.trading_date.isna())
    tone_possible=pd.concat([pd.DataFrame({'raw_row':m.loc[tone_pending,'raw_row'],'Date':stored.loc[tone_pending]}),pd.DataFrame({'raw_row':m.loc[tone_pending,'raw_row'],'Date':derived.loc[tone_pending]}),pd.DataFrame({'raw_row':m.loc[eligible & boundary,'raw_row'],'Date':time_before.loc[eligible & boundary]}),pd.DataFrame({'raw_row':m.loc[eligible & boundary,'raw_row'],'Date':time_after.loc[eligible & boundary]})],ignore_index=True).dropna().drop_duplicates()
    pending_counts=tone_possible.groupby('Date').raw_row.nunique()
    daily['additional_tone_unknown_possible_count']=daily.Date.map(pending_counts).fillna(0).astype(int)
    for val in ['positive','negative','mixed','neutral']:
        subset=m[m.additional_tone.eq(val).fillna(False)&m.trading_date.notna()]
        counts=subset.groupby('trading_date').raw_row.nunique()
        col='additional_tone_'+val
        daily[col+'_observed_count']=daily.Date.map(counts).fillna(0).astype(int)
        daily[col+'_event']=pd.Series(pd.NA,index=daily.index,dtype='Int64')
        daily.loc[daily[col+'_observed_count'].gt(0),col+'_event']=1
        daily.loc[daily[col+'_observed_count'].eq(0)&daily.additional_tone_unknown_possible_count.eq(0),col+'_event']=0
    tweet_path=DATA/'trump_tweets_analysis_input.csv'
    daily_path=DATA/'trump_market_analysis_input.csv'
    m.to_csv(tweet_path,index=False,encoding='utf-8-sig')
    daily.to_csv(daily_path,index=False,encoding='utf-8-sig')
    stats={'tweet_rows':len(m),'legacy_signal_counts':m.legacy_signal.value_counts(dropna=False).astype(int).to_dict(),
           'strict_review_state':m.strict_review_state.value_counts().to_dict(),
           'strict_provisional_flag_counts':{str(k):int(v) for k,v in m.strict_provisional_flag.value_counts(dropna=False).items()},
           'additional_tone_eligible':int(eligible.sum()),'additional_tone_status':m.additional_tone_status.value_counts().to_dict(),
           'additional_tone_counts':{str(k):int(v) for k,v in m.additional_tone.value_counts(dropna=False).items()},
           'time_conflict':int(conflict.sum()),'unmapped_trading_date':int(m.trading_date.isna().sum()),
           'daily_rows':len(daily),'daily_provisional_event_counts':{str(k):int(v) for k,v in daily.strict_provisional_event.value_counts(dropna=False).items()},
           'provisional_rows':m.loc[m.strict_provisional_flag.eq(1).fillna(False),['raw_row','trading_date','source_group']].to_dict('records'),
           'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [DATA/'trump_policy_tweets_integrated_review.csv',AUDIT/'conservative_review_integrated_2026-11-03.csv',AUDIT/'raw_timestamp_audit.csv',DATA/'trump_market_extended_data.csv']}}
    stats['legacy_signal_counts']={str(k):v for k,v in stats['legacy_signal_counts'].items()}
    stats['tone_source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in tone_files if p.exists()}
    (AUDIT/'analysis_input_summary.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(stats,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
