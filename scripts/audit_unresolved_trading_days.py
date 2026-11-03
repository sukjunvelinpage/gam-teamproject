"""미확정 원문이 겹치는 거래일을 기록한다. 시장가격이나 시그널을 수정하지 않는다."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import pandas_market_calendars as mcal

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/tweet_audit_2026-11-02/restoration'


def main():
    np.random.seed(42)
    OUT.mkdir(parents=True, exist_ok=True)
    events = pd.read_csv(ROOT / 'docs/tweet_audit_2026-11-02/remaining_context_required.csv', dtype={'id': str})
    market = pd.read_csv(ROOT / 'data/trump_market_extended_data.csv')
    days = pd.DatetimeIndex(pd.to_datetime(market.Date))
    schedule = mcal.get_calendar('NYSE').schedule(start_date=days.min(), end_date=days.max())
    closed = pd.DatetimeIndex(schedule.market_close)
    derived = pd.to_datetime(events.id.map(lambda x: (int(x) >> 22) + 1288834974657), unit='ms', utc=True)
    positions = closed.searchsorted(derived, side='right')
    events['snowflake_utc'] = derived.astype(str)
    events['mapped_actual_close'] = [str(schedule.index[i].date()) if i < len(schedule) else '' for i in positions]
    counts = events[events.mapped_actual_close.ne('')].groupby('mapped_actual_close').size()
    result = market[['Date', 'Policy_Pos_Dummy', 'Policy_Neg_Dummy', 'Fed_Neg_Dummy']].copy()
    result['unresolved_tweet_count'] = result.Date.map(counts).fillna(0).astype(int)
    result['current_no_signal'] = result[['Policy_Pos_Dummy','Policy_Neg_Dummy','Fed_Neg_Dummy']].eq(0).all(axis=1)
    result['no_signal_with_unresolved'] = result.current_no_signal & result.unresolved_tweet_count.gt(0)
    result.to_csv(OUT/'unresolved_trading_day_exposure.csv',index=False,encoding='utf-8-sig')
    events[['raw_row','audit_key','date_utc','snowflake_utc','mapped_actual_close']].to_csv(OUT/'unresolved_tweet_date_mapping.csv',index=False,encoding='utf-8-sig')
    summary = {'unresolved_rows':len(events),'unmapped_out_of_range':int(events.mapped_actual_close.eq('').sum()),
               'days_with_unresolved':int(result.unresolved_tweet_count.gt(0).sum()),
               'current_no_signal_days':int(result.current_no_signal.sum()),
               'current_no_signal_with_unresolved_days':int(result.no_signal_with_unresolved.sum()),
               'interpretation':'보류 트윗 동시 발생은 실제 정책 신호였다는 뜻이 아니다. 가격 데이터 장마감에 맞춘 노출가능성만 계산했으며 미확정 행을 0으로 보거나 신호로 확정하지 않았다.',
               'timestamp':'Snowflake ID의 상위 비트에서 UTC를 재구성해 NYSE 실제 폐장 및 휴일을 반영. ID 하위 정밀도 손상으로 초 경계는 추가 확인 필요.'}
    (OUT/'unresolved_trading_day_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
