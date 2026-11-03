# part_0 tail_b 개별 원문 검토 사례

## 범위와 방법

대상은 part_0.csv iloc[3700:6139], 총 2,439행이다. 100~250행 단위로 저장된 text 전체를 출력하여 개별 열람한 뒤 행별 판단을 기록했다. 원본의 잘린 RT, 링크 뒤 본문, 영상·이미지는 복원하지 않았다. 따라서 이는 제공 CSV 본문에 대한 전수검토이며 원 게시물 웹페이지·링크를 모두 확인한 검토는 아니다. raw_row는 원본 결합 키다.

include_core는 무역·통화·외환·농가·기업 행동/압박의 누락 후보, include_extended는 광의 경제·재정·보건·에너지 후보이며 최종 기존 분류체계 편입 확정과 다르다. 기업 방문·정부 활용·누적성과는 새로운 정책 이벤트와 구분한다. needs_context는 관련 없다는 판정이 아니며 원 링크·앞뒤글 확인이 필요하다. direction은 해당 본문에 대한 대상별 방향이고 관측 주가로 추론하지 않았다. 광의층 uncertain은 방향 확정을 유보한 것으로 이진 긍정/부정 분석에 바로 투입하면 안 된다.

## 판정 건수

- include_extended: 380행
- exclude: 1,527행
- needs_context: 492행
- include_core: 40행

## 주요·애매 사례

### raw_row 3852 — include_core / positive

> RT @SteveFDA: We issued a new authorization this evening to @Battelle for their decontamination system. @US_FDA staff have been working non…

FDA와 Battelle 제독장비 허가: 단순 팬데믹 언급과 달리 특정 기업에 대한 규제 허가다.

행별 기록: Battelle 제독체계 또는 Roche 항체검사에 대한 FDA 승인·허가를 알리는 기업별 보건규제 정보다. 구체 회사·승인 사건을 보존하되 주가상승을 단정하지 않는다. [본문: RT @SteveFDA: We issued a new authorization this evening to @Battelle for their decontamin]

### raw_row 3892 — include_core / positive

> RT @Reuters: Roche gets FDA emergency use approval for COVID-19 antibody test https://t.co/vo7nAK58ox https://t.co/eKbCjUuPU7

Roche 항체검사 긴급사용승인: 기업 허가에는 긍정적이지만 주가 상승이나 검사 효과를 확정하지 않는다.

