# part_0 tail_a 원문 개별검토 사례

검토 범위: part_0.csv iloc[1250:3700], 2,450개 고유 raw_row. 기존 400행과 후속 2,050행의 행별 판정 포함. CSV에 저장된 본문을 개별 열람했으며, RT 자체의 말줄임·URL 연결 내용은 복원하지 않았다. needs_context는 무관 판정이 아니다.

direction은 본문이 서술하는 정책·경제 방향의 보조 표지이며 사후 주가 수익률이나 객관적 사실 검증 결과가 아니다. mixed는 소비자·업계 또는 결합 정책의 방향이 다르다는 뜻이다. 광의 보건·재정·에너지 글은 extended로 분리했다. 선거 지지문 속 세금·일자리 단어만으로 core에 편입하지 않았다.

## 주요 및 애매 사례

### R1338 — include_core / negative

> Why isn’t Biden corruption trending number one on Twitter? Biggest world story, and nowhere to be found. There is no”trend”, only negative stories that Twitter wants to put up. Disgraceful! Section 230

트위터의 Biden기사 노출을 비판하며 Section230을 직접 거론하는 규제압박

### R1367 — include_core / positive

> RT @SenToomey: As @zoom_us user, it’s exciting see them opening a new R+D office in Pittsburgh, adding several hundred jobs. I have no doub…

Zoom Pittsburgh R&D사무실과 수백명 신규고용을 구체 언급한 재전송

### R1415 — exclude / na

> RT @SharylAttkisson: When did we decide, as Americans, that it's ok fo govt &amp, 3d parties to censor/ curate our info? That we cannot be trus...

정부와 제3자 정보검열을 비판하는 정치적 논평으로 대상 기업이나 구체 경제규제 조치 없음

### R1549 — exclude / na

> RT @realDonaldTrump: So disgusting to watch Twitter’s so-called “Trending”, where sooo many trends are about me, and never a good one. They…

트위터의 본인 관련 트렌드를 비판하는 정치적 재전송이며 규제·제재 요구가 본문에 없음

### R1563 — include_core / uncertain

> RT @Varneyco: On Wednesday, major big #tech leaders are meeting with Congress to discuss potential #regulations. We asked @RepKenBuck - wha…

빅테크 수장과 의회 잠재 규제 논의 관련 재전송; 규제확정 아님

### R1767 — exclude / na

> I paid many millions of dollars in Taxes to the Federal Government, most of which was even paid early, or PREPAID. MANY $MILLIONS. The Failing @nytimes never likes reporting that!

선거·정치 공방·지지·행사·개인 논평으로 신규 무역·통화·기업 정책조치가 본문에 제시되지 않음

### R1851 — include_extended / positive

> Just signed an order to protect fracking and the oil and gas industry. This means JOBS, low energy bills, and continued AMERICAN ENERGY INDEPENDENCE! Sleepy Joe would BAN fracking and destroy American energy jobs! He has NO clue!!

프래킹 및 석유가스 산업 보호 명령에 서명했다고 직접 발표한다. 구체 산업정책이나 무역갈등 사건과는 구분

### R1999 — include_core / mixed

> The drug companies are going crazy putting up nasty ads against me asking to “withdraw my Favored Nation’s Executive Order”. They don’t want the U.S. to have the lowest drug prices in the world, but we now will. Big reductions coming. No other politician would do this!!!

제약사들이 최혜국 행정명령 철회를 요구하는 광고를 내고 있다는 글로 약가규제 유지 입장을 명시. 소비자와 기업수익 방향이 달라 단일주가부호 부여불가

### R2090 — exclude / na

> I PREPAID Millions of Dollars in FEDERAL INCOME TAXES!

선거·정치 공방·지지·행사·개인 논평으로 신규 무역·통화·기업 정책조치가 본문에 제시되지 않음

### R2204 — include_extended / uncertain

> THANK YOU to the GREAT men and women of @FedEx and @UPS for driving through the storms this week to deliver millions of doses of the vaccine across the country. Two Great American Companies!

재정지원·직접지급·경기고용·백신유통·의료·경제재개를 다룬 광의 경제정보이며 무역·통화 사건과 구분해 정책단계·신규성 확인 필요

### R2242 — exclude / na

> RT @TheBabylonBee: California Mandates All Food Must Be Consumed Through IV To Ensure Masks Are Never Removed https://t.co/mwFBnW5gzY

BabylonBee의 음식물을 IV로만 섭취하도록 강제한다는 풍자 RT로 실제 행정명령이 아님

### R2518 — include_core / mixed

