"""개별 원문 열람 후 명시적으로 작성한 배치 판정을 검증·누적한다."""
import json
from pathlib import Path
import pandas as pd

P = Path(__file__).resolve().parent

def write_batch(start, count, groups):
    source = pd.read_csv(P / 'part_1.csv')
    expected = set(source.iloc[start:start+count].raw_row.astype(int))
    records = []
    for status, themes, direction, reason, ids in groups:
        for rid in ids:
            records.append(dict(raw_row=rid,status=status,themes=themes,direction=direction,reason_ko=reason,reviewer='review_part1',batch_id=f'p1_{start:04d}_{start+count:04d}'))
    assert len(records)==len(expected)==len(set(r['raw_row'] for r in records))
    assert set(r['raw_row'] for r in records)==expected
    target=P/'part_1_decisions.jsonl'
    old=[json.loads(x) for x in target.read_text(encoding='utf-8').splitlines()] if target.exists() else []
    assert not set(x['raw_row'] for x in old)&expected
    with target.open('a',encoding='utf-8') as f:
        for row in sorted(records,key=lambda x:x['raw_row']): f.write(json.dumps(row,ensure_ascii=False)+'\n')
    print('saved',len(records),'total',len(old)+len(records))

if __name__=='__main__':
    write_batch(0,150,[
        ('exclude',['Politics'],'na','바이든의 대테러 정책 비판이며 금융·무역 조치 없음',[6408]),
        ('include_extended',['Health_Travel'],'uncertain','공항 의료검사·지연을 직접 공지하므로 여행·보건정책 확장 범위',[6409]),
        ('needs_context',[],'uncertain','URL만 있어 연결된 글·매체를 복원해야 주제 판정 가능',[6410,6425,6479,6495,6499,6550,6551,6552]),
        ('needs_context',['Health'],'uncertain','코로나 태스크포스 생중계 예고만 있고 정책 내용 없음',[6411,6420]),
        ('exclude',['Politics_Media'],'na','민주당과 언론의 관계를 비난하며 경제정책 정보 없음',[6413,6439,6498,6510,6512]),
        ('exclude',['Politics'],'na','오바마 골프와 방역 권고의 모순을 공격하는 정치 논평',[6414]),
        ('include_extended',['Fiscal_Tax'],'uncertain','쿠오모 회동에서 세금 인하를 요구하나 구체적 세제·시행 정보 없음',[6415]),
        ('include_extended',['Local_Fiscal'],'uncertain','뉴욕시 경찰예산 10억달러 삭감을 언급하는 지방 재정 논쟁',[6416]),
        ('include_extended',['Macro_Campaign'],'neutral','경제 호황을 정치적 성과로 홍보하는 RT이며 신규 조치 없음',[6417]),
        ('exclude',['Impeachment_Investigation'],'na','탄핵·러시아·뮬러·Flynn·FISA·수사 절차 논평으로 금융정책 아님',[6419,6426,6429,6440,6442,6443,6444,6448,6459,6468,6471,6473,6476,6487,6491,6492,6500,6503,6519,6520,6521,6522,6524,6526,6539,6540,6549,6557,6558,6561]),
        ('needs_context',[],'uncertain','외부 칼럼·방송·논평 예고만 있어 본문에서 정책 내용 특정 불가',[6421,6436,6441,6465,6511,6536,6544,6562]),
        ('exclude',['Campaign_Media'],'na','바이든·해리스·대선토론·전당대회 지지와 언론 비평이며 신규 경제조치 없음',[6422,6423,6424,6427,6428,6437,6455,6461,6462,6463,6464,6466,6469,6478,6482,6484,6514,6515,6530,6531,6532,6545,6546,6554,6556,6564]),
        ('exclude',['Sports'],'na','Super Bowl 선수의 백악관 방문을 다루는 스포츠 RT',[6430]),
        ('needs_context',['Health_Seniors'],'uncertain','노인 보호 연설 생중계만 있어 구체 조치 판단 불가',[6431]),
        ('include_extended',['Fiscal_Infrastructure'],'positive','Blue Water Bridge 국경항 확장 2,500만달러 지원 제안; 교역 기반시설 확대',[6432]),
        ('exclude',['Judiciary_Politics'],'na','Schumer 대법원 발언 및 Barrett 인준 관련 정치 논쟁',[6433,6434]),
        ('include_core',['Industry_Mining_Regulation'],'uncertain','Pebble 광산 심사에 정치 개입하지 않겠다는 약속; 허가 결과는 미확정',[6438]),
        ('exclude',['Ceremony'],'na','기념행사 후원 기업들에 감사하는 글이며 기업 정책조치 아님',[6445]),
        ('needs_context',[],'uncertain','짧은 감사·동의·초대·진행 언급만 있어 연결 대상 없이는 정책 정보 판별 불가',[6446,6447,6460,6483,6490,6518,6555]),
        ('include_extended',['Fiscal_Infrastructure'],'positive','루이지애나 침수 방지 고가도로 1억3,500만달러 지원 제안',[6449]),
        ('exclude',['Sports'],'na','Big Ten 미식축구 경기 재개 요구로 목표 정책범위 밖',[6450]),
        ('exclude',['Politics'],'na','정부의 나쁜 인물을 제거하자는 정치 구호',[6451]),
        ('include_extended',['Health_Commentary'],'neutral','뉴욕 입원자 감소 및 곡선 평탄화 등 보건 통계 논평',[6452,6559]),
        ('include_core',['Company_Platform_Pressure'],'uncertain','Twitter 표현 제한을 대통령이 허용하지 않겠다는 압박; 후속 문맥과 조치 강도 확인 필요',[6453]),
        ('include_extended',['Fiscal_Infrastructure'],'positive','웨스트버지니아 Corridor H 완공을 위한 1,200만달러 지원 발표',[6457]),
        ('include_extended',['Fiscal_Infrastructure'],'positive','Wisconsin Merrimac 철도교 680만달러 개보수 지원 제안',[6458]),
        ('include_extended',['Campaign_Tax'],'uncertain','민주당 고세율을 비판하는 포괄적 선거 수사; 신규 세제 아님',[6467]),
        ('exclude',['Geopolitics_Iran'],'na','과거 이란 핵합의 비난이며 신규 금융 제재·무역조치 없음',[6470]),
        ('include_extended',['Veterans_Fiscal'],'uncertain','VA 예산·취업 성과를 홍보하는 RT이며 현행 범위 밖',[6472]),
        ('include_extended',['Health_Company'],'uncertain','Verily의 코로나 검사 분류도구 개발 발표; 규제·무역 충격이 아닌 기업 보건활동',[6475]),
        ('exclude',['Media_Attack'],'na','Atlantic 잡지 경영난과 해고를 조롱하며 신규 기업 정책조치 없음',[6477]),
        ('include_extended',['Fiscal_Infrastructure'],'positive','South Carolina I-77 교차로 개발을 위한 3,460만달러 지원',[6480]),
        ('include_extended',['Fiscal_Infrastructure'],'positive','Tennessee I-40 통신·광대역 인프라 1,120만달러 지원',[6481]),
        ('include_extended',['Health_Travel'],'uncertain','Wuhan의 이동제한 해제 소식 RT; 미국 무역정책은 아니지만 여행·보건 확장 정보',[6485]),
        ('include_extended',['Macro_Reopening'],'uncertain','주가지수 상승을 언급하며 주정부 경제 재개 촉구; 수익률로 부호 판정하지 않음',[6488]),
        ('include_extended',['Health_Testing'],'uncertain','주정부에 드라이브스루 검사를 강화하라고 요구하는 보건정책',[6489]),
        ('include_extended',['Fiscal_Port_Infrastructure'],'positive','Port Tampa Bay 컨테이너 시설 확장에 1,990만달러 지원',[6493]),
        ('include_extended',['Fiscal_Port_Infrastructure'],'positive','TulsaPort 철도 수송 개선에 620만달러 지원',[6494]),
        ('include_extended',['Health_Supply'],'positive','Colorado에 인공호흡기 100대 즉시 송부 발표',[6496]),
        ('exclude',['Poll'],'na','공화당 내 지지율 수치이며 경제정책 사건 아님',[6497]),
        ('exclude',['Religion_Support'],'na','대통령 보호를 바라는 기도와 지지 메시지',[6501]),
        ('exclude',['Domestic_Security'],'na','Kenosha·Portland 치안 및 주방위군 파견 논평',[6504]),
        ('include_extended',['Macro_Reopening'],'uncertain','경제 재개를 환영하거나 향후 호황을 예상하나 시행 조치·정책 조건 부족',[6505,6534,6547]),
        ('include_extended',['Fiscal_Infrastructure'],'positive','Rhode Island RI-246 안전 개선에 6,500만달러 지원',[6506]),
        ('include_extended',['Fiscal_Port_Infrastructure'],'positive','Port Houston 컨테이너터미널 복구·확장에 7,950만달러 지원',[6507]),
        ('include_extended',['Fiscal_Port_Infrastructure'],'positive','Washington Puget Sound 항만연계 도로에 7,370만달러 지원 제안',[6508]),
        ('exclude',['Media_Politics'],'na','기자회견 시청률과 언론의 무료 보도를 논평',[6509]),
        ('include_extended',['Geopolitics_Iran_Deal'],'uncertain','영국 총리가 이란합의를 Trump 합의로 바꾸자는 발언에 동의; 새 경제조건 불명',[6513]),
        ('exclude',['Campaign_Rhetoric'],'na','정당의 여러 정책 입장을 나열하는 선거 RT이며 확정 경제조치 없음',[6516]),
        ('include_extended',['Environment'],'uncertain','대기오염 배출 감소 등 환경 성과를 홍보하는 RT',[6517]),
        ('include_extended',['Foreign_Aid'],'uncertain','과거 우크라이나·파키스탄 원조 보류를 비교하는 정치 RT; 신규 지원변경 아님',[6523]),
        ('exclude',['Book_Promotion'],'na','Trump·Churchill 비교 서적 출간 축하 글',[6525]),
        ('include_extended',['Fiscal_Infrastructure'],'positive','Nevada Tropicana/I-15 교차로 재건에 5,000만달러 지원 제안',[6527]),
        ('include_extended',['Fiscal_Infrastructure'],'positive','North Carolina US74 고속도로 개선에 2,500만달러 지원',[6528]),
        ('include_core',['Trade_Deal_Progress'],'positive','United States-Mexico-Canada Agreement 협상 발표를 회고하는 RT; USMCA 약자 없이도 명확한 무역합의 문맥',[6529]),
        ('exclude',['Sports_Congratulations'],'na','GeauxTigers 응원·축하 글',[6533]),
        ('include_extended',['Campaign_Social_Security'],'uncertain','Social Security·Medicare 삭감 계획 부인과 상대 공약 비판; 신규 집행 아님',[6535]),
        ('exclude',['Election_Law'],'na','California 우편투표 소송에 관한 정치 기사 RT',[6538]),
        ('exclude',['Domestic_Security'],'na','Washington 동상 훼손범 수사와 형사처벌 경고',[6541]),
        ('include_extended',['Fiscal_Infrastructure'],'positive','Florida I-4 교통정보 기술 개선에 1,000만달러 지원',[6542]),
        ('include_extended',['Fiscal_Infrastructure'],'positive','Mississippi Greenville Bypass 완공에 7,150만달러 지원',[6543]),
        ('include_extended',['Health_Travel_Company'],'uncertain','Cambodia의 Westerdam 유람선 입항 허용에 감사; 보건·여행사건 확장 범위',[6548]),
        ('include_extended',['Fiscal_Infrastructure'],'positive','Delaware I95/SR896 교차로에 5,680만달러 지정',[6553]),
        ('exclude',['Diplomatic_Courtesy'],'na','Australia에 대한 친선·감사 표현으로 정책조치 없음',[6560]),
        ('exclude',['Geopolitics_Iran'],'na','이란에 대한 군사적 억지의 효과를 논평하는 RT',[6563]),
        ('exclude',['Memorial'],'na','Parkland 총격 희생자를 추모하는 연속 글',[6565,6566]),
    ])
