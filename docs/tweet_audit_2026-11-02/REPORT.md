# 트럼프 트윗 분류·누락 감사 보고서 — 2차 개별 원문 검토

GAM 팀프로젝트 · 검토기간 2026-11-02~2026-11-03 · 원본 데이터 보존

## 2차 검토 결과와 범위

1차에서 개별 의미 판독이 남았던 **24,556건 전부**를 분담하여 본문별로 검토하고 행별 근거를 저장했다. 기존 1,246건 및 1차 추가 후보 437건과 합치면 로컬 모집단 26,239건의 본문을 개별 열람한 범위가 된다. 연결 기사·이미지·영상의 복원까지 모두 완료했다는 뜻은 아니다.

| 2차 판단 | 건수 | 의미 |
| --- | ---: | --- |
| 경제·기업 정책 추가 분류 후보 | 471 | 무역·통화·외환·농가·기업 정책 관련 본문 및 경계 사례. 신규성·정밀 범주와 이벤트 중복을 확인해야 함 |
| 넓은 경제정책 범위 후보 | 3847 | 재정·거시·에너지·보건 등. 기존 무역 연구에 자동 합산하지 않음 |
| 본문상 제외 | 16611 | 정치·개인·행사 등으로 판단한 행; 근거는 개별 원장 참조 |
| 문맥 복원 필요 | 3627 | 링크·인용·생략으로 포함 여부나 부호 미확정. 누락 없음으로 처리하지 않음 |

이 수치는 1차의 추가 분류 필요 59건 및 기존 분류 재검토 152건과 별도 모집단의 결과다. 후보 글 수는 독립된 정책사건 수가 아니며, 재게시·스레드·RT가 포함된다. 시장 반응으로 부호를 정하지 않았고 원본 라벨·시장 자료를 수정하지 않았다.

`include_core`는 후속 분류에서 우선 검토할 경제정책 후보를 뜻한다. 원래의 무역·연준 표본에 모두 자동 편입할 확정 명단은 아니다. 제재·기술규제·기업계약 등 연구 범위의 경계 사례도 테마와 근거를 남겼다. `direction` 역시 사후 주가의 상승·하락이 아니라 본문상 완화·강화·지원·압박 방향의 잠정 판단이다. 소비자와 기업의 이해가 다르거나 대상·조건을 확정할 수 없으면 mixed/uncertain으로 기록했다.

분담 검토는 각 글을 서로 다른 담당자에게 배정한 방식이다. 모든 글에 대한 두 명의 독립 평가·합의를 수행한 것은 아니며, 평가자 간 일치도나 분류 정확도를 산출하지 않았다. 원장에는 판단 당시의 근거를 남겨 재검토할 수 있게 했다.

**해석:** 전량 본문 검토를 마쳤더라도 문맥 복원 필요 행이 있으므로 ‘정책 관련 누락이 더 없다’는 무조건적인 보증은 할 수 없다. 확인된 추가 후보를 분류 대상에 올리고, 미확정 글을 별도 추적하는 것이 감사 결과다.

## 새로 확인한 주요·애매 사례

## root 검토: 키워드 없는 핵심 정책·애매 사례

### R60: Trade_Brexit

> RT @Brexit: BREAKING: Boris Johnson says the U.K. will now get ready to split from the EU’s single market and customs union without a new t…

판정: include_core / negative

근거: 영국의 EU 단일시장·관세동맹 이탈과 새 합의 없는 분리를 전하는 RT이다. 무역 불확실성 관련성이 명시되어 누락 후보로 포함하되 잘린 RT 전체 복원이 필요하다.

### R198: Tech_Regulator_Personnel

> Nate Simington, a very smart and qualified individual, is having his Senate hearing today. Republicans will hopefully confirm him to the FCC ASAP! We need action NOW on this very important nomination!! @SenatorWicker @MarshaBlackburn @senatemajldr

판정: include_core / uncertain

근거: FCC 위원 Nate Simington의 인준을 촉구한다. 기업·기술규제 인선 정보로 보존하되 현재 기업에 대한 직접 제재나 주가 부호를 확정하지 않는다.

### R234: Technology_Regulation

> For purposes of National Security, Section 230 must be immediately terminated!!!

판정: include_core / negative

근거: 국가안보를 이유로 Section 230의 즉각 폐지를 요구한다. 기술기업 책임 규제 방향이 명시되어 기존 기업압박 범위의 누락 후보다.

### R398: Fiscal_Industry_Aid

> The restaurant business is being absolutely decimated. Congress should step up and help. Time is of the essence!

판정: include_extended / positive

근거: 식당업 피해를 지적하고 의회에 긴급지원을 요청한다. 특정 산업 지원 요구이나 구체적 금액·확정 시행은 없어 제안 단계다.

### R441: Company_Public_Contract_Health

> RT @WhiteHouse: JUST ANNOUNCED: We have finalized a partnership with @CVSHealth and @Walgreens to deliver the Coronavirus vaccine, when app…

판정: include_core / positive

근거: CVS Health·Walgreens와 백신 유통 파트너십 최종화를 발표한 RT이다. 회사·수요가 구체적이나 전체 계약과 신규성은 추가 확인한다.

### R458: Fiscal_Infrastructure

> $13.9M is heading to New Orleans in @USDOT funding for @NewOrleansRTA! Happy to support bus service and major fleet improvements for the great people of Louisiana and help them keep moving safely.

판정: include_extended / positive

근거: 뉴올리언스 버스·차량 개선을 위해 USDOT 자금 13.9백만 달러 배정을 발표한다. 지역 재정·인프라 정책 정보다.

### R466: Fiscal_Stimulus_Negotiation

> Just don’t see any way Nancy Pelosi and Cryin’ Chuck Schumer will be willing to do what is right for our great American workers, or our wonderful USA itself, on Stimulus. Their primary focus is BAILING OUT poorly run (and high crime) Democrat cities and states....

판정: include_extended / negative

근거: 코로나 부양책 협상과 민주당 지방정부 구제 요구를 직접 비판한다. 단순 선거 비난과 구분해 재정협상 차질 정보로 보존한다.

### R473: Sanctions_Relief

> GREAT news! New government of Sudan, which is making great progress, agreed to pay $335 MILLION to U.S. terror victims and families. Once deposited, I will lift Sudan from the State Sponsors of Terrorism list. At long last, JUSTICE for the American people and BIG step for Sudan!

판정: include_core / positive

근거: 수단의 335백만 달러 피해보상 입금 시 테러지원국 명단에서 해제하겠다는 조건부 제재완화 발표다. 외교행사만이 아닌 제재조건을 명시한다.


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


# part_1 개별 검토 완료 사례

검토 범위: part_1.csv 전체 6,139행. 이전 검토 원장을 유지하고 잔여 원문을 개별 열람해 최종 판정을 추가했다. 아래에는 검토 시점별 주요 경계 사례를 보존한다. needs_context는 연결 대상·잘린 원문을 확인하기 전까지 확정하지 않은 판정이다.

## R6438

Don’t worry, wonderful &amp; beautiful Alaska, there will be NO POLITICS in the Pebble Mine Review Process. I will do what is right for Alaska and our great Country!!!

판정: uncertain; Pebble 광산 심사에 정치 개입하지 않겠다는 약속; 허가 결과는 미확정


## R6453

....Twitter is completely stifling FREE SPEECH, and I, as President, will not allow it to happen!

판정: uncertain; Twitter 표현 제한을 대통령이 허용하지 않겠다는 압박; 후속 문맥과 조치 강도 확인 필요


## R6529

RT @WhiteHouse: On October 1, 2018, President @realDonaldTrump announced that negotiations on the United States-Mexico-Canada Agreement wer…

판정: positive; United States-Mexico-Canada Agreement 협상 발표를 회고하는 RT; USMCA 약자 없이도 명확한 무역합의 문맥


## R6621

RT @jsolomonReports: President Trump blasts Twitter after the platform disputed the accuracy of two of his tweets | Just The News https://t…

판정: uncertain; Twitter가 트윗 정확성을 표시한 뒤 대통령이 비난했다는 RT; 명시 조치·규모는 미제시


## R6656

....happen again. Just like we can’t let large scale Mail-In Ballots take root in our Country. It would be a free for all on cheating, forgery and the theft of Ballots. Whoever cheated the most would win. Likewise, Social Media. Clean up your act, NOW!!!!

판정: uncertain; 우편투표 비판과 함께 소셜미디어에 개선을 요구하는 후속 글; 대상·조치 세부는 앞 문맥 필요


## R6670

Republicans feel that Social Media Platforms totally silence conservatives voices. We will strongly regulate, or close them down, before we can ever allow this to happen. We saw what they attempted to do, and failed, in 2016. We can’t let a more sophisticated version of that....

판정: negative; 보수 목소리 제한을 이유로 소셜미디어 플랫폼 강력 규제 또는 폐쇄를 직접 위협


## R6683

Yesterday I spoke with the great American Grocers and Supply Chain Executives. We are confident that supply will continue to meet demand nationwide. These beacons of our community will remain open for you, no matter what. We are working hard to remove any barriers to that effort!

판정: uncertain; 식품유통·공급망 기업들과 협의하고 공급 장벽 제거 및 영업 유지 의지를 밝힘


## R6705

This morning, 450,000 protective suits landed in Dallas, Texas. This was made possible because of the partnership of two great American companies—DuPont and FedEx—and our friends in Vietnam. Thank you! @DuPont_News @FedEx https://t.co/8yhG6tYnQW

판정: positive; DuPont·FedEx와 Vietnam의 협력으로 방호복 45만벌 Dallas 도착 발표


## R6707

I saved the Iron Range from the Obama Closure. We opened it up again, proudly. Also sent the National Guard the Minneapolis to squelch a big problem. It worked, and quickly!!! https://t.co/v8mkiawBy5

판정: uncertain; Iron Range 폐쇄를 막고 재개했다고 주장하는 성과 홍보; 신규성은 확인 필요


## R6818

Twitter has now shown that everything we have been saying about them (and their other compatriots) is correct. Big action to follow!

판정: uncertain; Twitter에 대한 큰 조치가 뒤따를 것이라고 예고; 구체 제재는 미공개


## R6881

RT @Mike_Pence: President @realDonaldTrump promised the American people that he would bring back jobs and bring back manufacturing. He kept…

판정: uncertain; 제조업·일자리 복귀 공약 이행을 주장하는 Pence RT; 신규 조치인지 확인 필요


## R6883

RT @realDonaldTrump: This morning, 450,000 protective suits landed in Dallas, Texas. This was made possible because of the partnership of t…

판정: positive; 방호복 45만벌 Dallas 도착 및 기업 협력을 재전달하는 자기 RT; 최초 정보 아님


## R6899

RT @Mike_Pence: Under President @realDonaldTrump’s leadership, more than 90 percent of the regulations that @ShopFloorNAM identified as hur…

판정: uncertain; 제조업협회가 유해하다고 지목한 규제의 90% 이상에 관한 조치를 홍보하는 RT; 잘린 원문에서 세부 확인 필요


## R6965

Big Tech is doing everything in their very considerable power to CENSOR in advance of the 2020 Election. If that happens, we no longer have our freedom. I will never let it happen! They tried hard in 2016, and lost. Now they are going absolutely CRAZY. Stay Tuned!!!

판정: uncertain; Big Tech 검열을 허용하지 않겠다는 대통령 발언과 후속 예고; 구체 규제 미공개


## R7005

RT @WhiteHouse: President @realDonaldTrump spoke with executives from America’s fast food companies to discuss the important role that driv…

판정: uncertain; 패스트푸드 기업 경영진과 드라이브스루 등의 역할을 논의한 RT; 구체 지원·명령 미상


## R7291

Sleepy Eyes Chuck Todd should be FIRED by “Concast” (NBC) for this fraud. He knew exactly what he was doing. Public Airwaves = Fake News! @AjitPaiFCC  @FCC https://t.co/fLTDhjMXo4

판정: uncertain; Chuck Todd 해고 요구와 공공전파 문제를 거론하면서 FCC·위원장을 직접 태그; 실제 규제명령 미확정


### R7448: Company_Pharma_Price_Regulation

> I am SUBSTANTIALLY LOWERING MEDICARE PREMIUMS. Have instituted Favored Nations Clause and Rebates on Drug Companies. Never been done before. Drug companies are hitting me with Fake Ads, just like sleepy Joe. Be careful! Drug prices will be reduced massively, and soon.

판정: include_core / negative

근거: 제약회사에 대한 최혜국 조항과 리베이트 제도 시행 및 약가·보험료 인하를 명시한다. 단순 제약업계 비난이 아닌 규제 내용이 있다.

### R7471: Technology_Platform_Regulation

> RT @WhiteHouse: The Trump Administration is making sure your taxpayer dollars don't go to social media giants that unfairly repress free sp…

판정: include_core / negative

근거: 소셜미디어 검열 관련 행정명령·정부지출 제한·법무부 주정부 집행 지시 등 구체적 기업규제 문맥을 전한다. RT 원문과 명령 범위 확인이 필요하다.

### R7548: Trade_Export_Regulation

> ....I have seen some of the regulations being circulated, including those being contemplated by Congress, and they are ridiculous. I want to make it EASY to do business with the United States, not difficult. Everyone in my Administration is being so instructed, with no excuses...

판정: include_core / positive

근거: 국가안보를 이유로 외국의 미국 제품 구매를 어렵게 하는 규제를 비판하고 행정부에 거래를 쉽게 하라고 지시하는 연속 글이다. 수출규제 완화 방향이며 스레드의 최초 공개시각과 조치 범위 확인이 필요하다.

### R7554: Trade_Export_Regulation

> The United States cannot, &amp; will not, become such a difficult place to deal with in terms of foreign countries buying our product, including for the always used National Security excuse, that our companies will be forced to leave in order to remain competitive. We want to sell...

판정: include_core / positive

근거: 국가안보를 이유로 외국의 미국 제품 구매를 어렵게 하는 규제를 비판하고 행정부에 거래를 쉽게 하라고 지시하는 연속 글이다. 수출규제 완화 방향이며 스레드의 최초 공개시각과 조치 범위 확인이 필요하다.

### R7693: Technology_Regulation

> “Regulate Twitter if they are going to start regulating free speech.” @JudgeJeanine @foxandfriends  Well, as they have just proven conclusively, that’s what they are doing. Repeal Section 230!!!

판정: include_core / negative

근거: Twitter 규제 및 Section230 폐지를 직접 요구한다. 단순 플랫폼 비난보다 구체적인 법적 책임보호 폐지 방향이 명시된다.