> RT @LindseyGrahamSC: @realDonaldTrump Congress will vote on additional stimulus checks and repealing Section 230 -- all wins for the Americ…

Section230 책임면제·폐지 및 기술기업 규제를 구체 언급하며 재정법·국방법과 결합된 경우 두 주제를 분리해야 함

### R2570 — include_core / mixed

> Unless Republicans have a death wish, and it is also the right thing to do, they must approve the $2000 payments ASAP. $600 IS NOT ENOUGH! Also, get rid of Section 230 - Don’t let Big Tech steal our Country, and don’t let the Democrats steal the Presidential Election. Get tough! https://t.co/GMotstu7OI

Section230 책임면제·폐지 및 기술기업 규제를 구체 언급하며 재정법·국방법과 결합된 경우 두 주제를 분리해야 함

### R2638 — include_core / mixed

> Because of the Trump Administration, hospitals are now required, effective immediately, to publish their REAL PRICES, which will create competition and drive downs costs MASSIVELY. Won lawsuit last week. Bigger than healthcare, it’s called PRICE TRANSPARENCY....

병원이 실제 가격을 공개하도록 하는 규제가 즉시·1월1일 시행됨을 명시하고 소송승소를 언급. 소비자혜택과 병원수익 영향은 구분

### R2648 — include_core / mixed

> TRANSPARENCY in medical pricing will be one of the biggest and most important things done for the American citizen. It was just put into service, January 1, against long odds and bitter opposition. Final lawsuits won last week. Enjoy all the extra money you will have!

병원이 실제 가격을 공개하도록 하는 규제가 즉시·1월1일 시행됨을 명시하고 소송승소를 언급. 소비자혜택과 병원수익 영향은 구분

### R2725 — needs_context / uncertain

> JOBS, JOBS, JOBS! https://t.co/wAkQMKdPXA

URL·짧은 반응·주어와 조치가 생략된 단편으로 연결 매체나 이전 원문 없이는 정책 관련성과 부호 확정 불가

### R2726 — include_extended / uncertain

> 'Trump signs bill undoing Obama coal mining rule' https://t.co/yMfT5r5RGh

Obama 석탄광산 규칙을 취소하는 법안 서명이라는 구체 에너지 규제변경 기사. 현행 무역범위와 분리

### R2987 — include_extended / negative

> In light of the attack from the Invisible Enemy, as well as the need to protect the jobs of our GREAT American Citizens, I will be signing an Executive Order to temporarily suspend immigration into the United States!

국민 일자리 보호와 코로나를 이유로 미국 이민 일시중단 행정명령 서명 예정 명시

### R3016 — include_extended / positive

> RT @WhiteHouse: President @realDonaldTrump signed the $8.3 billion funding bill to combat Coronavirus and defend the health and safety of t…

코로나 대응 83억달러 지출 법안 서명 명시

### R3069 — include_extended / mixed

> Finally! Suburban women are flocking over to us. They realize that I am saving the Suburbs - the American Dream! I terminated the Regulation that would bring projects and crime to Suburbia. Not on my watch! Biden will bring the Regulation back, but bigger and worse.

교외 저소득 주택 관련 규정 폐지했다고 주장하므로 단순 후보 비판과 구별

### R3133 — include_extended / positive

> I am allocating $2.96 BILLION in Emergency Solutions Grants to support homeless Americans and those at risk of becoming homeless because of job or wage loss, or illness due to COVID-19. We are taking care of our Nation’s most vulnerable citizens. Thanks @SecretaryCarson!

코로나 실직 임금손실 질환에 따른 노숙위험 지원29.6억달러 배정

### R3168 — include_core / positive

> Subject only to State approval, our important Ethanol Industry will be allowed to use the 10% Pumps for the 15% BLEND. Thank you! @SenJoniErnst @ChuckGrassley @SenatorFischer @SenJohnThune @SenatorRounds   @KimReynoldsIA @EPAAWheeler @SecretarySonny @govkristinoem

주 승인 조건하에10퍼센트펌프의15퍼센트에탄올혼합 허용 명시

### R3190 — include_core / mixed

> Every time you see a negative Big Pharma commercial against me remember, it means your drug prices are coming way down!

제약사 반대광고를 약가인하의 신호로 해석하며 업계를 압박하나 이 글만으로 새 명령의 시점은 확정할 수 없음

### R3288 — include_extended / negative

> I am giving consideration to a QUARANTINE of developing “hot spots”, New York, New Jersey, and Connecticut. A decision will be made, one way or another, shortly.

뉴욕 뉴저지 코네티컷의 격리를 고려중이며 아직 결정 전임을 명시

