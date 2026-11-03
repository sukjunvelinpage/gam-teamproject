"""Inspect selected held posts with extended text from local reference archive."""
from pathlib import Path
import hashlib
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'docs/tweet_audit_2026-11-02'

def main():
    target={
        '4979':('유럽 이동 제한이 무역·화물에 적용되지 않는다는 3월 12일 02:13 UTC 트럼프 본인 정정(R4806) 이후 재게시.','https://trumpwhitehouse.archives.gov/briefings-statements/remarks-president-trump-address-nation/','R4806의 기존 정정이 트럼프 RT보다 앞섬; 독립 아카이브 본문 및 원작성자 확인 필요.'),
        '6529':('USMCA 7월 1일 발효를 발효 당일 이후 알린 백악관 RT.','https://www.ustr.gov/about-us/policy-offices/press-office/press-releases/2020/april/usmca-enter-force-july-1-after-united-states-takes-final-procedural-steps-implementation','2020-04-24 USTR이 7월 1일 발효 예정 공개; 발효 사실과 예정 발표는 구분.'),
        '11802':('코소보·세르비아 합의에 대한 언론 비판이며 확장 문구에 신규 무역·관세 조치 없음.','','연결매체 미확인, 외부 최초 공개 및 맥락 미검증.'),
        '21241':('미일 농업·디지털 무역협정 서명을 설명하는 이방카의 글을 트럼프가 RT.','https://www.ustr.gov/countries-regions/japan-korea-apec/japan/us-japan-trade-agreement-negotiations','10월 7일 공식 서명은 확인되나 서명·RT 및 이전 공개의 정확한 시각 차이는 미검증.'),
        '23958':('멕시코 관세 위협에 대한 정치적 평가 RT.','https://www.presidency.ucsb.edu/documents/tweets-june-8-2019','6월 8일 대통령 기록에 관세 유예 발표가 존재. 외부 링크 내용은 미확인.'),
        '23966':('에이즈 예방약 제공·무보험자 지원 관련 보건 RT.','','연결매체 미확인; 새 무역·관세 사안이 감춰졌는지 완전 배제하지 않음.'),
        '23980':('트럼프 자신의 멕시코 관세 유예 글을 하루가량 후 재전송.','https://www.presidency.ucsb.edu/documents/tweets-june-8-2019','대통령 기록에 원 글이 2019-06-08 00:25 및 00:31 기록; 원 RT와 게시시각 대조 추가 필요.'),
        '24191':('대일 무역협상 추진을 칭찬하는 정치 RT. 새 합의나 구체 관세 조치 미제시.','','링크 내용과 전후 맥락·사전 공개 여부 미검증.'),
        '24270':('미국산 쇠고기 일본 수입 제한 완화를 알리는 그래슬리 상원의원 RT.','https://www.usdajapan.org/market-research/reports/3196/','2019-05-17 USDA 일본 사무소 자료가 연령 제한 해제를 RT 전 공개. 동일 제한인지 검토해야 함.')}
    held=pd.read_csv(D/'conservative_review_integrated_2026-11-03.csv',dtype=str,keep_default_na=False)
    cross=pd.read_csv(D/'exact_id_crosswalk.csv',dtype=str,keep_default_na=False)
    ref=pd.read_csv(D/'independent_archive_reference.csv',dtype=str,skipinitialspace=True).fillna('')
    ref['exact_id']=ref['Tweet URL'].str.extract('/status/([0-9]+)',expand=False).fillna('')
    df=held[held.raw_row.isin(target)].merge(cross,on='raw_row',validate='one_to_one')
    ref=ref[ref.exact_id.isin(df.reference_exact_id)]
    assert ref.exact_id.is_unique
    df=df.merge(ref,left_on='reference_exact_id',right_on='exact_id',validate='one_to_one')
    assert len(df)==len(target)
    df['reference_extension_chars']=df['Tweet Text'].str.len()-df.text.str.len()
    assert (df.reference_extension_chars>20).all()
    for col in ['reason_ko','source_url','novelty_limitation']:
        df[col]=''
    for raw,(reason,source,limitation) in target.items():
        ix=df.raw_row.eq(raw)
        df.loc[ix,['reason_ko','source_url','novelty_limitation']]=[reason,source,limitation]
    df['decision']='hold'
    df['identity_quality']='근접 원본 ID와 교차표 URL 매칭; 원본 ID 정밀도 손상 및 교차표 검증 한계 존재'
    seconds=[]
    for row in df.to_dict('records'):
        snow=pd.Timestamp((int(row['reference_exact_id']) >> 22)+1288834974657,unit='ms',tz='UTC')
        stored=pd.to_datetime(row['date_utc'],utc=True)
        seconds.append((stored-snow).total_seconds())
    df['stored_minus_reference_id_seconds']=seconds
    df['timestamp_status']=df['stored_minus_reference_id_seconds'].map(lambda x: '2초 이내 일치; 원 아카이브 시각 별도 검증 필요' if abs(x)<=2 else '저장 시각과 ID 유래 시각 2초 초과 충돌; 원 시각 재확인 필요')
    df['archive_source']='https://github.com/MarkHershey/CompleteTrumpTweetsArchive/blob/master/data/realDonaldTrump_in_office.csv'
    cols=['raw_row','audit_key','date_utc','text','reference_exact_id','Tweet URL','Tweet Text','reference_extension_chars','archive_source','decision','reason_ko','source_url','novelty_limitation','identity_quality','stored_minus_reference_id_seconds','timestamp_status']
    df[cols].to_csv(D/'conservative_recovery_round3.csv',index=False,encoding='utf-8-sig')
    print(f'{len(df)} held rows with extended reference, all held')
if __name__=='__main__':main()