### R7707: Cross_Border_Rail_Permit

> Based on the strong recommendation of @SenDanSullivan and @repdonyoung of the Great State of Alaska, it is my honor to inform you that I will be issuing a Presidential Permit for the A2A Cross-Border Rail between Alaska &amp; Canada. Congratulations to the people of Alaska &amp; Canada!

판정: include_core / positive

근거: Alaska와 Canada 사이 A2A 국경간 철도에 대통령 허가를 발급하겠다고 발표한다. 실제 국경간 운송 인프라 허가로 무역·산업 문맥이 구체적이다.

### R7755: Technology_Regulation

> REVOKE 230!

판정: include_core / negative

근거: REVOKE230이라는 직접적인 법적 책임보호 폐지 요구다. 문구는 짧지만 Section230 정책대상이 특정된다.

### R8235: Energy_OPEC_Deal

> The big Oil Deal with OPEC Plus is done. This will save hundreds of thousands of energy jobs in the United States. I would like to thank and congratulate President Putin of Russia and King Salman of Saudi Arabia. I just spoke to them from the Oval Office. Great deal for all!

판정: include_extended / positive

근거: OPEC Plus 석유합의 완료 및 미국 에너지 일자리 보호를 발표한다. 구체 에너지 정책으로 무역·연준 핵심과 구분한 별도층에 포함한다.

### R8286: Fishing_Industry_Deregulation

> It was my great honor to free up 5000 square miles of ocean off the coast of Maine. Enjoy!

판정: include_core / positive

근거: Maine 연안 5000제곱마일을 개방했다고 구체 면적을 명시한다. 어업 접근 규제완화로 기존 산업정책 범위와 연결해 검토한다.

### R8411: Technology_Regulation

> If Big Tech persists, in coordination with the mainstream media, we must immediately strip them of their Section 230 protections. When government granted these protections, they created a monster! https://t.co/velyvYTOR0

판정: include_core / negative

근거: BigTech가 행동을 지속하면 즉시 Section230 보호를 박탈해야 한다고 명시한다. 조건부 법적책임 규제 위협이다.

### R8421: Company_Tesla_Reopening

> California should let Tesla &amp; @elonmusk open the plant, NOW. It can be done Fast &amp; Safely!

판정: include_core / positive

근거: California에 Tesla와 Elon Musk의 공장을 즉시 재개하도록 직접 요구한다. 기업의 구체 영업규제 완화 요구로 포함한다.

### R8427: Monetary_Negative_Rates

> As long as other countries are receiving the benefits of Negative Rates, the USA should also accept the “GIFT”. Big numbers!

판정: include_core / positive

근거: 다른 나라의 마이너스 금리 혜택을 미국도 받아야 한다고 요구한다. Fed 키워드가 없어도 통화완화 방향이 구체적이며 주식·은행 공통 호재를 뜻하지 않는다.

### R8528: Industry_Manufacturing_Contract

> Landing in Wisconsin. Launching big new ship contract!

판정: include_core / positive

근거: Lordstown 차량제조 또는 Wisconsin 조선소 계약·1500명 유지와1000명 추가고용을 전한다. 회사·산업 생산 및 수요 문맥이 구체적이나 원계약과 RT신규성은 확인해야 한다.

### R8553: Industry_Manufacturing_Contract

> RT @WhiteHouse: "This contract will support your 1,500 full-time employees, and it will also enable you to hire another 1,000 people all ac…

판정: include_core / positive

근거: Lordstown 차량제조 또는 Wisconsin 조선소 계약·1500명 유지와1000명 추가고용을 전한다. 회사·산업 생산 및 수요 문맥이 구체적이나 원계약과 RT신규성은 확인해야 한다.


## 최종 잔여 원문 검토에서 추가한 경계 사례

### R11521

> Great News! Randall Stephenson, the CEO of heavily indebted AT&amp;T, which owns and presides over Fake News @CNN, is leaving, or was forced out. Anyone who lets a garbage “network” do and say the things that CNN does, should leave ASAP. Hopefully replacement will be much better!

판정: include_extended / uncertain · Company_Commentary

근거: AT&T CEO Stephenson 퇴임과 CNN보도를 비난한다. 회사 경영진 비판이지만 새로운 제재·행정조치는 없어 기업 논평으로 구분한다.

### R11578

> RT @SenJoniErnst: #ICYMI Iowa leaders send letter petitioning @USDA to provide CFAP funds to egg producers https://t.co/wzPJ4UcD30

판정: include_core / positive · Farm_Aid

근거: USDA에 계란 생산자 CFAP지원을 요청하는 서한을 전달한다. farmers 없이 명확한 농업구제금융 지원 요구가 나타난 후보.

### R11712

> RT @WhiteHouse: "Today, my Administration reached a historic agreement with Pfizer, to produce and deliver 100 million doses of their vacci…

판정: include_core / positive · Company_Vaccine_Contract

근거: 정부가 Pfizer와 백신1억회분 생산·공급 합의를 맺었다고 알리는 RT이다. 기업 계약·보건공급 확대라는 구체정보가 있으나 세부조건은 원문복원 필요.

### R11865

> RT @LindseyGrahamSC: Great news for South Carolina and a compliment to the @weareboeingsc workforce!
> 
> This would never have come to pass ha…

판정: needs_context / uncertain · Company_Boeing

근거: Boeing SouthCarolina인력을 칭찬하는 RT이나 어떤 합의·조치를 가리키는지 잘려 있다. 본문만으로 기업 정책사건을 확정할 수 없다.

### R11918

> RT @MarketWatch: Pharma stocks finish lower as Trump targets drug prices with executive orders https://t.co/s9imYC0dLq

판정: include_core / mixed · Pharmaceutical_Price_Regulation

근거: 약가를 겨냥한 행정명령 보도 RT이다. 사후 제약주 등락을 라벨 근거로 사용하지 않고 소비자 약가와 기업규제를 구분한다.

### R12020

> Great job by @elonmusk in agreeing to build, in TEXAS, what is expected to be the largest auto plant anywhere in the world. He kept his word to me. Texas &amp; @Tesla are big winners. MADE IN THE USA!

판정: include_core / positive · Company_Investment

근거: ElonMusk가 Texas에 대규모 Tesla자동차 공장 건설에 합의했다고 직접 밝힌다. Apple/Boeing 없이 명확한 미국내 기업투자 발표가 있는 누락 후보.

### R12044

> RT @TeamTrump: President @realDonaldTrump: “We will finally allow the safe and legal importation of prescription drugs from Canada and othe…

판정: include_core / mixed · Pharmaceutical_Import_Price_Regulation

근거: 처방약 수입 허용·약가인하 행정명령·서명조치 또는 그 후속 효과를 언급한다. 소비자 가격과 제약기업 영향의 부호를 분리하고 후속글은 사건중복을 확인한다.

### R12138

> Yesterday I signed four measures that will massively reduce the prices of prescription drugs, in many cases by more than 50%. Nothing like this has ever been done before because Big Pharma, with its vast power, would not let it happen. Expensive Insulin went from big dollars.....

판정: include_core / mixed · Pharmaceutical_Import_Price_Regulation

근거: 처방약 수입 허용·약가인하 행정명령·서명조치 또는 그 후속 효과를 언급한다. 소비자 가격과 제약기업 영향의 부호를 분리하고 후속글은 사건중복을 확인한다.

### R12162

> Nancy Pelosi is asking for $2.4 Trillion Dollars to bailout poorly run, high crime, Democrat States, money that is in no way related to COVID-19. We made a very generous offer of $1.6 Trillion Dollars and, as usual, she is not negotiating in good faith. I am rejecting their...

판정: include_extended / uncertain · Fiscal_Macro_Industry

근거: 임금세·실업급여·PPP·지방정부구제·성장·부양협상·경제재개·에너지·주거규제·재난지원을 다룬 경제 발언이다. 무역/연준 직접충격과 구분한 확장 후보이며 실행·제안·회고의 신규성을 별도 확인한다.

### R12164

> ...request, and looking to the future of our Country. I have instructed my representatives to stop negotiating until after the election when, immediately after I win, we will pass a major Stimulus Bill that focuses on hardworking Americans and Small Business. I have asked...

판정: include_extended / uncertain · Fiscal_Macro_Industry

근거: 임금세·실업급여·PPP·지방정부구제·성장·부양협상·경제재개·에너지·주거규제·재난지원을 다룬 경제 발언이다. 무역/연준 직접충격과 구분한 확장 후보이며 실행·제안·회고의 신규성을 별도 확인한다.

### R12329

> The House &amp; Senate should IMMEDIATELY Approve 25 Billion Dollars for Airline Payroll Support, &amp; 135 Billion Dollars for Paycheck Protection Program for Small Business. Both of these will be fully paid for with unused funds from the Cares Act. Have this money. I will sign now!

판정: include_extended / positive · Fiscal_Airline_PPP_Support

근거: 항공사 급여지원250억달러와PPP1350억달러를 CARES미사용재원으로 즉시승인·서명하겠다고 구체적으로 제안한다. 기업명없는산업지원 누락후보.

### R12338

> If I am sent a Stand Alone Bill for Stimulus Checks ($1,200), they will go out to our great people IMMEDIATELY. I am ready to sign right now. Are you listening Nancy? @MarkMeadows @senatemajldr @kevinomccarthy @SpeakerPelosi @SenSchumer

판정: include_extended / positive · Fiscal_Direct_Payments

근거: 1200달러 직접지원 단독법안을 보내면 즉시서명·지급하겠다고 밝힌다. 정책금액과 조건이 구체적인 재정지원 제안이다.

### R12501

> RT @WhiteHouse: Our 33rd use of the Defense Production Act will mobilize Kodak to make generic, active pharmaceutical ingredients. https://…

판정: include_core / positive · Company_Kodak_DPA

근거: DPA의33번째사용으로Kodak을제네릭원료의약품 생산에 동원한다고 명시한다. 기업·생산정책 핵심누락 후보이나RT전체조건은복원해야한다.

### R12521

> Support Patio Pizza and its wonderful owner, Guy Caligiuri, in St. James, Long Island (N.Y.). Great Pizza!!! @Varneyco

판정: include_extended / positive · Company_Endorsement

근거: PatioPizza와점주를지원하라고공개추천한다. 직접회사언급이지만무역·행정규제아닌 소비추천이므로광의기업층이다.

### R12600

> So disgusting to watch Twitter’s so-called “Trending”, where sooo many trends are about me, and never a good one. They look for anything they can find, make it as bad as possible, and blow it up, trying to make it trend. Really ridiculous, illegal, and, of course, very unfair!

판정: include_extended / negative · Company_Twitter_Criticism

근거: Twitter Trending이 자신에게 불리하고 불법이라고 비난하지만 구체적 제재·법 개정 지시는 없다.

### R12671

> Payroll Tax Cut plus Dollars!

판정: include_extended / positive · Fiscal_Payroll_Tax

근거: Payroll Tax Cut plus Dollars라는 급여세 감면·현금 지원 요구이다. 간결하지만 정책 수단이 명시된다.

### R12682

> RT @WhiteHouse: We have reached a historic deal with @Kodak to begin producing critical pharmaceutical ingredients right here in America! h…

판정: include_core / positive · Company_Kodak_DPA

근거: Kodak의 미국 내 필수 의약품 원료 생산 협정 또는 7억6500만달러 지원 합의를 명시한다. 동일 행사 RT를 새 계약으로 중복 세지 않는다.

### R12701

> RT @LouDobbs: Tackling the Pandemic: @realDonaldTrump announces a historic $765m deal with Kodak to bring medical manufacturing back to the…

판정: include_core / positive · Company_Kodak_DPA

근거: Kodak의 미국 내 필수 의약품 원료 생산 협정 또는 7억6500만달러 지원 합의를 명시한다. 동일 행사 RT를 새 계약으로 중복 세지 않는다.

### R12728

> When we win I, as your President, will totally forgive ALL deferred payroll taxes with money from the General Fund. I will ALWAYS protect Seniors and your Social Security! Sleepy Joe Biden will do the opposite, he will raise your taxes and DESTROY our Country!

판정: include_extended / positive · Fiscal_Payroll_Tax

근거: 재선 시 유예된 급여세를 일반회계 재원으로 모두 면제하겠다는 구체적 공약이다. 이미 면제된 세금으로 처리하면 안 된다.

### R12756

> Congratulations to JPMorgan Chase for ordering everyone BACK TO OFFICE on September 21st. Will always be better than working from home!

판정: include_extended / positive · Company_JPMorgan_Operations

근거: JPMorgan Chase의 9월21일 사무실 복귀 지시를 축하한다. 금융규제·정부의 회사 강제명령은 아니다.

### R12779

> Texarkana Regional Airport has a major grant coming its way from @USDOT. I’m designating $3.6 million to reconstruct its terminal building, in addition to 5 more airport grants around the State. Glad to help the people of Arkansas!

판정: include_extended / positive · Fiscal_Airport_Grants

근거: USDOT의 공항 터미널·유도로·안전 개선 보조금 배정을 금액과 함께 발표한다. 특정 민간기업 투자 압박과 구분한다.

### R12801

> If Congress doesn’t bring fairness to Big Tech, which they should have done years ago, I will do it myself with Executive Orders. In Washington, it has been ALL TALK and NO ACTION for years, and the people of our Country are sick and tired of it!

판정: include_core / negative · BigTech_Executive_Order_Threat

근거: 의회가 Big Tech에 공정성을 부과하지 않으면 본인이 행정명령으로 하겠다고 위협한다. 구체적 명령 서명·시행 확정과 구분한다.

### R12806

> ...Your housing prices will go up based on the market, and crime will go down. I have rescinded the Obama-Biden AFFH Rule. Enjoy!

판정: include_extended / mixed · Housing_AFFH_Repeal

근거: AFFH 규칙 철회와 교외 저소득 주택 부담 감소를 주장한다. 교외 집주인 가격 주장과 저소득 주택 접근 영향이 달라 혼합이다.

### R12826

> Great honor to have the endorsement of the Governor of Puerto Rico, Wanda Vázquez Garced. As I have always said, Donald J. Trump is the best thing to ever happen to the people of Puerto Rico. The drug manufacturers are now coming back. Biden ended that program! @wandavazquezg

판정: include_extended / positive · Pharma_Manufacturing_Reshoring

근거: 푸에르토리코 제약 제조업체가 돌아오고 있다고 주장한다. 지지 선언 문맥이며 특정 업체·금액·신규 투자 확정은 없다.



전체 범위: part_2.csv 6,139행 원문 개별 검토 완료. 링크·문맥 부족 사례는 needs_context로 남겼다.

