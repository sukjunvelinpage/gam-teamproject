"""Hand-reviewed shortlist from existing classified tweets; no market return used."""
from pathlib import Path
import csv
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'docs/tweet_audit_2026-11-02'

def main():
    src = pd.read_csv(PATH/'existing_review_ledger.csv', dtype=str, keep_default_na=False).set_index('raw_row')
    # A specific announcement makes a candidate, not proof of contemporaneous surprise.
    rows = [
      ('17200','candidate_unverified','escalation','터키산 철강 50%·알루미늄 20%로 두 배 인상 승인 발표; 이전 보도 및 행정 시행 시점 확인 필요'),
      ('15829','candidate_unverified','deescalation','중국이 미국산 자동차 관세 인하·철폐에 합의했다는 구체적 주장; 선행 발표 및 합의 내용 확인 필요'),
      ('25116','candidate_unverified','escalation','EU 제품 110억 달러에 대한 관세 부과 예고; 이전 USTR 통보와 발표 시점 확인 필요'),
      ('24123','candidate_unverified','escalation','멕시코산 모든 제품에 6월 10일부터 5% 관세 부과 예고; 말미는 잘렸으므로 전체 맥락·기존 공개 여부 확인 필요'),
      ('24641','candidate_unverified','escalation','중국산 2천억 달러 상품 관세를 금요일 10%에서 25%로 인상하겠다는 구체적 발표; 후속 문장과 선행 보도 확인 필요'),
      ('5605','candidate_unverified','escalation','브라질·아르헨티나산 철강 및 알루미늄 관세 즉시 복원 선언; 실제 시행과 별개로 선행 공개 여부 확인 필요'),
      ('19273','candidate_unverified','mixed','대중 1단계 합의와 잔여 상품 7.5% 관세 내용을 발표; 기존 보도·앞뒤 스레드·정확한 합의 시점 확인 필요'),
      ('16559','hold','unknown','USMCA 합의 발표이나 전날 밤 타결을 직접 서술; 이전 공개 여부·잘린 뒷부분 확인 전 보류'),
      ('17767','hold','unknown','EU 자동차 20% 조건부 관세 예고이나 저장 시각이 ID 시각과 12시간 충돌; 정확 시각·최초 공개 확인 필요'),
      ('17763','exclude_repeat','unknown','R17767과 사실상 동일한 EU 자동차 관세 문구의 후속 반복; 두 기록의 시각 교차 확인 필요'),
      ('25654','hold','unknown','3월 1일 대중 관세 인상 연기 내용이나 앞부분이 잘린 스레드; 전체 맥락·최초 공개 확인 필요'),
      ('23998','exclude_repeat','unknown','멕시코 관세 유예 합의 발표가 R24000의 약 6분 후 동일 문장으로 반복; R24000의 시각 충돌 확인 필요'),
      ('24000','hold','unknown','멕시코 관세 유예 합의 발표이나 저장 시각이 ID 시각과 12시간 충돌하고 이어지는 본문이 잘림'),
      ('22930','hold','unknown','중국산 3천억 달러 상품에 대한 10% 관세 조각; 선행 스레드 및 중복 사건을 확인해야 함'),
      ('22486','hold','unknown','중국산 상품 관세 25%에서 30% 인상 발표 조각; 앞선 스레드와 직전 보도 확인 필요'),
      ('22485','hold','unknown','중국산 나머지 상품 관세 10%에서 15% 인상 조각; R22486과 동일 스레드 및 사건 중복 가능'),
      ('21964','hold','unknown','관세 인상일을 10월 1일에서 15일로 연기하는 후속 조각; 앞선 스레드 복원 및 선행 공개 확인 필요'),
      ('5502','hold','unknown','1단계 미중 합의 서명 일정 공지; 실제 합의 내용의 신규 발표와 구별하고 일정의 선행 보도 확인 필요'),
      ('25890','exclude_recap','unknown','기존 철강 관세의 효과 자찬·성과 회고로 구체적 신규 조치가 없음'),
      ('17252','exclude_recap','unknown','철강 관세 효과를 자찬하는 후속 글; 구체적인 신규 조치가 없음'),
      ('13476','exclude_vague','unknown','미중 관계 덕담으로 무역 합의의 구체적 발표가 없음'),
    ]
    out=[]
    for raw,status,direction,reason in rows:
        x=src.loc[raw]
        out.append({'raw_row':raw,'audit_key':x.audit_key,'decision':status,'trade_direction_provisional':direction,
                    'reason_ko':reason,'date_utc_stored':x.date_utc,'snowflake_utc':x.snowflake_utc,
                    'timestamp_conflict':x.timestamp_conflict,'tweet_text':x.text,'source_url':x.reference_url,
                    'novelty_verified':'no','external_first_disclosure_checked':'no',
                    'review_note':'본문 기반 선별; 최초 외부 공개 여부·정확 문맥의 독립 검증 전 핵심 확정 불가'})
    pd.DataFrame(out).to_csv(PATH/'conservative_existing_review.csv',index=False,encoding='utf-8-sig',quoting=csv.QUOTE_MINIMAL)
    print('Wrote',len(out),'manually reviewed examples; candidate_unverified',sum(v[1]=='candidate_unverified' for v in rows))

if __name__=='__main__': main()
