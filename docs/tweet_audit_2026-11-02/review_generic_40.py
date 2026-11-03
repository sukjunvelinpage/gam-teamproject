"""개별 원문을 읽어 작성한 광의 후보 40건의 잠정 재검토 기록."""
from pathlib import Path
import pandas as pd

REVIEW = [
(1285,'exclude','정치','국방수권법을 둘러싼 정치 비판만 보이며 경제 조치는 명시되지 않음'),
(1288,'performance','주가','주가 최고치에 대한 사후 성과 평가이며 신규 정책이 아님'),
(1296,'exclude','재난','허리케인 해일·비·토네이도 경보로 경제정책은 나타나지 않음'),
(1297,'needs_context','고용','소수계 노동자 보호를 언급하나 리트윗이 잘려 내용과 조치를 확인할 수 없음'),
(1307,'include_candidate','보건·약가','의료비 청구·약가·가격 투명성 등 정책 공약이며 시행 확정과 구분'),
(1321,'exclude','선거','학교와 명절에 관한 선거 비난으로 경제정책 내용이 드러나지 않음'),
(1323,'include_candidate','재정·PPP','상원의 PPP 유연화 법안 통과 언급이나 잘린 대출 조건은 확인 필요'),
(1330,'include_candidate','조세·에너지','상대 후보의 증세·규제 등을 주장하는 선거 발언이며 실제 조치가 아님'),
(1335,'needs_context','조세·선거','증세 주장과 기회특구 언급이나 잘린 리트윗 나머지 내용 확인 필요'),
(1347,'needs_context','중소기업','중소기업 지원 법안 변경을 암시하지만 조치의 이름과 내용이 잘림'),
(1348,'needs_context','농업 지원','농무 서비스 기관 지원 신청 마감만 보이며 어떤 프로그램인지 확인 필요'),
(1349,'exclude','보건·입국','고위험 국가발 여행자 검사로 경제정책·통상 제한이 명시되지 않음'),
(1357,'exclude','우주·행사','우주 발사 및 NASA에 대한 일반 평가로 구체 경제정책이 드러나지 않음'),
(1368,'needs_context','고용·선거','고용에 관한 후보 비판 RT이나 잘려 구체 주장의 맥락 확인 필요'),
(1370,'exclude','보건·외교','인도네시아에 인공호흡기를 제공한다는 보건 외교이며 경제정책 조치가 명시되지 않음'),
(1375,'exclude','재난','허리케인에 대비하고 지역 당국에 협조한다는 공지'),
(1376,'needs_context','보건','치매 돌봄에 관한 단편으로 연결 내용이나 정책성 확인 필요'),
(1383,'include_candidate','재정·PPP','PPP 대출 9만8천 건과 조건 수정 언급이나 잘린 변경 내용은 확인 필요'),
(1388,'exclude','보건·행사','코로나 전화 타운홀 행사 안내로 구체 경제정책 내용 없음'),
(1389,'include_candidate','재정·PPP','PPP 대출기간 연장법의 상원 통과 언급이며 잘린 조건 추가 확인 필요'),
(1390,'needs_context','여론조사','정부 대응 신뢰도 여론조사 인용이 잘려 나머지 주제를 확인할 수 없음'),
(1400,'include_candidate','조세·선거','상대 후보의 증세 계획을 비판하는 선거 발언이며 실행된 증세가 아님'),
(1402,'needs_context','약가·기업','제약사 관련 행정명령을 언급하지만 핵심 의무가 잘려 원문 확인 필요'),
(1406,'needs_context','보건','요양원 사망에 관한 정치 발언이 잘려 후속 내용 확인 필요'),
(1411,'exclude','보건·개인','코로나 검사와 자가격리 발표로 경제정책 조치는 명시되지 않음'),
(1424,'exclude','보건·물자','주정부의 장비 요청 이행 상태에 대한 보건 성과 홍보이며 경제 조치 불명'),
(1428,'performance','고용','고용보고서에 대한 평가이며 새 정책 시행은 아님'),
(1433,'needs_context','보건','백신 개발 약속을 인용한 글이 잘려 관련 정책·경제 내용 확인 필요'),
(1435,'exclude','보건','사회적 거리두기와 마스크 착용 권고로 경제정책이 명시되지 않음'),
(1436,'performance','고용','고용보고서에 대한 긍정적 평가로 신규 정책이 아님'),
(1438,'performance','GDP·조세','GDP 성과 평가와 상대방의 증세 비판이 혼합되며 새 시행 조치 없음'),
(1444,'include_candidate','에너지·선거','후보의 수압파쇄 금지 가능성에 관한 제3자 주장으로 실제 금지 아님'),
(1452,'include_candidate','재정·PPP','의회의 PPP 제도 보완을 언급하나 세부 변경 내용은 잘림'),
(1453,'exclude','우주·행사','미국 우주비행사와 로켓에 대한 행사 메시지로 경제정책 불명'),
(1460,'needs_context','기후·선거','상대 후보의 기후계획을 다룬 기사 공유이나 정책 내용이 잘림'),
(1482,'performance','고용','주간 실업수당 청구 지표에 대한 회고로 신규 정책이 아님'),
(1500,'exclude','선거','사회주의에 대한 선거 수사이며 구체적 경제정책 조치 없음'),
(1512,'needs_context','형사·정책','제3자 회동과 플래티넘 계획을 언급하나 해당 계획 내용이 잘림'),
(1523,'performance','재정·PPP','PPP가 구한 기업·일자리 수를 회고하며 신규 조치 발표가 아님'),
(1525,'performance','GDP','GDP 3분기 성장률에 대한 성과 평가로 신규 조치가 아님'),
]

def main():
    base = Path(__file__).resolve().parent
    source = pd.read_csv(base / 'additional_extended_candidates.csv', dtype=str, keep_default_na=False)
    review = pd.DataFrame(REVIEW, columns=['raw_row','scope_proposal','topic_proposal','reason_new_ko'])
    review['raw_row'] = review.raw_row.astype(str)
    result = review.merge(source, on='raw_row', how='left', validate='one_to_one')
    assert len(result) == 40 and result.text.ne('').all()
    result.to_csv(base / 'generic_theme_manual_review_40.csv', index=False, encoding='utf-8-sig')
    print(result.scope_proposal.value_counts().to_string())

if __name__ == '__main__':
    main()