## part 2: 기업명·협정명 없는 글과 비영어 원문

### R12887 · ['Fiscal_COVID']

> Covid Relief Negotiations are moving along. Go Big!

판정: include_extended / positive

근거: 코로나 구호 협상이 진전 중이라 알리며 규모 확대를 요구

### R12913 · ['Health_Price_Regulation']

> When you see the Drug Companies taking massive  television ads against me, forget what they say (which is false), YOU KNOW THAT DRUG PRICES ARE COMING DOWN, BIG. Favored Nations Clause means USA will pay the lowest price of any nation in the World. Never done before. Watch!!!

판정: include_extended / uncertain

근거: 약가에 최혜국 조항을 적용해 최저 수준으로 낮춘다고 설명; 소비자와 제약사 영향 상이

### R13258 · ['Firm_Financial_Regulation']

> Fines and penalties against Wells Fargo Bank for their bad acts against their customers and others will not be dropped, as has incorrectly been reported, but will be pursued and, if anything, substantially increased. I will cut Regs but make penalties severe when caught cheating!

판정: include_core / negative

근거: Wells Fargo 제재가 철회된다는 보도를 부인하고 벌금·제재 증액 추진을 명시; 구체 기업의 규제 부담 정보

### R13311 · ['Industry_Commercial_Deal']

> Today, it was my great honor to meet with the Crown Prince of Bahrain at the @WhiteHouse. Bahrain and the United States are important partners.During the Crown Prince’s visit, he is advancing $9 BILLION in commercial deals, including finalizing the purchase of F-16’s... https://t.co/vYuw7UGYmN

판정: include_core / positive

근거: 바레인 왕세자 방미에서 90억 달러 상업계약과 F-16 구매 마무리를 발표; 신규 조달·수요 관련 문맥

### R13735 · ['Macro_Fiscal_Regulatory']

> Money pouring into Insurance Companies profits, under the guise of ObamaCare, is over. They have made a fortune.Dems must get smart &amp, deal!

판정: include_extended / uncertain

근거: 거시지표·감세·보험보조금·규제완화·정부재정 등 확대 범위 경제정보를 포함. 실행 조치와 성과 홍보·정치 수사를 구분해야 함. 식별 문구: Money pouring into Insurance Companies profits, under the guise of ObamaCare, is over. They have made a fortune.Dems mus

### R13748 · ['Macro_Fiscal_Regulatory']

> The Democrats ObamaCare is imploding. Massive subsidy payments to their pet insurance companies has stopped. Dems should call me to fix!

판정: include_extended / uncertain

근거: 거시지표·감세·보험보조금·규제완화·정부재정 등 확대 범위 경제정보를 포함. 실행 조치와 성과 홍보·정치 수사를 구분해야 함. 식별 문구: The Democrats ObamaCare is imploding. Massive subsidy payments to their pet insurance companies has stopped. Dems should

### R13761 · ['Media_License_Regulation']

> Network news has become so partisan, distorted and fake that licenses must be challenged and, if appropriate, revoked. Not fair to public!

판정: include_core / negative

근거: 방송 뉴스의 편파성을 이유로 면허 이의제기와 적절할 경우 취소를 요구; 단순 언론 비난보다 구체 규제 위협

### R14314 · ['Firm_Price_Pressure']

> .@Merck Pharma is a leader in higher &amp, higher drug prices while at the same time taking jobs out of the U.S. Bring jobs back &amp, LOWER PRICES!

판정: include_core / negative

근거: Merck를 직접 지목해 약가 상승과 해외 일자리 이전을 비난하고 국내복귀·가격인하 요구

### R14406 · ['Industry_Investment']

> Toyota &amp, Mazda to build a new $1.6B plant here in the U.S.A. and create 4K new American jobs. A great investment in American manufacturing!

판정: include_core / positive

근거: Toyota·Mazda의 미국16억 달러 공장 및4000개 일자리 투자 발표

### R14462 · ['Industry_Investment']

> Thank you Foxconn, for investing $10 BILLION DOLLARS with the potential for up to 13K new jobs in Wisconsin! MadeInTheUSA🇺🇸 https://t.co/jJghVeb63s

판정: include_core / positive

근거: Foxconn100억 달러 투자와 최대13000개 일자리를 구체적으로 제시

### R14529 · ['Industry_Investment']

> Billions of dollars in investments &amp, thousands of new jobs in America! An initiative via Corning, Merck &amp, Pfizer: https://t.co/QneN48bSiq https://t.co/5VtMfuY3PM

판정: include_core / positive

근거: Corning·Merck·Pfizer의 미국 수십억 달러 투자와 수천개 일자리 프로젝트 발표

### R14682 · ['Trade_Deal']

> New Sugar deal negotiated with Mexico is a very good one for both Mexico and the U.S. Had no deal for many years which hurt U.S. badly.

판정: include_core / positive

근거: 멕시코와 새 설탕 협상을 체결했다고 명시; Sugar deal로 기존 trade deal 키워드 밖 통상 합의

### R15288 · ['Industry_Investment']

> Thank you to @exxonmobil for your $20 billion investment that is creating more than 45,000 manufacturing &amp, construction jobs in the USA!

판정: include_core / positive

근거: 원문에 미국 내 투자금액·일자리 또는 자동차 생산유치가 명시된다. 특히 Exxon Mobil의 200억 달러 투자와 4만5천 일자리는 구체적 산업 수요 정보다. 익명 기업·선행 발표·단편의 신규성은 추가 확인한다.

### R15422 · ['Company_Investment_Intel']

> Thank you Brian Krzanich, CEO of @Intel. A great investment ($7 BILLION) in American INNOVATION and JOBS!... https://t.co/oicfDsPKHQ

판정: include_core / positive

근거: Intel CEO Brian Krzanich와 미국 내 70억 달러 투자·일자리를 명시한다. 기존 산업투자 범위에 맞는 회사명 사전 밖 후보다.

### R15425 · ['Company_Pressure_Nordstrom']

> My daughter Ivanka has been treated so unfairly by @Nordstrom. She is a great person -- always pushing me to do the right thing! Terrible!

판정: include_core / negative

근거: Nordstrom이 Ivanka를 부당하게 대우했다고 기업명을 직접 비난한다. 직접 제재는 아니지만 기존 기업압박 범위에서 개인적 이해관계와 정책강도를 구분해 보존한다.

### R15574 · ['Border_Closure_Threat']

> We will be forced to close the Southern Border entirely if the Obstructionist Democrats do not give us the money to finish the Wall &amp, also change the ridiculous immigration laws that our Country is saddled with. Hard to believe there was a Congress &amp, President who would approve!

판정: include_core / negative

근거: 국경장벽 예산 미확보 시 남부 국경 전체 폐쇄를 강제하겠다는 조건부 위협이다. 통상 물류 영향 가능성은 있지만 상품무역 예외와 시행범위는 미확정이다.

### R15611 · ['Farm_Bill_Legislation']

> We signed two pieces of major legislation this week, Criminal Justice Reform and the Farm Bill. These are two Big Deals, but all the Fake News Media wants to talk about is “the mistake” of bringing our young people back home from the Never Ending Wars. It all began 19 years ago!

판정: include_core / positive

근거: 농업법 서명 또는 서명예고를 명시한다. 농가 정책 범위에 맞고 Farm Bill이라는 표현만 있어 기존 farmers 검색이 놓칠 수 있는 후보다.

### R15720 · ['Company_Investment_Tim_Cook']

> Thank you to @tim_cook for agreeing to expand operations in the U.S. and thereby creating thousands of jobs! https://t.co/2zOVxp9nTF

판정: include_core / positive

근거: @tim_cook이 미국 사업 확장과 수천 일자리 창출에 합의했다고 명시한다. Apple이라는 단어 없이도 기업투자 실질 문맥이 있으나 연결 원문의 투자금액·신규성은 보완한다.

### R15836 · ['Trade_Agreement_Mexico']

> RT @EPN: En mi último día como Presidente, me siento muy honrado de haber participado en la firma del nuevo Tratado Comercial entre México,...

판정: include_core / positive

근거: 멕시코 대통령 EPN의 스페인어 RT는 멕시코 간 새 무역협정 서명에 참여한 사실을 명시한다. 영어 trade/USMCA 키워드 없이도 무역합의 관련성이 확인된다.


## 최종 잔여 원문 검토에서 추가한 경계 사례

### R19295

> Iran wanted me to lift the sanctions imposed on them in order to meet. I said, of course, NO!

판정: include_core / negative · Iran_Sanctions

근거: 회담 조건으로 이란이 요구한 제재 해제를 거절했다고 명시한다. 신규 제재 부과가 아니라 기존 제재 유지·협상 거부이다.

### R19320

> RT @realDonaldTrump: They were just upset that I demanded they pay their fair share for NATO. Their countries are delinquent. I raised $530...

판정: include_extended / positive · NATO_Burden_Sharing

근거: NATO 동맹국의 공정한 방위비 부담을 요구해 530으로 시작하는 금액을 늘렸다는 잘린 RT이다. 실제 단위·총액은 복원 전 확정하지 않는다.

### R19363

> Wow! All of our priorities have made it into the final NDAA: Pay Raise for our Troops, Rebuilding our Military, Paid Parental Leave, Border Security, and Space Force! Congress – don’t delay this anymore! I will sign this historic defense legislation immediately!

판정: include_extended / positive · Defense_Authorization

근거: NDAA 합의·임금 인상·유급 육아휴직·우주군을 지지한다. 19363은 즉시 서명 의사이지 서명 완료가 아니다.

### R19392

> They were just upset that I demanded they pay their fair share for NATO. Their countries are delinquent. I raised $530 Billion more from NATO countries! Thank you Charles. https://t.co/1klX5GtK8r

판정: include_extended / positive · NATO_Burden_Sharing

근거: NATO 동맹국에 공정 부담을 요구해 5300억달러를 더 확보했다고 주장한다. 미국 무역흑자나 즉시 현금 수입으로 해석하지 않는다.

### R19446

> RT @GOPLeader: The US-Mexico-Canada Agreement is a win for the American worker and has been since the day President Trump signed it over a...

판정: include_core / positive · Trade_USMCA

근거: 미국·멕시코·캐나다 협정 USMCA가 노동자에게 이익이라는 공화당 원내대표 RT이다. 신규 서명·비준 완료일로 사용하지 않는다.

### R19448

> On my way to Hershey, Pennsylvania for a rally. See everyone soon. I love Hershey chocolate! https://t.co/bDUYBK8KRc

판정: exclude / na · Political_Personal_Ceremonial

근거: 선거·정치 공방, 지지·감사, 이동·행사 또는 개인 논평이다. 본문에 무역·통화·기업·농가 조치가 제시되지 않아 현행 정책 사건에서 제외한다.

추가 주의: Hershey는 집회 방문 도시이자 초콜릿 브랜드 언급이다. 초콜릿을 좋아한다는 문장은 관세·제조 투자 압박이 아니므로 기업명 키워드만으로 포함하지 않는다.

### R19473

> RT @WhiteHouse: President @realDonaldTrump has asked Congress to pass a federal tax credit to support state-based scholarship programs and...

판정: include_extended / positive · Fiscal_Education_Tax_Credit

근거: 주정부 장학금 프로그램 지원 연방 세액공제를 의회에 통과시켜 달라고 요청한다. 법안 확정·시행과 구분한다.

### R19507

> RT @Jim_Jordan: While Democrats are focused on undoing the 2016 election, President Trump is doing what he said.Able-bodied adults withou...

판정: needs_context / uncertain · Context_Required

근거: 링크·짧은 반응 또는 지시 대상이 생략된 글이다. 연결 원문 없이는 경제정책 관련성과 부호를 확정할 수 없어 보류한다.



## part3 개별 검토 주요·애매 사례

아래는 담당 원문 개별 검토에서 선정한 주요·애매 사례다.

### R19671

> RT @HouseGOP: House Democrats continue to waste the American people’s time with their impeachment sham.... ❌ Passing #USMCAnow❌ Securing o...

판정: include_core / uncertain

근거: USMCAnow 법안 통과 지연을 탄핵 비판과 연결; hashtag 뒤 now 때문에 기존사전 누락 [본문: RT @HouseGOP: House Democrats continue to waste the Ame]

### R19952

> Nancy Pelosi will go down as the least productive Speaker of the House in history. She is dominated by AOC Plus 3 and the Radical Left. Mexico and Canada, after waiting for 6 months to be approved, are ready to flee - and who can blame them? Too bad!

판정: include_core / uncertain

근거: Mexico·Canada가 6개월 승인지연 끝에 이탈할 가능성을 제시; 협정 명칭이 없어도 USMCA 입법불확실성 문맥 [본문: Nancy Pelosi will go down as the least productive Speak]

### R20651

> RT @CNNPolitics: JUST IN: Trump administration suspends US commercial flights to 9 destinations in Cuba except for Havana https://t.co/KPPQ...

판정: include_core / uncertain

근거: 쿠바9개 목적지 미국 상업항공편 중단이라는 구체 제한 [본문: RT @CNNPolitics: JUST IN: Trump administration suspends]

### R21033

> Dealing with @LindseyGrahamSC and many members of Congress, including Democrats, about imposing powerful Sanctions on Turkey. Treasury is ready to go, additional legislation may be sought. There is great consensus on this. Turkey has asked that it not be done. Stay tuned!

판정: include_core / uncertain

근거: Treasury 준비된 터키 강력제재 및 추가입법 논의 [본문: Dealing with @LindseyGrahamSC and many members of Congr]

### R21124

> The joint statement released with President Bolsonaro in March makes absolutely clear that I support Brazil beginning the process for full OECD membership. The United States stands by that statement and stands by @jairbolsonaro. This article is FAKE NEWS! https://t.co/Hym9ZATHjt

판정: include_core / uncertain

근거: 브라질 OECD정회원 가입절차 지지 보도정정 [본문: The joint statement released with President Bolsonaro i]

### R21244

> As I have stated strongly before, and just to reiterate, if Turkey does anything that I, in my great and unmatched wisdom, consider to be off limits, I will totally destroy and obliterate the Economy of Turkey (I’ve done before!). They must, with Europe and others, watch over...

판정: include_core / uncertain

근거: 터키 경제를 파괴하겠다는 조건부위협 [본문: As I have stated strongly before, and just to reiterate]

### R21805

> The Trump Administration is revoking California’s Federal Waiver on emissions in order to produce far less expensive cars for the consumer, while at the same time making the cars substantially SAFER. This will lead to more production because of this pricing and safety......

판정: include_core / uncertain