### R3465 — needs_context / uncertain

> Highly recommended by Governor @MikeDeWine of Ohio. @FDA must move quickly! https://t.co/pLpI4CSs9H

FDA신속처리 촉구하나 이 글만으로 승인대상 식별불가

### R3492 — include_core / positive

> Hope the FDA can approve Mask Sterilization equipment ASAP. As per Governor @MikeDeWine, there is a company in Ohio, @Battelle, which has equipment that can sterilize masks quickly.

Battelle회사 명시하며 마스크살균장비 FDA조속승인을 요구

### R3495 — include_extended / positive

> Upon departing the Oval Office for Ohio, I’ve notified my staff to continue working on an Executive Order with respect to Payroll Tax Cut, Eviction Protections, Unemployment Extensions, and Student Loan Repayment Options.

급여세감면 퇴거보호 실업연장 학자금상환 행정명령 준비 지시

### R3558 — exclude / na

> RT @JennyGuice: @realDonaldTrump Lord I'm Thankful Each Day, Trump gives us FaithTrump gives us VirtueTrump gives us DignityTrump give...

선거·정치 공방·지지·행사·개인 논평으로 신규 무역·통화·기업 정책조치가 본문에 제시되지 않음

### R3611 — needs_context / uncertain

> This is the letter sent to Dr. Tedros of the World Health Organization. It is self-explanatory! https://t.co/pF2kzPUpDv

URL·짧은 반응·주어와 조치가 생략된 단편으로 연결 매체나 이전 원문 없이는 정책 관련성과 부호 확정 불가

### R3700 — include_extended / positive

> We will not be touching your Social Security or Medicare in Fiscal 2021 Budget. Only the Democrats will destroy them by destroying our Country’s greatest ever Economy!

2021회계연도 예산에서 사회보장과 메디케어 유지 명시

### R3710 — include_extended / negative

> Saudi Arabia and Russia are arguing over the price and flow of oil. That, and the Fake News, is the reason for the market drop!

사우디와 러시아 원유가격 공급갈등을 증시하락 요인으로 지목, 새 미국정책 없음

### R3721 — exclude / na

> In the highly competitive world of high tech, how come nobody has ever challenged Mini Mike Bloomberg and his very average, &amp; supposedly outdated, “stuff” that he sells to so many? Did he use his position as Mayor of New York to create what is now a monopoly? Just askin’?

블룸버그 단말기 독점과 시장재임을 의문시하나 조사규제조치는 제시하지 않음

### R3744 — include_core / positive

> RT @SenJohnKennedy: I think Speaker Pelosi is having 2nd thoughts about impeaching the President. The Senate should get back to work on USM...

상원이 USMCA업무로 돌아가야 한다고 촉구하는 RT단편

### R3812 — include_core / mixed

> Just signed a new Executive Order to LOWER DRUG PRICES! My Most Favored Nation order will ensure that our Country gets the same low price Big Pharma gives to other countries. The days of global freeriding at America’s expense are over...

최혜국 약가행정명령 새서명을 명시, 소비자 약가인하와 제약업 수익영향 구별 필요

### R3813 — include_core / mixed

> ...and prices are coming down FAST! Also just ended all rebates to middlemen, further reducing prices.

중개인 리베이트 전면종료를 명시하므로 단순 가격전망과 구별

## 경계 판단

- R1415의 일반적 검열 비판과 R1549의 트위터 트렌드 불만은 구체 규제요구가 없어 제외했다. R1338은 Section 230을 직접 연결하고 R1563은 의회 규제 논의를 명시하여 별도로 보존했다.
- R3465는 FDA의 신속처리 요구만 있고 승인 대상이 본문에 없어 문맥보류했다. R3492는 Battelle와 마스크 살균장비를 명시하므로 개별 기업 승인압박으로 편입했다. 인접 글을 소급해 R3465의 대상을 확정하지 않았다.
- R2242는 Babylon Bee의 IV 식사 의무화 풍자이므로 실제 캘리포니아 보건정책으로 편입하지 않았다.
- R2725 등 JOBS 문구와 URL만 있는 글은 고용정책이나 긍정방향을 자동 확정하지 않았다.
- R1999와 R3812는 각각 최혜국 약가명령 유지와 새 서명이라는 다른 정보다. R3813의 리베이트 폐지는 글 자체에 조치가 명시되어 있으며 후속 시장반응을 사용하지 않았다.
- R3288 격리 검토는 당시의 미결정 상태로 판정했다. 이후의 격리 불필요 선언이나 여행권고를 거꾸로 적용하지 않았다.