행별 기록: Battelle 제독체계 또는 Roche 항체검사에 대한 FDA 승인·허가를 알리는 기업별 보건규제 정보다. 구체 회사·승인 사건을 보존하되 주가상승을 단정하지 않는다. [본문: RT @Reuters: Roche gets FDA emergency use approval for COVID-19 antibody test https://t.co]

### raw_row 3891 — needs_context / uncertain

> Thank you Dr. Hahn &amp; the FDA for your fast approval of this respected Ohio company recommended by Governor @MikeDeWine. Great potential! https://t.co/jAiIUAXwaL

Ohio 기업 FDA 승인 감사: 회사와 승인 내용이 본문에 없어 링크 확인 전 확정하지 않는다.

행별 기록: 링크·짧은 반응·생략된 지시대상만으로 정책 관련성이나 조치 내용을 확정하기 어렵다. 연결 원문 또는 앞 문맥 복원 전 보류한다. [본문: Thank you Dr. Hahn &amp; the FDA for your fast approval of this respected Ohio company rec]

### raw_row 3929 — include_core / positive

> RT @ChuckGrassley: Pres @realDonaldTrump is right 2use authority 2 keep open meat processing plants Its critical infrastructure 4 country's…

육가공장 가동 유지를 위한 대통령 권한 지지. 공급 유지와 근로자 건강의 효과는 분리해야 한다.

행별 기록: 육류 가공공장을 계속 가동하도록 대통령 권한을 사용한 것을 지지한다. 식량 공급망 생산조치라는 정책 내용이 명시된다. [본문: RT @ChuckGrassley: Pres @realDonaldTrump is right 2use authority 2 keep open meat processi]

### raw_row 4323 — include_core / mixed

> My Administration is helping U.S. auto workers by replacing the failed Obama Emissions Rule. Impossible to satisfy its Green New Deal Standard; Lots of unnecessary and expensive penalties to car buyers!

자동차 배출규정 교체: 산업 비용 완화와 환경 영향이 충돌하므로 단일 긍정으로 코딩하지 않는다.

행별 기록: 기존 Obama 자동차 배출규정을 교체해 자동차 근로자·소비자의 부담을 낮춘다고 발표한다. 산업 규제 변경이며 기업·소비자 영향은 다를 수 있다. [본문: My Administration is helping U.S. auto workers by replacing the failed Obama Emissions Rul]

### raw_row 4351 — include_core / mixed

> My proposal to the politically correct Automobile Companies would lower the average price of a car to consumers by more than $3500, while at the same time making the cars substantially safer. Engines would run smoother. Positive impact on the environment! Foolish executives!

차량가격 인하 주장: 법적 확정·실현가격과 기대효과를 구분한다.

행별 기록: 자동차 규제 대안이 평균가격을3500달러이상 낮추고 안전성을 높인다고 주장하며 경영진을 비난한다. 산업규제 제안·기업압박으로 보존하고 이전3000달러변형글과 사건중복을 점검한다. [본문: My proposal to the politically correct Automobile Companies would lower the average price ]

### raw_row 4397 — include_core / positive

> Everyone said it couldn’t be done. But for the first time in a generation, there will be direct flights between Serbia and Kosovo. Another win. Thanks to @WHNSC Ambassador Robert O’Brien and Ambassador @RichardGrenell! https://t.co/0qSLryG96B

Serbia-Kosovo 직항 합의: 국명만 있는 외교 수사가 아니라 구체 운송서비스 개통 관련이다.

행별 기록: 세르비아와 코소보 사이 직접 항공편 개통 합의를 발표한다. 외교적 찬사뿐 아니라 구체 항공서비스·교역연결 정보가 있다. [본문: Everyone said it couldn’t be done. But for the first time in a generation, there will be d]

### raw_row 4495 — include_core / positive

> RT @SenMcSallyAZ: .@Raytheon is headquartering its combined missiles defense unit right here in Southern Arizona.
> https://t.co/KhQRzdvSXt

Raytheon 사업부 본사 위치: 기업 조직·입지 정보이며 새로운 정책 법안과 구분한다.

행별 기록: Raytheon의 통합 미사일방어 부문 본사를 SouthernArizona에 둔다는 기업투자·입지 정보다. 신규확정인지 성과홍보인지 구분한다. [본문: RT @SenMcSallyAZ: .@Raytheon is headquartering its combined missiles defense unit right he]

### raw_row 4533 — include_core / negative

> Concast is known for its terrible service. On top of that they provide FAKE NEWS on MSDNC &amp; @NBCNews. Drop them and go to a good provider! https://t.co/Ew4cB2UPv4

Comcast 가입 해지 요구: 언론 비판에서 고객 이탈을 요구하는 기업 압박으로 넘어간다.

행별 기록: Concast(Comcast)의 서비스·방송을 비판하며 구독을 끊고 좋은 공급자로 옮기라고 직접 촉구한다. 회사불매 압박으로서 단순 언론 비판과 다르다. [본문: Concast is known for its terrible service. On top of that they provide FAKE NEWS on MSDNC ]

### raw_row 4657 — include_core / positive

> RT @SenShelby: Big news: @Airbus will again increase production rates in #Mobile, AL - resulting in 275 new jobs. Proud this company is bui...

Airbus Mobile 생산과 고용 확대: 구체 생산 증가·고용 숫자가 있어 기업투자 후보다.

행별 기록: Airbus가 Alabama Mobile 생산속도를 높여275개 일자리를 만든다는 기업 생산확장 RT다. 구체 회사·입지·수량이 있어 일반 경제찬사와 구분한다. [본문: RT @SenShelby: Big news: @Airbus will again increase production rates in #Mobile, AL - res]

### raw_row 4659 — include_core / uncertain

> مشاور امنیت ملی امروز عنوان کرد كه تحریم ها و اعتراضات، ایران را«به شدت تحت فشار»قرار داده است و آنها را مجبور به مذاكره می كند.در واقع، اصلا برایم اهمیتی نداردکه آیا آنها مذاکره می کنند یا نه.این کاملاً به عهده ی خودشان است، اما سلاح هسته ای نداشته باشیدو«معترضان خود را نکشید.» https://t.co/DBGGs8QFcJ

페르시아어 제재·협상 문맥: 영문 키워드만으로 누락될 수 있으며 신규 제재 발동은 아니다.

행별 기록: 페르시아어로 제재·시위가 이란을 협상하도록 압박한다는 보좌관 발언과 대통령의 반응을 전한다. 영문sanctions검색에 없는 동일 정책논평이며 신규 제재 명령은 아니다. [본문: مشاور امنیت ملی امروز عنوان کرد كه تحریم ها و اعتراضات، ایران را«به شدت تحت فشار»قرار داده]

### raw_row 4682 — include_core / positive

> CONGRATS to General Dynamic’s Bath Iron Works &amp; Local S6 on reaching a tentative agreement after the long strike. GD builds GREAT Arleigh-Burke destroyers. Super boost for Maine Economy. Glad to have helped. I’ve done a lot for Maine! https://t.co/6bXwvtje5P

General Dynamics Bath Iron Works 잠정 노사합의: 최종 타결이나 생산 재개 실현과 구분한다.

행별 기록: General Dynamics Bath Iron Works와 Local S6가 장기파업 후 잠정합의에 도달했다고 알린다. 회사 생산·노사 합의 정보이며 완전최종타결로 과장하지 않는다. [본문: CONGRATS to General Dynamic’s Bath Iron Works &amp; Local S6 on reaching a tentative agree]

### raw_row 4776 — include_extended / positive

> Just spoke to my friend MBS (Crown Prince) of Saudi Arabia, who spoke with President Putin of Russia, &amp; I expect &amp; hope that they will be cutting back approximately 10 Million Barrels, and maybe substantially more which, if it happens, will be GREAT for the oil &amp; gas industry!

MBS-Putin 원유 감산: 대통령의 기대·희망 수치이며 확정 합의로 읽지 않는다.

행별 기록: 사우디 왕세자·Putin과의 대화를 거쳐 원유약1000만배럴 감산을 기대한다고 말한다. 감산확정이 아닌 희망·예상이라는 점을 보존하는 에너지정책 후보다. [본문: Just spoke to my friend MBS (Crown Prince) of Saudi Arabia, who spoke with President Putin]

### raw_row 4788 — needs_context / uncertain

> .....Could be as high as 15 Million Barrels. Good (GREAT) news for everyone!

주어 없는 1,500만 배럴 후속글: 앞글을 자동 연결하지 않고 맥락 보류한다.

행별 기록: 링크·짧은반응·주체와 내용이 생략된 예고 또는 단편이다. 원문복원 전 경제정책 관련성·조치·부호를 확정하지 않는다. [본문: .....Could be as high as 15 Million Barrels. Good (GREAT) news for everyone!]

### raw_row 4884 — include_core / positive

> There is tremendous CoronaVirus testing capacity in Washington for the Senators returning to Capital Hill on Monday. Likewise the House, which should return but isn’t because of Crazy Nancy P. The 5 minute Abbott Test will be used. Please inform Dr. Brian P. Monahan. @MarkMeadows

Abbott 검사 활용: 제품의 정부 사용을 말하지만 새로운 FDA 허가나 계약량은 제시하지 않는다.

행별 기록: 복귀 의원들에게 Abbott5분진단검사를 사용할 계획을 명시한다. 회사제품의 공적 이용 정보지만 새 FDA허가나 확정 구매규모로 확대해석하지 않는다. [본문: There is tremendous CoronaVirus testing capacity in Washington for the Senators returning ]

### raw_row 4911 — include_core / negative

> We hit 3M hard today after seeing what they were doing with their Masks. “P Act” all the way. Big surprise to many in government as to what they were doing - will have a big price to pay!

3M에 대한 생산 압박: 회사명과 강제수단 P Act가 함께 제시되어 일반 정치비판과 구별한다.

행별 기록: 마스크 관련3M 행동을 비판하고 P Act사용 및 큰 대가를 언급한다. 회사생산·공급에 대한 대통령의 직접 압박이며 구체조치범위는 별도 확인한다. [본문: We hit 3M hard today after seeing what they were doing with their Masks. “P Act” all the w]

### raw_row 4944 — include_core / positive

> RT @IvankaTrump: Today, Honda signed the White House’s #PledgetoAmericasWorkers alongside @Jim_Jordan in Marysville, Ohio, committing to tr…

Honda 노동훈련 서약: 기업의 약속과 실제 투자·고용 실현을 구분한다.

행별 기록: Honda가 백악관 Pledge to Americas Workers에서 훈련을 약속했다는RT다. 구체 기업의 고용·인력훈련 약속이며 투자액이나 시행완료는 알 수 없다. [본문: RT @IvankaTrump: Today, Honda signed the White House’s #PledgetoAmericasWorkers alongside ]

### raw_row 5049 — include_core / positive

> RT @SeemaCMS: Thanks, @UnitedHealthGrp, for helping ensure your communities have coverage for the #COVID19 testing and treatment they need.

UnitedHealthGroup 보장: 기업 의료보장 조치이나 새 정책인지 기존 조치 감사인지는 불확실하다.

행별 기록: UnitedHealth그룹이 코로나 검사·치료 보장을 지원하는 것을 감사한다. 기업·건강보험 관련 정보로 보존하되 원문에서 새 합의 여부는 불확실하다. [본문: RT @SeemaCMS: Thanks, @UnitedHealthGrp, for helping ensure your communities have coverage ]

### raw_row 5221 — include_core / positive

> Making great progress in @Davos. Tremendous numbers of companies will be coming, or returning, to the USA. Hottest Economy! JOBS, JOBS, JOBS!

다보스 기업 복귀 전망: 확정 기업명·투자액이 없어 약한 기업 유치 신호로만 다룬다.

행별 기록: 다보스에서 기업들이 미국에 진출·복귀할 것이라고 밝힌 기업 유치 전망이다. 기업명·확정 계약·실현 투자는 제시되지 않는다. [본문: Making great progress in @Davos. Tremendous numbers of companies will be coming, or return]

### raw_row 5314 — include_core / positive

> RT @IvankaTrump: Effective immediately, Brooks Brothers will produce 150,000 masks per day to protect those on the frontlines battling the…

Brooks Brothers 생산 전환: 하루 15만 마스크 생산이라는 구체 기업행동이다.

행별 기록: Brooks Brothers가 즉시 하루 15만 개 마스크를 생산한다는 기업 생산전환 소식이다. 보건 일반론과 달리 기업과 생산량이 명시된다. [본문: RT @IvankaTrump: Effective immediately, Brooks Brothers will produce 150,000 masks per day]

### raw_row 5364 — include_core / negative

> Can’t believe @ATT keeps the management after yet another @CNN ratings dive. Nobody watching, NO CREDIBILITY! Maybe they should make changes at AT&amp,T? https://t.co/jdCLuNWEEQ

AT&T 경영진 교체 압박: CNN 시청률 비판에 머무르지 않고 모회사 경영을 겨냥한다.

행별 기록: CNN 시청률 비판을 AT&T 경영진 교체 요구로 연결한다. 단순 언론 비판을 넘어 모회사 경영에 공개 압박하지만 법적 제재는 아니다. [본문: Can’t believe @ATT keeps the management after yet another @CNN ratings dive. Nobody watchi]

### raw_row 5389 — include_core / positive

> RT @BW: This German biotech company has made kits with 4 million coronavirus tests since the outbreak began https://t.co/KQczW0srBr

독일 바이오기업 검사키트 생산: 미국 기업·미국 규제 허가로 오인하지 않는다.

행별 기록: 독일 바이오기업이 누적 400만 검사 키트를 생산했다는 재게시다. 기업명과 미국 승인 여부는 제시되지 않아 링크 확인이 필요하다. [본문: RT @BW: This German biotech company has made kits with 4 million coronavirus tests since t]

### raw_row 5415 — include_core / negative

> RT @USATODAY: Viking Cruises cancels all cruises until May 1 due to coronavirus pandemic https://t.co/EGiOedfQx9

Viking 운항 취소: 코로나 관련 일반론이 아니라 기업 영업 중단이다.

행별 기록: Viking Cruises가 코로나로 5월 1일까지 모든 크루즈를 취소한다는 기업 영업 중단 소식이다. 정부가 새 명령을 발동했다는 뜻은 아니다. [본문: RT @USATODAY: Viking Cruises cancels all cruises until May 1 due to coronavirus pandemic h]

### raw_row 5467 — include_core / positive

> RT @WhiteHouse: President @realDonaldTrump will travel to Central Florida to watch as @NASA and @SpaceX launch astronauts from American soi…

SpaceX 유인발사 방문: 기업 사업 진행과 대통령 행사 참석을 구분하며 투자·보조금 발표로 읽지 않는다.

행별 기록: NASA와 SpaceX의 미국 내 유인발사에 대통령이 참석할 예정이라는 기업·공공 우주사업 진행 소식이다. 신규 계약이나 투자 발표는 아니다. [본문: RT @WhiteHouse: President @realDonaldTrump will travel to Central Florida to watch as @NAS]

### raw_row 5650 — include_core / negative

> RT @thehill: Trump considers forming panel to investigate anti-conservative bias on social media: report https://t.co/7381Siae49 https://t.…

소셜미디어 조사 패널: 검토 보도이고 실제 기구 설치·법 집행과 다르다.

행별 기록: 보수 편향 문제를 조사할 소셜미디어 조사기구를 검토한다는 기사 재게시다. 플랫폼 규제 압박이지만 구성·집행 확정은 아니다. [본문: RT @thehill: Trump considers forming panel to investigate anti-conservative bias on social]

### raw_row 5709 — include_core / negative

> At my request, effective midnight tonight, Carnival, Royal Caribbean, Norwegian, and MSC have all agreed to suspend outbound cruises for thirty days. It is a great and important industry – it will be kept that way!

4개 크루즈사 운항중단 합의: 보건 목적은 긍정일 수 있으나 기업 영업에는 제한이므로 negative를 기업 관점으로 명시한다.

행별 기록: 대통령 요청에 Carnival·Royal Caribbean·Norwegian·MSC가 자정부터 30일 출항 중단에 동의했다. 기업별 영업을 제한하는 구체 합의이며, 보건상 효과와 기업 매출 방향을 분리한다. [본문: At my request, effective midnight tonight, Carnival, Royal Caribbean, Norwegian, and MSC h]

### raw_row 5959 — include_core / mixed

> Democrats Hate that I called for Big Pharma to match the lowest prescription drug prices in the World by using a FAVORED NATIONS CLAUSE. Prices will plunge!

국제최저약가 조항: 소비자 비용과 제약기업 가격권의 방향이 달라 mixed.

행별 기록: 제약사에 최저 국제약가를 맞추도록 최혜국 조항을 요구했다고 밝힌다. 소비자 비용 절감과 제약사 수익 압박이 상반하므로 단일 시장 긍정으로 단정하지 않는다. [본문: Democrats Hate that I called for Big Pharma to match the lowest prescription drug prices i]

### raw_row 5989 — include_core / mixed

> Drug companies, which are being forced by me to substantially reduce Drug Prices, are taking $millions in ads saying I want to increase Medicare Primiums. Wrong, just the opposite! These ads show DRUG PRICES ARE GOING DOWN, and they are not happy! False advertising!

제약사 가격인하 압박 및 광고 반발: 새로운 법적 조치인지 여부와 약가·기업 이익 효과를 분리한다.

행별 기록: 제약사 약가 인하 강제 주장과 제약사 광고 반발이 함께 제시된다. 환자 약가에는 우호적·기업 가격권에는 불리하므로 혼합 방향이며 실제 집행 여부는 별도 확인해야 한다. [본문: Drug companies, which are being forced by me to substantially reduce Drug Prices, are taki]

### raw_row 6290 — include_core / negative

> RT @realDonaldTrump: At my request, effective midnight tonight, Carnival, Royal Caribbean, Norwegian, and MSC have all agreed to suspend ou…

크루즈 운항중단 원글 재게시: 트윗 행 수와 독립 사건 수를 혼동하지 않는다.

행별 기록: 대통령 요청에 Carnival·Royal Caribbean·Norwegian·MSC가 출항중단에 동의했다는 본인글 재게시다. 원조치 raw5709와 중복 사건으로 다루고 별도 신규조치로 세지 않는다. [본문: RT @realDonaldTrump: At my request, effective midnight tonight, Carnival, Royal Caribbean,]

### raw_row 6210 — exclude / na

> RT @JohnWHuber: Not only is the statement “Flynn had told Russia to ignore US sanctions” 100% false, it doesn’t even make sense if it were…

Flynn의 제재 통화 관련 주장: sanctions라는 단어만 있으나 정치수사 수사에 대한 반박이며 새 제재 정책은 아니다.

행별 기록: 정치·선거·탄핵·안보외교·인사·개인 감사·행사·언론공방이다. 세금/기업/제재 단어가 나와도 구체 경제정책이나 기업조치는 제시하지 않는다. [본문: RT @JohnWHuber: Not only is the statement “Flynn had told Russia to ignore US sanctions” 1]

### raw_row 6206 — exclude / na

> Congratulations to @foxandfriends on completely dominating the just released morning TV Ratings. Morning Joke, staring Psycho Joe Scarborough on MSDNC, a Concast Company, was a disaster. Even worse was the barely registering @CNN mess!

Comcast 자회사 시청률 비판: 회사명만 등장하고 불매·경영교체·규제 요구가 없어 제외한다.

행별 기록: 정치·선거·탄핵·안보외교·인사·개인 감사·행사·언론공방이다. 세금/기업/제재 단어가 나와도 구체 경제정책이나 기업조치는 제시하지 않는다. [본문: Congratulations to @foxandfriends on completely dominating the just released morning TV Ra]

### raw_row 4057 — exclude / na

> RT @mchooyah: We should just vote by FedEx. Oh wait, you’ll need an ID.

FedEx를 이용한 투표 농담: 물류기업 정책이 아니라 선거·신분증 주장이다.

행별 기록: 본문은 선거·탄핵·인물 비판·감사·행사·스포츠 또는 개인 논평이다. 구체적인 무역·통화·농가·기업 정책 조치가 명시되지 않아 현행 연구 범위에서 제외한다. [본문: RT @mchooyah: We should just vote by FedEx. Oh wait, you’ll need an ID.]

### raw_row 4380 — exclude / na

> خطاب به رهبران ايران: معترضان خود را نكشيد. هزاران تن تاكنون به دست شما كشته يا زنداني شده اند، و جهان نظاره گر است. مهمتر از ان، ايالات متحده نظاره گر است. اينترنت را دوباره وصل كنيد و به خبرنگاران اجازه دهيد ازادانه حركت كنند! كشتار مردم بزرگ ايران را متوقف كنيد! https://t.co/rzpx3Nfn03

페르시아어 이란 시위자 지지: 외국어·국명 자체가 경제제재를 뜻하지 않는다.

행별 기록: 선거·탄핵·정치·언론 비판, 안보·인권 또는 행사·개인 논평이다. 본문에 구체 경제제재·무역·통화·기업 조치가 없어 현행 정책 범위에서 제외한다. [본문: خطاب به رهبران ايران: معترضان خود را نكشيد. هزاران تن تاكنون به دست شما كشته يا زنداني شده]