근거: 캘리포니아 자동차배출 연방면제 철회라는 구체산업규제 조치 [본문: The Trump Administration is revoking California’s Feder]

### R21810

> I have just instructed the Secretary of the Treasury to substantially increase Sanctions on the country of Iran!

판정: include_core / uncertain

근거: 재무장관에게 이란 경제제재 대폭 강화 지시 [본문: I have just instructed the Secretary of the Treasury to]

### R22496

> ....My only question is, who is our bigger enemy, Jay Powel or Chairman Xi?

판정: include_core / negative

근거: Jay Powel과 Chairman Xi 중 누가 더 큰 적인지 묻는 연준 공격이다. Powell 오탈자·후속문장 때문에 기존검색이 놓친 명백한 통화정책 수사 후보다. [본문: ....My only question is, who is our bigger enemy, Jay Powel or Chairman Xi?]

### R22555

> My proposal to the politically correct Automobile Companies would lower the average price of a car to consumers by more than $3000, while at the same time making the cars substantially safer. Engines would run smoother. Very little impact on the environment! Foolish executives!

판정: include_core / mixed

근거: 자동차 규제 대안이 소비자가격을3000달러 낮춘다고 주장하며 경영진을 비난한다. 회사명이없어도 자동차 규제·기업압박 문맥이 명시된다. [본문: My proposal to the politically correct Automobile Companies would lower the average price ]

### R22961

> Lowering drug prices for many Americans - including our great seniors! At my direction, @HHSGov @SecAzar just released a Safe Importation Action Plan. Our Governors will be very happy too! @GovRonDeSantis @GovofCO https://t.co/VIxmZWgYM2

판정: include_core / positive

근거: HHS의 Safe Importation Action Plan 공개로 약가를 낮추려는 구체 수입정책 발표다. import라는 정책 의미가있어 기존trade회사명사전과 무관하게포함필요. [본문: Lowering drug prices for many Americans - including our great seniors! At my direction, @H]

### R22986

> ...to ripoff the USA, even bigger and better than ever before. The problem with them waiting, however, is that if &amp, when I win, the deal that they get will be much tougher than what we are negotiating now...or no deal at all. We have all the cards, our past leaders never got it!

판정: include_core / negative

근거: 현재 협상보다 향후 거래조건이 더 엄격해지거나 합의가없을 수 있다고 위협하는 후속문장이다. 교역국·협정명이 생략되어 스레드복원이 필요하다. [본문: ...to ripoff the USA, even bigger and better than ever before. The problem with them waiti]

### R20669

> To Tim: The Button on the IPhone was FAR better than the Swipe!

판정: include_extended / uncertain

근거: 아이폰 버튼·Swipe에 대한 제품 의견이다. 기업 언급이나 새 규제·무역 조치가 아니므로 core에서 광의 기업 논평으로 재분리한다.

### R21169

> But we are now, for the first time, giving companies a better alternative! https://t.co/jJFKywyIGw

판정: needs_context / uncertain

근거: 정책대안이나 잘린 협정 해시태그를 언급하지만 대상·내용을 본문만으로 특정할 수 없어 원문복원이 필요하다.

## raw_row 24399

> Great to welcome Chairman Shin from Lotte Group to the WH. They just invested $3.1 BILLION into Louisiana-biggest investment in U.S. EVER from a South Korean company, &amp, thousands more jobs for Americans. Great partners like ROK know the U.S. economy is running stronger than ever! https://t.co/WaJxDeTuxj

Lotte의 Louisiana 31억달러 투자. 한국회사 최대 대미투자라는 구체 기업투자 내용으로 회고성 찬사와 신규 투자확정을 구분하되 핵심 후보에 포함한다.

## raw_row 24569

> Great news today: My Administration just secured a historic donation of HIV prevention drugs from Gilead to help expand access to PrEP for the uninsured and those at risk. Will help us achieve our goal of ending the HIV epidemic in America! https://t.co/wux5QasWgW

Gilead의 HIV 예방약 기부 확보와 무보험자 PrEP 접근 확대를 발표한 기업·보건합의. 긍정은 접근성 확대를 가리키며 주가상승을 뜻하지 않는다.

## raw_row 24575

> Big announcement today: Drug companies have to come clean about their prices in TV ads. Historic transparency for American patients is here. If drug companies are ashamed of those prices—lower them!

제약기업 TV광고 가격공개 의무 발표와 가격인하 요구. 소비자 부담완화는 긍정, 기업수익에는 부정 가능성이 있어 mixed가 적절하다.

## raw_row 25141

> We have redeployed 750 agents at the Southern Border’s specific Ports of Entry in order to help with the large scale surge of illegal migrants trying to make their way into the United States. This will cause traffic &amp, commercial delays until such time as Mexico is able to use....

입국항 요원750명 재배치가 commercial delays를 초래한다고 직접 명시. 이민 관련 글이라도 무역운송을 막는 실제조치는 단순 정치글로 제외하면 안 된다.

## raw_row 25290

> It was announced today by the U.S. Treasury that additional large scale Sanctions would be added to those already existing Sanctions on North Korea. I have today ordered the withdrawal of those additional Sanctions!

추가 대북제재 철회를 오늘 명령했다는 원문. 기존 대북제재 전면해제라고 확대해석하지 않으며 완화방향 positive는 추가제재에 한정한다.

## raw_row 25675

> There is far more ENERGY on the Right than there is on the Left. That’s why we just won the Senate and why we will win big in 2020. The Fake News just doesn’t want to report the facts. Border Security is a big factor. The under construction Wall will stop Gangs, Drugs and Crime!

ENERGY는 우파의 정치적 열의를 뜻하므로 에너지산업으로 분류하지 않는다.

## raw_row 25778

> Coal is an important part of our electricity generation mix and @TVAnews should give serious consideration to all factors before voting to close viable power plants, like Paradise #3 in Kentucky!

TVA에 Paradise3 등 발전소 폐쇄 전 고려를 촉구. 에너지정책과 특정기업 운영압박이 겹치므로 핵심 기업압박 후보로 포함한다.

## raw_row 25888

> Howard Schultz doesn’t have the “guts” to run for President! Watched him on @60Minutes last night and I agree with him that he is not the “smartest person.” Besides, America already has that! I only hope that Starbucks is still paying me their rent in Trump Tower!

Howard Schultz의 출마 비판과 Starbucks 임대료 농담. 회사명이 등장해도 기업투자·규제발표가 아니므로 제외한다.

## raw_row 26056

> Volkswagen will be spending 800 million dollars in Chattanooga, Tennessee. They will be making Electric Cars. Congratulations to Chattanooga and Tennessee on a job well done. A big win!

Volkswagen의 Chattanooga 전기차생산 8억달러 투자를 명시. 기업명·투자규모·지역·사업이 모두 특정되는 강한 포함사례다.

## raw_row 26237

> Just signed an order to support the workers of Delphi Corporation and make sure that we protect the pensions of all American workers! Obama-Biden FAILED American workers and FAILED the workers of Delphi. I ALWAYS put American workers FIRST!

Delphi근로자 연금지원을 위한 명령 서명 발표. 일반 노동자 지지구호와 달리 기업 및 실제 행정명령이 특정된다.


## 2차 검토 근거와 재현

- `remaining_individual_review_ledger.csv`: 24,556행 원문·검토자·배치·판단·근거.
- `additional_core_candidates.csv`: 기존 범위의 추가 후보.
- `additional_extended_candidates.csv`: 범위 확장 여부를 결정할 글.
- `remaining_context_required.csv`: 연결 원문 복원이 필요한 미확정 글.
- `remaining_individual_review_summary.json`: 판단별 합계와 분담 범위.
- `remaining_review/*_decisions.jsonl`: 배치별 개별 판정 기록.

`python scripts/finalize_remaining_tweet_review.py`는 24,556행의 키·건수·범위·원본 체크섬을 검증한 후 이 보고서를 갱신한다. 의미 판독을 자동으로 재수행하는 스크립트가 아니다.

## 1차 감사 보존 기록

아래는 2차 검토 전 결과의 보존 기록이다. 아래의 ‘24,556행 미검토’라는 문구는 **1차 시점의 상태**이며 현재 상태는 위의 2차 검토표가 대체한다. 기존 분류 1,246건의 문제와 시각 오류·통계 해석에 관한 상세 근거는 계속 유효하다.

# 트럼프 트윗 분류·누락 감사 보고서

GAM 팀프로젝트 · 감사일 2026-11-02 · 원본 보존 검토


## Executive Summary · 핵심 판단

현재 분류는 **동명이인·관용구를 걸러 낸 연구 초안으로 유용하지만, 누락 없는 전수 분류나 일관된 시장 호재·악재 라벨로 확정하기에는 부족하다.** 원본 26,239행을 자동으로 전수 대조하고 기존 분류 1,246행과 추가 후보 437행의 본문을 개별 열람한 결과, 현행 범주와 대조해 추가 분류가 필요한 글을 **59건** 특정했다. ‘trade wars’ 복수형, ‘trade deals’ 복수형, KORUS, 회사명 사전 밖 기업 등이 주요 누락 경로이다. 이는 확정된 정책사건 수나 전체 누락률이 아니라 **본문상 포함 검토가 필요한 최소 확인 목록**이다.

기존 분류에서는 **152건**에 범주 수정, 부호 재설계, 스레드·링크 보완 또는 범위 일관성 검토를 제안했다. 이 숫자는 오분류 확정 건수나 오류율이 아니다. 동명이인·관용구 경보 48건의 기존 Noise 판정은 본문상 타당했다. 가장 큰 해석 문제는 **무역갈등 방향, 국내 산업 수혜, 연준 비판의 어조, 경제 성과 홍보를 같은 Positive/Negative 축에 섞었다는 점**이다.

시각 검증에서는 원본 **311건**, 기존 분류 **19건**의 `date_utc`가 Snowflake 생성 시각과 약 12시간 어긋났다. 실제 NYSE 폐장시각까지 반영하면 기존 분류 **2건**의 거래일 수정이 필요하다. 반면 현재 라벨·저장된 날짜를 그대로 이용한 25개 일별 집계열은 1,007일 모두 일치했다. **내부 집계가 맞는 것과 원문 분류·사건 시각이 맞는 것은 별개**다.

권고는 기존 원본을 보존하고, 분류 기준을 다축으로 재설계한 별도 버전을 만든 뒤 누락·시각·신규성을 함께 정리하는 것이다. 이 감사에서는 라벨이나 시장 데이터를 덮어쓰지 않았고, 수정 전후 시장효과를 새로 확정하지 않았다.

## 1. ‘전수조사’의 범위와 판단 단위

감사 모집단은 프로젝트에 저장된 트럼프 1기 아카이브 26,239행이다. 리트윗도 포함한다. ‘원글’이라는 표현은 데이터에 보존된 본문을 뜻하며, 트럼프 본인이 새로 쓴 글만을 의미하지 않는다. 본인 작성 글만을 분석할 경우 RT 포함 연구와 별도로 모집단을 다시 정의해야 한다.

**전수 완료 범위:** 모든 행의 원문·작성시각·식별자·기존 분류 포함 여부·확장 테마 경보·RT/단편 여부를 자동 검사했다. 분류된 1,246행은 본문 전체를 열람했고, 기존 분류 밖 437개 추가 후보도 본문을 열람해 확인 목록을 작성했다. 라벨은 검토 제안이며 복수 독립 평가자가 만든 정답지가 아니다.

**완료하지 않은 범위:** 무경보 23,698행과 거시·재정 범위만 검출된 858행, 합계 24,556행은 개별 의미 판독을 끝내지 않았다. 연결된 기사·인용글·이미지·영상·전체 RT 원문의 전수 복원도 실시하지 않았다. 따라서 ‘26,239개 원글을 모두 의미 판독했고 누락이 더 없다’는 결론을 내릴 수 없다. 이 제한은 특히 키워드가 전혀 없는 후속 스레드와 링크·영상만 있는 글에서 중요하다.

본문의 C번호는 `tweet_idx`(0부터 시작), R번호는 원본 CSV 데이터 행의 0기반 위치다. CSV 물리적 줄 번호는 본문 줄바꿈 때문에 다를 수 있다. 연결키는 날짜+정규화 본문의 SHA-256이며 손상된 ID에 의존하지 않는다. 검토에 시장 수익률이나 사후 VIX 급등 여부를 사용하지 않았다.

### 감사 범위와 확인 결과

| 점검 | 범위·결과 | 해석 |
| --- | --- | --- |
| 전체 원문 | 26,239행 | 자동 전수 점검; 모두 개별 의미 판독한 것은 아님 |
| 기존 분류 | 1,246행 / 원문 대조 불일치 0 | 357 Positive + 421 Negative + 468 Noise |
| 확장 테마 추가 후보 | 437행 | 그중 59행 추가 분류 필요; 나머지는 소음·보류·범위 후보 |
| 거시·재정만 검출 | 858행 | 정책 모집단 확대 여부 결정 후 개별 판독 필요 |
| 확장 규칙 무경보 | 23,698행 | 무경보가 정책 관련 글 부재를 보증하지 않음 |
| 시장 자료 | 1,007일 × 120열 | NYSE 거래일 누락·추가 0; 원본 열 보존 |
| 집계 연결 | 25열 × 1,007일 = 25,175셀, 불일치 0 | 현재 라벨·저장된 매핑을 재현한 결과 |
| 의미 검토 유지/추가 점검 | 유지 1094 / 추가 점검 152 | 정확도 산출용 독립 정답 판정이 아님 |

## 2. 누락은 존재하며, 검색 범위를 넓히는 것만으로 해결되지는 않는다

기존 `audit_trade_tweets.py`는 `trade war`, `trade deal`을 단어 경계로 검색한다. 이 설정은 `trade wars`, `trade deals`의 끝 경계와 맞지 않아 다른 키워드가 없으면 글을 놓친다. KORUS, WTO, 무역 관련 일반 `trade`, President Xi의 축약형, GM·Ford·Harley·TikTok·Amazon 등도 기존 1차 사전에 충분히 들어 있지 않다. 반면 최종 분류에는 GM·Google·Qualcomm·Harley 등 사전 밖 기업을 이미 포함한 사례가 있어, 최종 분류 범위와 후보 추출 범위가 어긋난다.

누락 후보 437건을 그대로 누락 확정치로 보고하지 않았다. 확대 검색에서는 World Trade Center, Witness Trade, drug trade, duties(직무), GM(교통기관 general manager), Ford(항공모함·인명·병원), Amazon(열대우림), phase one(건강검진·백신 임상)이 새 오탐으로 들어온다. 이 가운데 20건을 명확한 제외 예시로 원장에 기록했다.

누락의 의미도 구분해야 한다. 원본에 존재하지만 분류 파일에 없는 **후보 선택 누락**, 아카이브 자체에 빠진 **수집 누락**, 정책 문맥은 있지만 신호·방향을 정하기 어려운 **판정 보류**는 서로 다르다. 아래 목록은 첫 번째 문제를 확인한 것이며, 연결 매체와 신규성 검토까지 마친 사건 정답지는 아니다.

### R18710. 복수형 trade wars 때문에 빠진 대표적 보호무역 수사

**추적:** R18710 · 저장 UTC 2018-03-02 10:50:34+00:00 · 원문+시각 연결키 `a9198e2d52a924238e5870e7d88ec990dd7ee960a48548ac89d50d08d26bf650`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/969525362580484098)

> When a country (USA) is losing many billions of dollars on trade with virtually every country it does business with, trade wars are good, and easy to win. Example, when we are down $100 billion with a certain country and they get cute, don’t trade anymore-we win big. It’s easy!

**판정:** Trade_Protectionism / Escalation. 무역전쟁 정당화, 불공정무역 대응조치, WTO 개발도상국 특혜 시정 지시가 명시되어 기존 범위에서 추가 분류가 필요하다. 원문 보도·행정조치가 있는 링크는 별도 보존한다.

### R18565. 한미 FTA(KORUS) 합의 발표 누락

**추적:** R18565 · 저장 UTC 2018-03-28 16:14:34+00:00 · 원문+시각 연결키 `ed308f009f981d943cdd68e9e883f193b519dc36afc1281ccddf1a87a095592f`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/979028987858112512)

> .@USTradeRep just announced an agreement in principle with South Korea on KORUS! A great deal for American and Korean workers. Let’s now focus on our important security relationship.

**판정:** Trade_Deal_Progress / Deescalation/Positive. 한미 FTA 합의·서명, 미멕시코 협정, 미일 협상 진전·합의, 미EU 무역관계 개선, 미중 1단계 서명이라는 직접 정책 문맥이 있다. 짧은 RT는 신규성·원문 보완을 병행한다.

### R16605. 한미 FTA 서명식 공지 누락

**추적:** R16605 · 저장 UTC 2018-09-24 20:44:24+00:00 · 원문+시각 연결키 `5349402d3654ca9e06c04ac5e15a07c8acc4e5df100f781cb510153fa92b8326`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1044326708151820289)

> US-Korea Free Trade Agreement Signing Ceremony! https://t.co/yLFkAZgagG

**판정:** Trade_Deal_Progress / Deescalation/Positive. 한미 FTA 합의·서명, 미멕시코 협정, 미일 협상 진전·합의, 미EU 무역관계 개선, 미중 1단계 서명이라는 직접 정책 문맥이 있다. 짧은 RT는 신규성·원문 보완을 병행한다.

### R16920. 캐나다 협상 미타결이라는 악재 누락

**추적:** R16920 · 저장 UTC 2018-09-01 22:51:29+00:00 · 원문+시각 연결키 `d6f3a81d985a556e319672e7347b087f9a50c7718d156eff3d512a0561a2813d`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1036023767489814528)

> No Deal! Trade Talks with Canada Conclude for the Week with No Agreement | Breitbart https://t.co/87vi7OqopY via @BreitbartNews

**판정:** Trade_Deal_Setback / Escalation/Negative. 캐나다 협상 결렬·합의 미도달을 직접 알리는 제목이다. 링크 없이도 정책 불확실성 정보가 있다.

### R23057. WTO 시정조치 지시 누락

**추적:** R23057 · 저장 UTC 2019-07-26 18:29:22+00:00 · 원문+시각 연결키 `59be78c265c849112ce5cfdfb965641ca163cd944ffe5faeeed38ee0d9bccbaa`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1154821023197474817)

> The WTO is BROKEN when the world’s RICHEST countries claim to be developing countries to avoid WTO rules and get special treatment. NO more!!! Today I directed the U.S. Trade Representative to take action so that countries stop CHEATING the system at the expense of the USA!

**판정:** Trade_Protectionism / Escalation. 무역전쟁 정당화, 불공정무역 대응조치, WTO 개발도상국 특혜 시정 지시가 명시되어 기존 범위에서 추가 분류가 필요하다. 원문 보도·행정조치가 있는 링크는 별도 보존한다.

### R17703. Harley 이전 시 과세 위협 누락

**추적:** R17703 · 저장 UTC 2018-06-26 12:17:49+00:00 · 원문+시각 연결키 `16fb1e86d1856c3dbbfa2e1e8916e60ec102fc1109d63db136dac378e92e1155`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1011584315040419840)

> A Harley-Davidson should never be built in another country-never! Their employees and customers are already very angry at them. If they move, watch, it will be the beginning of the end - they surrendered, they quit! The Aura will be gone and they will be taxed like never before!

**판정:** Company_Pressure / Pressure/Asset_Dependent. 할리·GM·자동차업체·아마존에 대한 이전 억제·공장 재개·세금·배송료·생산 요구이다. 기존 NEG_Company_Tech_Pressure의 GM·Google 등 확장 범위와 동일 원칙을 적용해야 한다. 산업 보호 효과와 개별 기업 비용 증가는 별개다.

### R10866. GM·Ford에 대한 인공호흡기 생산 요구 누락

**추적:** R10866 · 저장 UTC 2020-03-27 15:23:53+00:00 · 원문+시각 연결키 `4deaee54b8c3420b4a899d15f8ec220a8bb92462720cf40d433b35bfe7091b45`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1243559373395410957)

> General Motors MUST immediately open their stupidly abandoned Lordstown plant in Ohio, or some other plant, and START MAKING VENTILATORS, NOW!!!!!! FORD, GET GOING ON VENTILATORS, FAST!!!!!! @GeneralMotors @Ford

**판정:** Company_Pressure / Pressure/Asset_Dependent. 할리·GM·자동차업체·아마존에 대한 이전 억제·공장 재개·세금·배송료·생산 요구이다. 기존 NEG_Company_Tech_Pressure의 GM·Google 등 확장 범위와 동일 원칙을 적용해야 한다. 산업 보호 효과와 개별 기업 비용 증가는 별개다.

### R8886. Amazon 배송료 인상 요구 누락

**추적:** R8886 · 저장 UTC 2020-08-18 22:49:11+00:00 · 원문+시각 연결키 `fc4c3547da1e65b2d8643008c6e7bd4a5318968ea05bdf43ee660272e878f83a`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1295855291523723264)

> .@Amazon, and others in that business, should be charged (by the U.S. Postal System) much more per package, and the Post Office would be immediately brought back to “good health”, now vibrant, with ALL jobs saved. No pass on to customers. Get it done!

**판정:** Company_Pressure / Pressure/Asset_Dependent. 할리·GM·자동차업체·아마존에 대한 이전 억제·공장 재개·세금·배송료·생산 요구이다. 기존 NEG_Company_Tech_Pressure의 GM·Google 등 확장 범위와 동일 원칙을 적용해야 한다. 산업 보호 효과와 개별 기업 비용 증가는 별개다.

### R3829. TikTok 행정명령 RT 누락

**추적:** R3829 · 저장 UTC 2020-08-07 12:41:26+00:00 · 원문+시각 연결키 `0c152fa8dba560348e5d5555ca80431732d564cdabc75050fe2976a4327eec1b`. 원글 링크는 정확한 ID 복원이 확인되지 않아 생략했다.

> RT @QuickTake: BREAKING: Trump signs executive order forcing the divestment of TikTok by it’s owner, ByteDance. Any company still doing bu…

**판정:** Technology_Regulation / Pressure/Uncertain. TikTok 금지·매각명령·Google 조사 등 기술기업 규제 문맥이다. 기존 Google·Huawei 제재 범위와 같은 기준으로 후보를 포함하고 실제 조치·검토·제3자 주장·재전달을 구분한다.

### R4806. 코로나 여행제한의 무역 적용 배제 정정 누락

**추적:** R4806 · 저장 UTC 2020-03-12 02:13:32+00:00 · 원문+시각 연결키 `7c5228a00036053fde042d9833bc4ec4e1c1b372799b50c211f5171e1c8d5544`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1237924658185469954)

> Hoping to get the payroll tax cut approved by both Republicans and Democrats, and please remember, very important for all countries &amp; businesses to know that trade will in no way be affected by the 30-day restriction on travel from Europe. The restriction stops people not goods.

**판정:** Trade_Restriction_Clarification / Deescalation/Neutral. 유럽 여행제한·캐나다 국경폐쇄가 무역·화물에는 적용되지 않는다고 명시한다. 코로나 단어로 제외하면 실제 무역제한 범위 정정 정보를 잃는다.

### R7436. 캐나다 국경폐쇄와 상품무역을 구분한 글 누락

**추적:** R7436 · 저장 UTC 2020-03-18 13:37:46+00:00 · 원문+시각 연결키 `0a2bfca44a1b3e77d530b6e5a08e17ca43e698d21597f267beafe1a442d0c90a`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1240271178692005889)

> We will be, by mutual consent, temporarily closing our Northern Border with Canada to non-essential traffic. Trade will not be affected. Details to follow!

**판정:** Trade_Restriction_Clarification / Deescalation/Neutral. 유럽 여행제한·캐나다 국경폐쇄가 무역·화물에는 적용되지 않는다고 명시한다. 코로나 단어로 제외하면 실제 무역제한 범위 정정 정보를 잃는다.

### R13537. Broadcom 미국 투자·생산 관련 발표 누락

**추적:** R13537 · 저장 UTC 2017-11-02 20:33:18+00:00 · 원문+시각 연결키 `1171426750d63a7b18da80b192ba5d989bfefbee590bc5169b4838c6c152b77c`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/926185468911382529)

> Broadcom's move to America=$20 BILLION of annual rev into U.S.A., $3+ BILLION/yr. in research/engineering &amp, $6 BILLION/yr. in manufacturing. https://t.co/NsJ4PtVTtl

**판정:** Industry_Investment_or_Production / Asset_Dependent/Positive. 미국 내 투자·공장·일자리 또는 DPA 관련 자동차업체 생산조치이다. 현재 POS_US_Industry_Econ_Boom 및 Company 범위와 대조하면 회사명 사전 제한으로 누락된 사례이다. 단순 만남은 낮은 강도로 별도 관리한다.

### R23404. Facebook Libra 규제 문맥 누락

**추적:** R23404 · 저장 UTC 2019-07-12 00:15:23+00:00 · 원문+시각 연결키 `068c5b75716ace7adc52c3e1911562de92dd8a90566e9016c632fd53a1ffc635`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1149472284702208000)

> ....Similarly, Facebook Libra’s “virtual currency” will have little standing or dependability. If Facebook and other companies want to become a bank, they must seek a new Banking Charter and become subject to all Banking Regulations, just like other Banks, both National...

**판정:** Crypto_FX_Regulation / Mixed/Uncertain. Bitcoin·Libra·은행규제·달러를 다룬 연속 글이다. 기존 FX 범위에 포함할지 명시적으로 결정하고 암호자산 규제와 달러 선호를 구분한다.

## 3. 동명이인·관용구는 대체로 잘 제거되어 있다

48개 명시적 동명이인·관용구 경보는 모두 현재 Noise이며, 본문 검토상 유지가 적절하다. Sidney Powell·Colin Powell·Dina Powell을 Jerome Powell로 오인하거나, Shawn Steel을 철강산업으로 연결한 흔적은 이 경보군에서 찾지 못했다. `fed up`, `being fed`, `apple cart`, `man of steel`, 국경의 steel slats/barrier도 실제 정책 테마와 구분되어 있다. 경보 규칙이 모든 동음이의어를 포괄한다는 뜻은 아니다.

이 결과는 1차 키워드 사전의 오탐이 최종 문맥 분류에서 상당 부분 교정됐다는 근거다. 다만 기존 `Trade_Tweet_Dummy`, `Fed_Tweet_Dummy`는 원래 키워드 기준을 그대로 보존하므로, 최종 Noise가 기존 더미 분석에서 자동으로 제외된 것은 아니다. 두 종류의 분석을 발표에서 혼용하면 안 된다.

### C29. Shawn Steel은 사람 이름

**추적:** C29, R2715 · 저장 UTC 2017-07-03 20:44:27+00:00 · 원문+시각 연결키 `7639f9c2f25aafdb5788b65d84f7cbe7e0512f70af797d566a2fc52f5877ffee`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/881976958556549120)

> Thank you to Shawn Steel for the nice words on @FoxNews.

**판정:** 현재 Noise 유지. 본문의 고유명사·관용적 의미를 우선하고 키워드 일치 자체를 경제정책 신호로 취급하지 않는다.

### C494. Sidney Powell은 Flynn의 변호사

**추적:** C494, R23894 · 저장 UTC 2019-06-13 10:21:50+00:00 · 원문+시각 연결키 `266922448c01e4653f0fb8e55c662f899a59c30f4f31e4f8c53541fead372f69`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1139115655532298240)

> General Michael Flynn, the 33 year war hero who has served with distinction, has not retained a good lawyer, he has retained a GREAT LAWYER, Sidney Powell. Best Wishes and Good Luck to them both!

**판정:** 현재 Noise 유지. 본문의 고유명사·관용적 의미를 우선하고 키워드 일치 자체를 경제정책 신호로 취급하지 않는다.

### C1053. Colin Powell은 연준 의장이 아님

**추적:** C1053, R12178 · 저장 UTC 2020-06-07 14:19:03+00:00 · 원문+시각 연결키 `0a06012f54961c0b4794b16415852954f150ec1703e7fb6bb3156f947da876d0`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1269634983687315457)

> Colin Powell, a real stiff who was very responsible for getting us into the disastrous Middle East Wars, just announced he will be voting for another stiff, Sleepy Joe Biden. Didn’t Powell say that Iraq had “weapons of mass destruction?” They didn’t, but off we went to WAR!

**판정:** 현재 Noise 유지. 본문의 고유명사·관용적 의미를 우선하고 키워드 일치 자체를 경제정책 신호로 취급하지 않는다.

### C146. apple cart는 관용구

**추적:** C146, R18088 · 저장 UTC 2018-05-27 20:32:33+00:00 · 원문+시각 연결키 `ccf44e25be028405d78446f3e40ed6eb14899c86e15d78d230d4c54c8d1939f4`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1000837182297464832)

> Why didn’t President Obama do something about the so-called Russian Meddling when he was told about it by the FBI before the Election? Because he thought Crooked Hillary was going to win, and he didn’t want to upset the apple cart! He was in charge, not me, and did nothing.

**판정:** 현재 Noise 유지. 본문의 고유명사·관용적 의미를 우선하고 키워드 일치 자체를 경제정책 신호로 취급하지 않는다.

### C208. man of steel은 골퍼 묘사

**추적:** C208, R17176 · 저장 UTC 2018-08-13 17:11:21+00:00 · 원문+시각 연결키 `a6e14954fb04d103633dd56b228d4fa328e1c3ba7872ba4ba6cf7523c5d70736`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1029052803380076544)

> Brooks Koepka just won his third Golf Major, and he did it not only with his powerful game, but with his powerful mind. He has been a man of steel on the Tour and will have many Victories, including Majors, ahead of him. Congrats to Brooks and his great team on a job well done!

**판정:** 현재 Noise 유지. 본문의 고유명사·관용적 의미를 우선하고 키워드 일치 자체를 경제정책 신호로 취급하지 않는다.

### C300. steel slats는 국경 구조물

**추적:** C300, R15679 · 저장 UTC 2018-12-19 01:13:30+00:00 · 원문+시각 연결키 `b2bcf55707b4fe617ca499ac4ac1eb01e6140bc279705eb23f65695fdcb2e708`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1075197395892404231)

> The Democrats, are saying loud and clear that they do not want to build a Concrete Wall - but we are not building a Concrete Wall, we are building artistically designed steel slats, so that you can easily see through it....

**판정:** 현재 Noise 유지. 본문의 고유명사·관용적 의미를 우선하고 키워드 일치 자체를 경제정책 신호로 취급하지 않는다.

## 4. 긍정·부정의 가장 큰 문제는 ‘무엇에 대한 방향인가’가 섞였다는 점이다

기존 라벨 357 Positive·421 Negative·468 Noise 가운데 추가 점검 대상으로 특정한 글은 각각 **76·50·26건**이다. 검토 이슈는 범주 불일치, 정의 문제, 혼합 신호, 본문 부족, 낮은 신규성을 포함하며 전부 오류는 아니다. 유지로 남긴 글도 완전한 정확성을 보증하지 않는다.

현재 정의는 ‘정책 불확실성 완화/고조’와 ‘미국 산업 성장’, ‘발화의 비난 어조’를 결합한다. 그 결과 관세가 철강업을 살렸다는 유사한 문장이 어떤 날은 Positive, 어떤 날은 Negative가 된다. 연준 금리 인하 요구는 Fed에 대한 비판일 수 있으나 주식·채권·달러에 동일한 부호를 갖는 악재라고 미리 정할 수 없다. 사후 주가 등락으로 라벨을 정하는 방법 역시 결과변수에 의한 선택 편향을 만든다.

권고하는 방향은 Positive/Negative를 기계적으로 뒤집는 것이 아니다. **테마, 정책 갈등 방향, 통화정책 방향, 개별 자산 노출, 발표 강도, 신규성, 불확실성**을 분리해야 한다. ‘Noise’도 ‘어떤 시장에도 영향 없음’이 아니라 ‘이번 연구의 사전 정의 밖이거나 관련 정보 부족’으로 정의하는 편이 정확하다.

### 세부유형별 기존 건수와 추가 점검 건수

| 기존 세부유형 | 전체 | 추가 점검 | 주의 |
| --- | --- | --- | --- |
| NEG_Company_Tech_Pressure | 27 | 3 | 정의·범주·문맥 이슈를 포함; 오류율 아님 |
| NEG_Fed_Rate_Attack | 105 | 3 | 정의·범주·문맥 이슈를 포함; 오류율 아님 |
| NEG_Protectionist_Attack | 199 | 23 | 정의·범주·문맥 이슈를 포함; 오류율 아님 |
| NEG_Tariff_Threat_Action | 90 | 21 | 정의·범주·문맥 이슈를 포함; 오류율 아님 |
| NOISE_Non_Market | 468 | 26 | 정의·범주·문맥 이슈를 포함; 오류율 아님 |
| POS_Deal_Progress | 227 | 37 | 정의·범주·문맥 이슈를 포함; 오류율 아님 |
| POS_Purchase_Agri_Support | 58 | 8 | 정의·범주·문맥 이슈를 포함; 오류율 아님 |
| POS_US_Industry_Econ_Boom | 72 | 31 | 정의·범주·문맥 이슈를 포함; 오류율 아님 |

### C499. Michael Steel 인용과 거시 낙관론: 회사·산업 키워드가 아님

**추적:** C499, R23756 · 저장 UTC 2019-06-20 14:14:13+00:00 · 원문+시각 연결키 `655c724e18cb97b73b5f2457ba21d45ddf94f8cde102670b0bce6908e5d688f8`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1141710851617034240)

> “The President has a really good story to tell. We have unemployment lower than we’ve seen in decades. We have people who stopped looking for work coming back into the labor force. We are in a record growth period.” Michael Steel @MSNBC (do you believe?)

**기존:** Positive / `POS_US_Industry_Econ_Boom`.

**검토:** 인용자의 성이 Steel이며 철강산업 발언이 아니다. 본문은 일반적인 고용·성장 평가이므로 광의의 Macro_Commentary로 보존할 수는 있다. 그러나 이 글을 포함하려면 회사명·산업 키워드가 없는 동일한 경기 낙관론도 같은 모집단에서 추출해야 한다. 따라서 동명이인만으로 Noise 확정하지 않고 범위 선택 편향을 지적한다.

### C519. 농민 지지율은 농산물 구매·농가 지원이 아님

**추적:** C519, R23622 · 저장 UTC 2019-06-30 00:07:39+00:00 · 원문+시각 연결키 `a1b80387d2e6909d42d339dbd23e8136ab5e82e64ff1a37743195bf2b3e18594`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1145121683193421826)

> The highly respected Farm Journal has just announced my Approval Rating with our great Farmers at 74%, and that despite all of the Fake &amp, Corrupt News that they are forced to endure. Farmers have been unfairly treated for many years - and that is turning around FAST!

**기존:** Positive / `POS_Purchase_Agri_Support`.

**검토:** 지지율·선거 전망·정권 성과 홍보가 중심이며 신규 구매·농가지원·산업투자 조치가 없다. 특히 C519는 농민 지지율을 실제 농가 구매지원으로 분류했다.

### C355. 연준 인선을 산업 호재로 처리한 비대칭

**추적:** C355, R25291 · 저장 UTC 2019-03-22 16:47:33+00:00 · 원문+시각 연결키 `042233c4cf74dc396d92c526d7177229e5368c0b7b5b6b7488bf470e7f98c8f8`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1109134531771150336)

> It is my pleasure to announce that @StephenMoore, a very respected Economist, will be nominated to serve on the Fed Board. I have known Steve for a long time – and have no doubt he will be an outstanding choice!

**기존:** Positive / `POS_US_Industry_Econ_Boom`.

**검토:** 연준 인선·지명·철회는 실제 통화정책 관련 정보이다. Moore 지명은 산업호재, Powell·Waller·Shelton 지명 및 Cain·Moore 철회는 Noise로 처리한 기준이 비대칭이다. 인선 사실과 완화/긴축 방향을 별도 기록해야 한다.

### C497. ECB 금리 인하 전망을 Fed 공격으로 분류

**추적:** C497, R23715 · 저장 UTC 2019-06-18 14:09:23+00:00 · 원문+시각 연결키 `bab7c6f685a7ea2062b5959707a400300e1d55696c58154676ff843ced33ac08`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1140984860628213760)

> “ECB officials see Rate Cut as primary tool for any new stimulus.” @business

**기존:** Negative / `NEG_Fed_Rate_Attack`.

**검토:** ECB의 금리 인하 전망을 인용한 글이며 미국 연준이나 Powell을 공격하는 내용이 없다. 경제·통화 신호는 맞지만 NEG_Fed_Rate_Attack은 부적절하다.

### C1234. 1832년 Andrew Jackson의 중앙은행 대립

**추적:** C1234, R2424 · 저장 UTC 2020-12-20 16:53:00+00:00 · 원문+시각 연결키 `8389301b09b96a098fadeb6aa9b1cb75a1c799514dd51c8d3f4876f2cbda9422`. 원글 링크는 정확한 ID 복원이 확인되지 않아 생략했다.

> RT @KanekoaTheGreat: Can you imagine a president taking on the Federal Reserve System today? That's what Andrew Jackson did in 1832 and it…

**기존:** Negative / `NEG_Fed_Rate_Attack`.

**검토:** Andrew Jackson의 1832년 역사적 중앙은행 대립을 언급한다. 현 연준 정책에 대한 신규 요구가 본문에 없으므로 현대 Fed 공격 사건과 구분한다. 잘린 RT 후반의 원문 복원은 별도 필요하다.

### C330. 관세의 철강산업 수혜를 Positive로 판정한 사례

**추적:** C330, R25890 · 저장 UTC 2019-01-28 13:16:32+00:00 · 원문+시각 연결키 `6cf5becbbe0e2b35e73a6d11ee9dfc8edf30411852cd4c126e46d93a936213c8`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1089874871247687683)

> Tariffs on the “dumping” of Steel in the United States have totally revived our Steel Industry. New and expanded plants are happening all over the U.S. We have not only saved this important industry, but created many jobs. Also, billions paid to our treasury. A BIG WIN FOR U.S.

**기존:** Positive / `POS_US_Industry_Econ_Boom`.

**검토:** 관세 유지·효과 찬사와 국내 산업 수혜를 호재로 처리했지만 C111·C199·C390·C439·C786 등 유사 내용은 보호무역 악재이다. 정책 갈등 방향과 철강 등 개별 자산 수혜를 두 축으로 분리해야 한다.

### C199. 관세의 철강산업 수혜를 Negative로 판정한 유사 사례

**추적:** C199, R17252 · 저장 UTC 2018-08-04 19:53:22+00:00 · 원문+시각 연결키 `03e742e4fc5a3a22f7c6c0b2f5d11ec81eb844f9ab05ffeadb1074268b3256e5`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1025832084521119745)

> ....Tariffs have had a tremendous positive impact on our Steel Industry. Plants are opening all over the U.S., Steelworkers are working again, and big dollars are flowing into our Treasury. Other countries use Tariffs against, but when we use them, foolish people scream!

**기존:** Negative / `NEG_Protectionist_Attack`.

**검토:** 관세 효과와 경제 성과를 칭찬하는 유사 문장들이 Positive에도 분포한다. 어느 쪽으로 일괄 뒤집기보다 보호무역 방향·국내 산업 영향·신규성 분리 후 재코딩한다.

### C145. ZTE 제재 조건과 영업재개 완화가 함께 있는 글

**추적:** C145, R18106 · 저장 UTC 2018-05-25 23:07:19+00:00 · 원문+시각 연결키 `f938d4c89df77a442d6af4ad4f229682f62e9a6adbade72ad43e98b1fe460cff`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1000151354701213696)

> Senator Schumer and Obama Administration let phone company ZTE flourish with no security checks. I closed it down then let it reopen with high level security guarantees, change of management and board, must purchase U.S. parts and pay a $1.3 Billion fine. Dems do nothing....

**기존:** Negative / `NEG_Company_Tech_Pressure`.

**검토:** ZTE를 폐쇄한 뒤 조건부 재개를 허용했다는 글이다. 벌금·보안조건은 규제지만 영업재개는 제재 완화이다. C130의 ZTE 구제 Positive와 함께 읽고 재개 대비 조건 강화라는 기준점을 명시해야 한다.

### C55. 중국과의 관계 덕담을 무역합의 진전으로 분류

**추적:** C55, R13476 · 저장 UTC 2017-11-09 13:58:32+00:00 · 원문+시각 연결키 `dc3f4dbd04a378283cb66a9edc5a00c7a6f502d5308d09630b2a3cebbed94113`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/928622838487007260)

> In the coming months and years ahead I look forward to building an even STRONGER relationship between the United States and China. 🇺🇸🇨🇳 https://t.co/mK3SB7t3EV

**기존:** Positive / `POS_Deal_Progress`.

**검토:** C55는 양국 관계 덕담, C598은 홍콩 시위의 평화적 해결과 개인 회동 제안이다. 본문에 무역합의 진전이 없으므로 POS_Deal_Progress 근거가 부족하다. 무역과 연결된 인접 문맥은 별도 표시한다.

### C598. 홍콩 시위 해결 제안을 무역합의 진전으로 분류

**추적:** C598, R22717 · 저장 UTC 2019-08-14 22:59:13+00:00 · 원문+시각 연결키 `e277af400fe395b1ade4ca0e5213deb1a9e782fbd4f57ff87d0b21e7498c1add`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1161774305895694336)

> I know President Xi of China very well. He is a great leader who very much has the respect of his people. He is also a good man in a “tough business.” I have ZERO doubt that if President Xi wants to quickly and humanely solve the Hong Kong problem, he can do it. Personal meeting?

**기존:** Positive / `POS_Deal_Progress`.

**검토:** C55는 양국 관계 덕담, C598은 홍콩 시위의 평화적 해결과 개인 회동 제안이다. 본문에 무역합의 진전이 없으므로 POS_Deal_Progress 근거가 부족하다. 무역과 연결된 인접 문맥은 별도 표시한다.

### C770. Powell과의 회동을 무역합의 진전으로 분류

**추적:** C770, R19996 · 저장 UTC 2019-11-18 03:49:55+00:00 · 원문+시각 연결키 `e122616c3f7d396dfc9d7484a34be59aa15554f5749b5cb27278467bee8707e5`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1196455500940038144)

> Just finished a very good &amp, cordial meeting at the White House with Jay Powell of the Federal Reserve. Everything was discused including interest rates, negative interest, low inflation, easing, Dollar strength &amp, its effect on manufacturing, trade with China, E.U. &amp, others, etc.

**기존:** Positive / `POS_Deal_Progress`.

**검토:** Powell과의 우호적 회동이며 금리·환율·무역을 논의한 사실을 적었다. 무역협상 진전이나 정책금리 인하 합의로 볼 수 없다. 같은 날 C773은 Fed 공격이어서 정책 Pure Positive 판정의 의미도 점검해야 한다.

### C273. #USMCA와 링크만 있는 글

**추적:** C273, R15844 · 저장 UTC 2018-11-30 13:08:27+00:00 · 원문+시각 연결키 `1fdbb0d5d49f846e9db31334014e172d90d7e942c3ece304ca5c5ede5d71b5b9`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1068491952696557575)

> #USMCA🇺🇸🇲🇽🇨🇦 https://t.co/7CYsYBYbd1

**기존:** Positive / `POS_Deal_Progress`.

**검토:** #USMCA 및 링크만으로는 해당 글에 새로 공개된 합의·조건·시각을 특정할 수 없다. 외부 매체 복원 전 강한 긍정 정책사건으로 확정하지 않는다.

### C1006. 코로나 비난을 하드 관세 위협으로 분류

**추적:** C1006, R8710 · 저장 UTC 2020-05-13 14:33:15+00:00 · 원문+시각 연결키 `af2b0cd45b5dd919e7adef23b83a6bbd7034c02f7b3ad1e84407e82f9b5607ad`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1260578860992737285)

> As I have said for a long time, dealing with China is a very expensive thing to do. We just made a great Trade Deal, the ink was barely dry, and the World was hit by the Plague from China. 100 Trade Deals wouldn’t make up the difference - and all those innocent lives lost!

**기존:** Negative / `NEG_Tariff_Threat_Action`.

**검토:** 코로나 피해는 무역합의 100개로도 보상할 수 없다는 비난이다. 본문에 신규 관세·세율·시한·조건부 부과 위협이 없어 하드 관세 충격으로 보기 어렵다.

### C530. 농산물 구매 실망과 직접 관세 선포의 차이

**추적:** C530, R23415 · 저장 UTC 2019-07-11 14:04:16+00:00 · 원문+시각 연결키 `af58cbb54f8c552632745271017ba2e1bba9ba2ce596a373b62b87f598d59a80`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1149318492711264257)

> Mexico is doing great at the Border, but China is letting us down in that they have not been buying the agricultural products from our great Farmers that they said they would. Hopefully they will start soon!

**기존:** Negative / `NEG_Tariff_Threat_Action`.

**검토:** 약속한 농산물 구매 부진을 비판한 글이다. 악재 방향은 가능하지만 직접 관세 선포·세율 인상은 없어 NEG_Tariff_Threat_Action보다 협상·구매 이행 차질이 적절하다.

### C568. 낙관적인 후속 문장이 하드 관세 악재가 된 사례

**추적:** C568, R22929 · 저장 UTC 2019-08-01 17:26:11+00:00 · 원문+시각 연결키 `ed3f450d4b0cc019aaf8b62630a6943e50dd9c3e7f27f44880db6e35b42f7c55`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1156979450560548864)

> ...We look forward to continuing our positive dialogue with China on a comprehensive Trade Deal, and feel that the future between our two countries will be a very bright one!

**기존:** Negative / `NEG_Tariff_Threat_Action`.

**검토:** 같은 스레드의 하드 충격을 모든 조각에 전파하면 C568의 낙관 문장과 C458의 관세 철회 문장도 단독 악재가 된다. 사건 단위로 묶되 최초 정보 공개시각을 유지하고 미래 조각으로 과거 라벨을 확정하지 않는다.

### C458. 관세가 제거될 조건을 적은 후속 문장

**추적:** C458, R23839 · 저장 UTC 2019-05-30 23:30:20+00:00 · 원문+시각 연결키 `d31a511e975b613c28255fb1288d3aa0c876dd2eb215738350c72fd8b7cddee0`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1134240657621438464)

> ....at which time the Tariffs will be removed. Details from the White House to follow.

**기존:** Negative / `NEG_Tariff_Threat_Action`.

**검토:** 같은 스레드의 하드 충격을 모든 조각에 전파하면 C568의 낙관 문장과 C458의 관세 철회 문장도 단독 악재가 된다. 사건 단위로 묶되 최초 정보 공개시각을 유지하고 미래 조각으로 과거 라벨을 확정하지 않는다.

### C824. Fake News 표현이 있어도 실제 관세 보도 부인일 수 있음

**추적:** C824, R19275 · 저장 UTC 2019-12-13 14:06:40+00:00 · 원문+시각 연결키 `48ac21ce7c867e4cd8376aed8fa7050276f86e3d0fc547ed2af5ba76740ef034`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1205489214546235393)

> The Wall Street Journal story on the China Deal is completely wrong, especially their statement on Tariffs. Fake News. They should find a better leaker!

**기존:** Noise / `NOISE_Non_Market`.

**검토:** 미중 합의와 관세에 관한 WSJ 보도를 직접 부인한다. Fake News라는 문구만으로 정치 소음으로 처리할 수 없다. 어떤 조건을 부인했는지는 당시 보도와 이미 알려진 정보에 의존하므로 단일 부호를 확정하지 않는다.

### C794. USMCA 붕괴 가능성을 Noise로 제외한 애매한 사례

**추적:** C794, R19608 · 저장 UTC 2019-12-07 18:54:36+00:00 · 원문+시각 연결키 `915cdb5f69261c4c11e458cc11f0cefb0893a03f5c00b5afe1d12bbef328343b`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1203387348274360322)

> Hard to believe, but if Nancy Pelosi had put our great Trade Deal with Mexico and Canada, USMCA, up for a vote long ago, our economy would be even better. If she doesn’t move quickly, it will collapse!

**기존:** Noise / `NOISE_Non_Market`.

**검토:** 통과 지연을 직접 지적하며 C794는 지연 시 합의 붕괴 가능성을 언급한다. 정치적 비판을 포함해도 정책 불확실성 정보가 있으므로 무조건 Noise 배제는 비대칭이다.

### C1077. 방역·사망률 찬사를 산업 호재로 처리

**추적:** C1077, R8512 · 저장 UTC 2020-07-06 18:36:50+00:00 · 원문+시각 연결키 `660ac26b484fe1c82bd03f048bd60ad3b1077937f883b314a401b169a9ddb9a2`. 원글 링크는 정확한 ID 복원이 확인되지 않아 생략했다.

> BREAKING NEWS: The Mortality Rate for the China Virus in the U.S. is just about the LOWEST IN THE WORLD! Also, Deaths in the U.S. are way down, a tenfold decrease since the Pandemic height (and, our Economy is coming back strong!).

**기존:** Positive / `POS_US_Industry_Econ_Boom`.

**검토:** 방역 수치·백신 성과·경기회복 찬사이며 신규 무역·산업 정책과 다르다. 유사한 백신 관련 C1128·C1225는 Noise이다. 보건 뉴스로 별도 관리할 수 있지만 시장 무관 여부와 Positive를 단정하지 않는다.

### C1236. 백신 보급 성과를 산업 호재로 처리하고 조기폐장도 놓침

**추적:** C1236, R2347 · 저장 UTC 2020-12-24 20:30:57+00:00 · 원문+시각 연결키 `c70ae2e31bc37c596f79806d1114aa71cd9ee0b8c3097406a833e6b4bcd9a7e2`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1342206148649299969)

> More than one million Americans have already received the China Virus Vaccine, a record pace!

**기존:** Positive / `POS_US_Industry_Econ_Boom`.

**검토:** 방역 수치·백신 성과·경기회복 찬사이며 신규 무역·산업 정책과 다르다. 유사한 백신 관련 C1128·C1225는 Noise이다. 보건 뉴스로 별도 관리할 수 있지만 시장 무관 여부와 Positive를 단정하지 않는다.

### C1233. 직접 재정 지급 요구를 Noise로 처리

**추적:** C1233, R2396 · 저장 UTC 2020-12-20 05:18:50+00:00 · 원문+시각 연결키 `b007f1fa42c422d238fda3b8a9766f64390630c296c896608bdf043adf184cbe`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1340527057151930369)

> Why isn’t Congress giving our people a Stimulus Bill? It wasn’t their fault, it was the fault of China. GET IT DONE, and give them more money in direct payments.

**기존:** Noise / `NOISE_Non_Market`.

**검토:** 코로나 농가지원·인프라 제안은 Positive인데 실업급여·직접 지급액 600/2000달러 협상은 Noise 또는 기업압박으로 분산되어 있다. 거시 재정정책 포함 여부를 사전 확정하고 금액·정책단계·신규성을 별도 코딩한다.

### C370. 보잉 개선 조언과 강제정책·제재의 경계

**추적:** C370, R25036 · 저장 UTC 2019-04-15 10:29:27+00:00 · 원문+시각 연결키 `63704e52a75b793a1f30ea7f0b95b0e745352d7e1eb02c289a2da678f3423992`. [독립 아카이브의 원글 링크](https://twitter.com/realDonaldTrump/status/1117736685721223168)

> What do I know about branding, maybe nothing (but I did become President!), but if I were Boeing, I would FIX the Boeing 737 MAX, add some additional great features, &amp, REBRAND the plane with a new name.No product has suffered like this one. But again, what the hell do I know?

**기존:** Negative / `NEG_Company_Tech_Pressure`.

**검토:** 737 MAX 개선·브랜드 변경에 대한 조언이다. 보잉 관련 발언은 맞지만 새로운 제재나 강제정책이 없고 사전 주가 방향도 확정하기 어렵다.

## 5. 스레드·리트윗·정보 강도를 별도 관리해야 한다

기존 분류 1,246행 중 RT 표시 또는 RT 접두어가 있는 글은 268행이다. 원본 전체에는 9,787행이 있다. RT는 트럼프가 다시 배포한 정보라는 의미가 있지만, 본인이 새 조치를 발표한 글과 동일한 정보 충격으로 간주할 수 없다. 원문 작성시각과 트럼프의 재전달시각을 둘 다 보존하고, 동일 정책사건에 `event_id`를 부여해 최초 공개와 반복 노출을 구분해야 한다.

529행은 본문의 앞 또는 끝에 `...`/`…`가 있다. 이는 **단편·생략 가능성 경보**이며 529개 모두 데이터가 잘렸다는 뜻은 아니다. 작성자가 이어 쓴 스레드, RT의 표시 길이 제한, 의도적인 말줄임이 섞여 있다. C567의 신규 관세 조치와 C568의 낙관적 후속 글을 하나의 사건으로 연결할 수 있지만, 서로의 단독 문장 부호까지 같아야 하는 것은 아니다.

정확한 반복 본문은 추가 19행이며 동일 본문에 신호나 세부유형이 다르게 붙은 사례는 없었다. 그렇더라도 문구를 조금 고친 재게시·RT·하루 사이의 사건 중첩은 남는다. 단순 개수 차이의 Net Signal은 같은 정책을 길게 나눠 쓴 사람이 더 강한 충격을 준 것처럼 보이게 할 수 있다.

스레드 복원에는 시간 제약이 필요하다. 뒤에 게시된 글을 이용해 앞선 시점의 정보집합을 완성하면 사후 정보가 섞인다. 최초로 조치가 확인되는 시각에서 사건을 발생시키고, 후속 글은 추가 정보로만 집계해야 한다. 날짜를 먼저 고친 뒤 가까운 시각의 스레드를 연결해야 12시간 오류 때문에 엉뚱한 글을 연결하는 문제도 줄일 수 있다.

아카이브의 최종 retweet/favorite 수는 발표 시점에 알려진 값이 아니다. 동시점 수집 이력이 없다면 설명용 인기도 지표로만 사용하고, 충격 표본 선정·사전 강도·포트폴리오 신호에는 사용하지 않아야 한다. VIX나 사후 수익률이 크게 움직인 날만 ‘진짜 충격’으로 선별하는 방식도 피해야 한다.

## 6. 시각과 거래일: 현재 집계는 재현되지만 원천 오류가 남아 있다

### 6.1 손상된 식별자와 원본 수집 범위

26,239개 ID가 모두 끝 두 자리 `00`으로 저장되어 있고, 서로 다른 두 RT가 같은 ID·같은 초를 갖는다. 작성시각+본문 조합의 중복은 0개이다. 64비트 Snowflake는 문자열로 보관해야 한다는 [X 공식 문서](https://docs.x.com/fundamentals/x-ids)와도 부합하는 문제다. 다만 각 ID의 원래 하위 자릿수는 이 파일만으로 복구할 수 없으므로 기존 숫자를 그대로 X 링크로 조립하지 않았다.

프로젝트의 [기존 공개 원본 JSON](https://github.com/ttzztztz/TrumpTwitterArchive)을 다시 내려받아 기간을 동일하게 제한했을 때, 로컬과 날짜+본문의 다중집합이 **26,239행 전부 일치**했다. 이는 로컬 추출이 해당 원본을 빠뜨리지 않았다는 뜻이며, 그 원본이 실제 트윗 전체를 완전히 보존했다는 독립 증명은 아니다. ID·시각 오류도 상위 원본에 이미 존재한다.

[별도 아카이브](https://github.com/MarkHershey/CompleteTrumpTweetsArchive)의 23,075행(고유 URL 23,065개)과 추가 대조하여 ID 근접 후보 **23,050행**의 교차키를 만들었다. 본문 유사도 0.8 이상은 **19,204행**이다. 나머지는 RT 길이·문자 인코딩·반복 문장 등이 달라 잠정 링크로만 보존한다. 별도 아카이브에서 근접 ID로 연결되지 않은 15행은 수집 범위·삭제·잘림 차이가 있는 미해결 대조 항목이며 곧바로 15개 누락 확정으로 세지 않았다. 두 아카이브는 같은 Twitter Archive 계열 자료일 수 있으므로 완전히 독립된 정답 자료라고 가정하지 않았다.

관측된 최종 게시일은 2021-01-08이다. 별도 아카이브도 같은 날의 계정 정지를 설명한다. 따라서 1월 20일까지 매일 트윗이 있어야 한다고 판단하면 안 된다. 반대로 UTC 자정부터 재임기간을 잡아 취임식(2017-01-20 17:00 UTC) 이전 글 3개를 포함한 경계는 연구 모집단 정의에 명시해야 한다.

### 6.2 12시간 어긋난 시각은 원천 파싱 문제를 시사한다

생성시각은 `((int(id) >> 22) + 1288834974657)` 밀리초로 재구성했다. 비트 배치와 epoch는 [Twitter의 원 구현](https://raw.githubusercontent.com/twitter-archive/snowflake/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala)에서 확인했다. 하위 ID 반올림 손상은 초 경계 주변의 밀리초 오차를 만들 수 있지만 12시간 차이를 설명하지 못한다. 그래서 2초 초과를 충돌 기준으로 사용했다.

원본 311행은 약 ±43,200초 차이가 나며, 기존 분류 안에는 19행이 있다. AM/PM 혼동과 일치하는 패턴이지만 당시 수집·변환 로그가 없어 **구체적인 발생 원인은 가설**로 남긴다. 원본 전체를 16시 기준으로 다시 매핑하면 **48행**의 거래일이 달라진다. 기존 분류에서는 아래 C466 한 행이 해당한다. 원본 전체의 거래일 변경에는 기존 분류 밖 글도 포함되므로, 19개 분류 시각 오류가 모두 이벤트일을 바꿨다고 표현하면 안 된다.

### 6.3 고정 16시 규칙과 실제 조기폐장을 구분

저장된 `date_utc`를 신뢰하면 1,246건 모두 프로젝트의 고정 16시 규칙을 정확히 재현한다. 그러나 NYSE의 실제 폐장시각을 적용하면 C1236은 다음 거래일로 이동해야 한다. 2020-12-24 13시 조기폐장은 [NYSE/ICE 당시 공식 공지](https://ir.theice.com/press/news-details/2019/NYSE-Group-Announces-2020-2021-and-2022-Holiday-and-Early-Closings-Calendar/default.aspx)와 대조했다. 시각 오류와 조기폐장을 함께 반영할 때 거래일 변경 대상은 총 2건이다.

### 거래일 변경이 필요한 기존 분류

| 글 | 저장 UTC | 검증 UTC·사유 | 기존 거래일 | 권고 거래일 |
| --- | --- | --- | --- | --- |
| C466 농가 재난지원법 | 2019-06-03 11:58:38 | Snowflake 23:58:38 UTC → NY 19:58, 장 마감 후 | 2019-06-03 | 2019-06-04 |
| C1236 백신 보급 | 2020-12-24 20:30:57 | NY 15:30; 당일 13시 조기폐장 이후 | 2020-12-24 | 2020-12-28 |

C1236은 분류 자체도 산업정책 호재로 보기 어려우므로, 향후 수정에서는 ‘날짜 이동’과 ‘분석 범위 제외/보건 테마 분리’를 따로 기록해야 한다. 현재 자료에서 매핑된 2행은 모두 Positive지만 실제 수정 후 신호일 수의 변화는 다른 글과의 동시 발생 여부에 따라 달라진다.

### 6.4 25개 집계열의 일치는 라벨의 타당성을 보장하지 않는다

원문 분류에서 Trade/Fed/Policy/Hard Tariff/Deal 관련 Count·Dummy·Pure Dummy·Net Signal·Retweet Sum을 독립 재집계했으며 25,175셀의 차이는 0이었다. 시장자료의 1,007개 거래일도 NYSE 일정과 일치한다. 반면 기존 라벨에서 발견한 범주·부호·누락 문제는 그대로 집계에 전달된다.

추가로 Policy Pure Positive 137일 중 13일에는 Fed_Neg_Dummy도 1이다. Policy Pure Negative 113일 중 14일도 Fed 공격과 겹친다. 이는 ‘순수’가 **모든 정책 테마를 통틀어 호재만/악재만 있다는 뜻이 아니라, 현재 Policy 정의 안에서 반대 신호가 없다는 뜻**임을 보여 준다. 연준과 무역을 별도 층으로 분석하고 교차 노출을 통제해야 한다. 특히 Powell과의 우호적 회동이 Policy Positive에 포함되고 Fed 공격은 Policy Negative에서 제외되는 비대칭은 먼저 해소할 필요가 있다.

## 7. 기존 시장효과 해석에서 유지할 것과 다시 검증할 것

이 감사는 분류·연결 품질 검토이며 새 시장효과 추정이 아니다. 앞선 결과의 p값을 그대로 재인용해 수정된 라벨에서도 결론이 유지된다고 주장하지 않았다. S&P 500의 비유의는 ‘효과 없음’이나 ‘산업 간 상쇄가 입증됨’과 같지 않다. 표본 선택·신호 정의·산업별 차이·시각 오차가 정리된 후 다시 비교해야 한다.

`empirical_context_sentiment.py`는 2·3일 복리수익률에서 전체 표본의 평균 복리수익률을 빼서 CAR라고 부른다. 고정 평균을 빼는 것은 같은 기간의 두 집단 평균차에는 영향을 주지 않지만, 사건별 기대수익률 모형에 기반한 표준적인 비정상수익률과는 다르다. 발표에서는 ‘전체 표본 평균을 차감한 누적수익률’로 명시하거나, 사건 전 추정구간으로 기대수익률을 추정하는 별도 모형을 사용해야 한다. 전체 표본 평균에는 사건 이후 정보가 들어가므로 실시간 전략 신호로 쓰지 않는다.

TNX_Return은 금리 수준의 상대적 변화율이다. TNX_Return의 집단 평균차가 −0.573%p라고 해서 10년물 금리가 57.3bp 떨어졌다는 뜻은 아니다. 금리 충격은 `100 × (TNX_Close[t] − TNX_Close[t−1])` bp로 별도 계산해야 한다. CNY=X와 다른 자산도 각자의 세션·가격 확정 시각을 확인해야 하며 미국 16시 일괄 매핑이 모든 글로벌 자산에 정확하다고 가정해서는 안 된다.

재추정 시에는 프로젝트 기준대로 T, T+1, CAR[0,+1], CAR[0,+2]를 모두 비교하고 Welch 검정(`equal_var=False`)을 유지한다. 신호가 연속한 날에는 누적 창이 겹치므로 관측 독립성 문제가 생긴다. 사건 클러스터 또는 시계열 블록을 반영한 추론을 보완하고, 다수 자산·기간·비교의 다중검정도 표시해야 한다. 부호와 표본을 시장 결과를 보고 조정하지 않는 것이 우선이다.

## 8. 권고 분류체계와 수정 순서

하나의 글에 하나의 유형·부호만 강제하기보다, 독립적인 필드를 두는 것이 재현성과 금융 해석을 함께 개선한다. 기존 열은 보존하고 새 버전의 감사 열을 추가하는 방식이 적절하다.

### 권고 분류 필드

| 필드 | 허용값·설계 | 목적 |
| --- | --- | --- |
| themes | Trade / Fed / ECB / FX / Firm / Farm / Fiscal / Health / Geopolitics (다중 선택) | 복합 주제 강제 단일화 방지 |
| trade_stance | Escalation / Deescalation / Mixed / Neutral / Uncertain / NA | 협상갈등 방향을 별도 기록 |
| monetary_stance | Easing / Tightening / Neutral / Uncertain / NA | Fed 비난 어조와 정책방향 분리 |
| action_stage | Implemented / Announced / Conditional_Threat / Investigation / Talks / Advocacy / Commentary | 직접 조치와 수사·기대 구분 |
| novelty | New / Update / Repeat / Retrospective / Unknown | 사후 홍보와 새 정보 구분 |
| asset_exposure | 수혜·피해 기업/산업을 텍스트 근거로 복수 기록 | 시장 전체 단일 부호 강제 금지 |
| context_status | Sufficient / Thread_Required / Link_Required / Media_Required | 본문 부족을 Noise와 분리 |
| speaker_type | Trump_Original / Self_RT / Third_Party_RT / Quote | 최초 발언과 재배포 구분 |
| source_time_verified | 원시 문자열 + Snowflake + 검증 근거 | 정확한 정보집합 시점 보존 |
| event_id / event_first_public_at | 동일 정책사건 묶음 / 최초 공개시각 | 스레드·재게시 중복과 시점 편향 관리 |
| review_state | Retain / Revise / Ambiguous / Context_Required / Out_Of_Scope | 미확정을 확정값으로 덮지 않음 |

수정은 다음 순서로 진행하는 것이 타당하다.

1. 기존 세 파일의 체크섬을 고정하고, 원래 ID와 문자열 정밀 ID·감사용 복합키를 별도 보관한다. 생성시각과 충돌하는 311행 및 조기폐장일의 매핑부터 정리한다.
2. 기존 연구의 범위를 무역·연준 중심으로 둘지, 기업·거시·재정·보건까지 포함할지 명시한다. 연구 범위를 넓히면 거시·재정 후보 858건뿐 아니라 키워드 없는 글도 포함한 전체 텍스트 분류가 필요하다.
3. 추가 분류 필요 목록과 기존 수정 권고를 다축 체계로 재코딩한다. 애매한 글은 Uncertain/Context_Required로 남기고, 독립 평가자 2인이 같은 코드북으로 판단한 뒤 불일치를 조정한다. 현재 감사만으로 평가자 간 일치도·정확도를 산출하지 않는다.
4. 같은 정책의 반복 게시와 스레드를 사건 단위로 연결하되 최초 공개시각을 보존한다. 최종 RT 수·VIX·수익률을 사건 선정 기준으로 쓰지 않는다.
5. 1,007일의 기존 열을 보존한 파생 데이터에 재집계하고, 동일 표본·기간·단위를 유지해 T/T+1/2일/3일 반응과 표본수 변화를 함께 보고한다. 재추정 전에는 기존 발표 결론을 강화하는 근거로 이 감사를 사용하지 않는다.

## 9. 재현 방법과 산출물

저장소 루트에서 `python scripts/audit_tweet_archive_sources.py`로 저장된 공개 참조 사본과의 교차키를 재현하고, `python scripts/audit_context_classification.py`를 실행하면 원본·분류·시장의 자동 감사 CSV와 JSON이 생성된다. 그 뒤 `python scripts/build_tweet_audit_report.py`를 실행하면 명시적 검토 결정과 연결한 원장 및 이 보고서가 생성된다. 참조 사본이 없을 때만 첫 스크립트에 `--download-missing`을 지정해 공개 URL에서 받는다. NYSE 일정 검증에는 requirements에 명시한 `pandas_market_calendars`를 사용한다. 난수 시드는 42이며 표본 추출은 하지 않았다.

검토 결정은 `review_decisions.json`에 기록되어 있고, 원문 1,246건을 검토했다는 서술은 이 작업의 실제 열람 기록을 뜻한다. 재실행 스크립트가 의미 판독을 다시 수행하는 것은 아니다. 기존 판정 근거를 데이터에 연결해 재현할 뿐이다. 원본 스냅샷이나 결정 파일이 바뀌면 보고서의 버전과 수치를 함께 갱신해야 한다.

공개 원본과 별도 아카이브는 이 폴더에 참조용 사본을 저장했다. 다운받은 시점의 파일 해시를 manifest에 보관했으며, 정밀 ID 교차키는 근접 ID와 본문 유사도에 기초한 잠정 연결이다. 링크 열람 성공이나 26,239건의 정확한 ID 복원을 주장하지 않는다. 기사·영상·보호된 데이터에 대한 접근을 우회하지 않았다.

### 검토 근거 파일

| 파일 | 내용 |
| --- | --- |
| full_corpus_review_coverage.csv | 26,239행 전수 스크리닝과 개별 의미 열람 여부 |
| existing_review_ledger.csv | 1,246행 기존 라벨·제안·이유·원문·시각 검증 |
| omission_review_ledger.csv | 437행 확대 후보, 포함 필요·제외 예시·보류 구분 |
| confirmed_scope_omissions.csv | 추가 분류가 필요한 59행 최소 확인 목록 |
| raw_timestamp_audit.csv | 모든 원문 시각과 Snowflake 차이, 311행 경보 |
| trading_date_audit.csv | 고정 16시·실제 NYSE 폐장·Snowflake별 매핑 비교 |
| daily_aggregation_mismatches.csv | 현재 라벨을 재집계한 25열 불일치 목록(0행) |
| exact_id_crosswalk.csv | 별도 아카이브와의 근접 ID·본문 유사도·URL 대조 |
| audit_summary.json / review_summary.json | 자동 및 개별 검토의 집계값 |
| review_decisions.json | 명시적 범주 수정·애매 사례·추가 분류 필요 결정 |
| source_manifest.json | 입력·외부 참조의 SHA-256 및 출처 |

## 10. 출처와 증거 한계

**[S1] 로컬 원문** `data/trump_tweets_1st_term_raw.csv`. 저장된 게시시각 기준 2017-01-20~2021-01-08, 26,239행. 입력 원문을 그대로 보존했다.

**[S2] 기존 문맥 분류** `data/trump_policy_tweets_context_classified.csv`, 1,246행. 기존 신호·세부유형·한국어 근거는 감사 대상이지 독립 정답이 아니다. 본문의 모든 트윗 인용은 사용자가 제공한 로컬 원문에서 가져왔다.

**[S3] 시장 자료와 생성 코드** `data/trump_market_extended_data.csv`, `scripts/audit_trade_tweets.py`, `scripts/empirical_context_sentiment.py`, `scripts/pipeline_extended.py`. 현재 집계·후보 선택·CAR 정의를 확인했다. 시장 가격을 새로 내려받거나 원자료의 가격 정확성까지 감사하지 않았다.

**[S4] 기존 수집 원본** [ttzztztz/TrumpTwitterArchive](https://github.com/ttzztztz/TrumpTwitterArchive). 공개 JSON을 내려받아 기간 제한 후 날짜·본문 다중집합을 로컬과 대조했다. 상위 원본과의 동일성만 확인한 것이며, 공통 오류까지 제거되는 것은 아니다.

**[S5] 보조 아카이브** [MarkHershey/CompleteTrumpTweetsArchive](https://github.com/MarkHershey/CompleteTrumpTweetsArchive). 공개 CSV의 문자열 URL 및 본문으로 ID 교차키를 작성했다. 인코딩·잘림·중복·수집 범위가 달라 독립 정답으로 간주하지 않았다.

**[S6] X 식별자 문서 및 Twitter 원 구현** [X IDs](https://docs.x.com/fundamentals/x-ids), [IdWorker.scala](https://raw.githubusercontent.com/twitter-archive/snowflake/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala). ID의 정밀 보관 원칙과 생성시각 계산식을 검증했다.

**[S7] 거래소 일정** [NYSE/ICE 2020~2022 휴장·조기폐장 공지](https://ir.theice.com/press/news-details/2019/NYSE-Group-Announces-2020-2021-and-2022-Holiday-and-Early-Closings-Calendar/default.aspx), [NYSE 정규 거래시간](https://www.nyse.com/trade/hours-calendars). 2020-12-24 조기폐장 사례와 정규 16시 마감을 확인했다. 전체 일정 재계산에는 설치된 NYSE 캘린더 패키지를 사용했으며 모든 과거 날짜를 별도 공식 공지와 하나씩 대조한 것은 아니다.

**감사일:** 2026-11-02, Asia/Seoul. 현재 보고서의 완성은 정해진 감사 범위의 결과를 문서화했다는 의미다. 원글 전량의 의미 판정, 모든 매체 복원, 수정 라벨 확정, 수정 후 시장효과 검증이 모두 완료됐다는 뜻은 아니다.


<!-- restoration-update-2026-11-03 -->
## 2026-11-03 추가 문맥 복원

보류 3,627건에 대한 아카이브·링크·전후 글 조사와 잠정 재판정은 [추가 문맥 복원 보고서](restoration/RESTORATION_REPORT.md)를 참조한다. 확정되지 않은 후보는 기존 분류에 자동 반영하지 않았다.
