# 트윗 분류 검수 가이드 (팀원용)

## 1. 왜 하나요

발표에 쓴 무역 트윗 1,246건은 LLM(AI)이 먼저 긍정/부정/소음으로 나눴습니다.
발표 Q&A에서 "AI 분류를 어떻게 믿나요?"라는 질문이 나오면, "사람이 100건을 따로 읽어 봤더니 ○○% 같았다"고 답하려고 합니다.

그래서 **AI 결과를 보지 않고 직접 판단해 주는 것**이 이번 작업의 핵심입니다. 정답 맞히기가 아닙니다. AI와 다르게 판단한 건도 그 자체로 의미 있는 결과입니다.

## 2. 작업 방법

- **파일:** `label_check_sample_100.xlsx`
- **분량:** 트윗 100건, 1~1.5시간 정도
- **순서**
  1. 이 문서(또는 엑셀의 `2_분류기준`, `3_예시` 시트)를 먼저 읽는다.
  2. `4_라벨링` 시트의 **노란 칸 3개만** 채운다.
     - **내 분류:** 긍정 / 부정 / 소음 (드롭다운)
     - **확신도:** 확실 / 애매
     - **한 줄 근거:** 어떤 단어나 행동을 보고 판단했는지 짧게 적는다. 애매한 건은 꼭 적는다.
  3. 파일을 그대로 돌려준다. `audit_key` 열은 수정하지 않는다.
- **회색 칸(한국어 번역, 당시 맥락)은 참고용입니다.**
  - AI로 작성했기 때문에 사실관계가 틀렸을 수 있습니다. 이상하면 원문을 기준으로 판단하고 메모해 주세요.
  - '좋은 소식/나쁜 소식' 같은 평가와 그날 주가 움직임은 일부러 적지 않았습니다. 분류 결과로 주가 반응을 검정하기 때문에, 주가를 보고 분류하면 결론이 순환논리가 됩니다.
- **지켜 주세요**
  - 다른 팀원이나 AI에게 개별 트윗의 정답을 묻지 않는다.
  - `data/` 폴더의 기존 분류 결과를 열어 보지 않는다.
  - 번역기(파파고, 구글 번역)는 써도 된다. 판단은 직접 한다.
  - 한 건에 1분 넘게 고민하게 되면 가장 가까운 쪽을 고르고 '애매'로 표시한 뒤 넘어간다.

## 3. 분류 기준

**핵심 질문 하나:**
> 이 트윗을 본 투자자(주식·채권·환율)가 "미국 무역·경제 정책의 불확실성이 **줄었다**"고 느낄까, "**커졌다**"고 느낄까, 아니면 "**시장과 상관없는 말**"로 넘길까?

| 단계 | 확인할 것 | 결과 |
|---|---|---|
| 1 | 무역·관세·중국 협상·연준 금리·특정 기업·미국 산업과 경제 이야기가 **실제로** 있나? 키워드만 있고 내용이 선거·코로나·탄핵·동명이인 이야기라면 '없다'로 본다. | 없으면 **소음** |
| 2 | 갈등이 풀리는 방향인가? 합의·서명·타결, 관세 유예·연기·면제, 협상 순항, 상대국의 미국산 구매, 미국 내 기업 투자·공장·일자리, 미국 경제·증시 호황 자랑, 농가 지원금이 여기에 해당한다. | **긍정** |
| 3 | 갈등이 커지는 방향인가? 신규 관세 부과·세율 인상·위협, 관세를 계속 쓰겠다는 과시, 상대국의 무역적자·환율조작·약속 불이행 비난, 특정 기업 공개 압박·제재, 연준·파월 공격과 금리 인하 압박이 여기에 해당한다. | **부정** |

**추가 규칙**
- **좋은 말과 나쁜 말이 섞여 있을 때:** 결론, 즉 마지막에 하겠다고 한 행동을 따른다.
  예: "협상이 잘 되고 있다. 하지만 안 되면 25% 관세" → **부정**
- **리트윗(RT):** 리트윗한 글의 내용으로 똑같이 판단한다.
- **잘린 트윗(`...`로 끝남):** 보이는 부분만으로 판단한다. 내용이 거의 없으면 가장 가까운 쪽을 고르고 '애매'로 표시한다.

### 헷갈리기 쉬운 경우

| 경우 | 판단 | 이유 |
|---|---|---|
| "Tariffs are working", "billions pouring in" 같은 좋은 단어 | 부정 | 단어가 아니라 내용을 본다. 관세를 거둘 생각이 없다는 뜻이라 갈등이 이어진다. |
| 관세 언급이 있지만 주인공이 미국 기업의 투자 성과 | 긍정 | 주어가 "기업이 미국에 투자했다"면 긍정, "관세가 옳다/계속한다"면 부정이다. |
| 연준에 금리 인하 요구 | 부정 | 금리 인하가 주가에는 좋을 수 있다. 하지만 이 분류에서는 "대통령이 중앙은행을 공격한다"는 점을 불확실성 증가로 본다. |
| 상대국이 약속을 안 지킨다는 불만 | 부정 | 새 관세가 없어도 합의 불이행 비난은 갈등을 키운다. |
| "China Virus", 바이든·헌터 공격, 선거·탄핵 | 소음 | 중국이나 무역 단어가 있어도 정책 조치가 없으면 시장 신호가 아니다. |
| fed up / Sidney·Colin·Dina Powell / apple cart / Shawn Steel / man of steel | 소음 | 연준·애플·철강과 관계없는 관용어나 동명이인이다. |

## 4. 확실한 예시와 근거

아래 예시는 검수할 100건에 들어 있지 않습니다.

### 긍정

| 트윗 (요약) | 판단 근거 |
|---|---|
| *"I will be signing our very large and comprehensive Phase One Trade Deal with China on January 15..."* | 1단계 무역합의 서명 날짜를 확정해 발표했다. 합의는 갈등 완화다. |
| *"China just announced that their economy is growing much slower... They have just suspended U.S. Tariff Hikes... It could happen, and rather soon!"* | 앞부분은 중국 비난이다. 하지만 핵심 사실이 "중국이 관세 인상을 유예했다"와 "곧 합의 가능"이라 결론이 완화 쪽이다. |
| *"CHINA HAS ALREADY BEGUN AGRICULTURAL PURCHASES FROM OUR GREAT PATRIOT FARMERS"* | 중국의 미국산 농산물 구매 시작은 합의 이행이다. |
| *"Having dinner tonight with Tim Cook of Apple. They will be spending vast sums of money in the U.S."* | 애플의 미국 내 대규모 투자를 언급했다. 미국 기업의 투자 호재다. |
| *"Congrats to @U_S_Steel for investing $1+ BILLION... Tariffs are working..."* | "Tariffs are working"이 있지만 주인공은 US스틸의 미국 투자다. 기업 투자 성과가 핵심이면 긍정이다. |

### 부정

| 트윗 (요약) | 판단 근거 |
|---|---|
| *"The process has begun to place additional Tariffs at 25% on the remaining 325 Billion Dollars..."* | 3,250억 달러어치에 25% 추가 관세 절차를 시작했다. 세율과 금액이 구체적인 신규 관세라 가장 확실한 부정이다. |
| *"I am a Tariff Man... We are right now taking in $billions in Tariffs."* | 관세를 계속 쓰겠다는 의지를 과시했다. wealth, billions 같은 좋은 단어가 있어도 내용은 무역갈등 지속이다. |
| *"Tariffs are working far better than anyone ever anticipated. China market has dropped 27%..."* | 관세 효과를 자랑하고 중국 시장 폭락을 언급했다. 관세를 거둘 생각이 없다는 신호다. |
| *"Our pathetic, slow moving Federal Reserve, headed by Jay Powell..."* | 연준과 파월을 공개적으로 비난하며 금리 인하를 압박했다. 중앙은행 공격은 불확실성 증가로 본다. |
| *"Early this year Harley-Davidson said they would move much of their plant operations... to Thailand..."* | 할리데이비슨이라는 특정 기업을 지목해 공개 비판했다. 개별 기업 압박이다. |
| *"...China is letting us down in that they have not been buying the agricultural products..."* | 중국이 약속한 농산물 구매를 하지 않는다고 공개적으로 불만을 표했다. 합의 불이행 비난은 갈등 고조다. |

### 소음

| 트윗 (요약) | 판단 근거 |
|---|---|
| *"RT: Sidney Powell and Lin Wood hit Georgia with 104-page lawsuit."* | 여기서 Powell은 연준 의장이 아니라 대선 소송 변호사 시드니 파월이다. 동명이인이다. |
| *"European Countries are sadly getting clobbered by the China Virus."* | China가 들어 있지만 코로나 상황 이야기다. 무역이나 관세 조치가 없다. |
| *"...forest fires in California... Remedy now, or no more Fed payments!"* | 여기서 Fed payments는 연준이 아니라 산불 연방 지원금이다. 키워드 오탐이다. |
| *"Somebody please wake up Mitt Romney... my statement on China pertained to corruption, not politics."* | 우크라이나 통화와 탄핵을 둘러싼 정치 공방이다. China는 부패 조사 맥락에서 나왔다. |

---

## 5. (정리 담당용) 결과 계산과 발표 활용

팀원이 파일을 돌려주면 아래 명령으로 계산합니다.

```bash
python scripts/score_label_check.py docs/label_check/label_check_sample_100.xlsx
```

- 베트남어판(`label_check_sample_100_vi.xlsx`, 가이드 `LABELING_GUIDE_vi.md`)은 같은 100건이 같은 순서로 들어 있습니다. 같은 명령에 파일 경로만 바꾸면 됩니다.
- 단순 일치율, Cohen's kappa, 혼동표, '확실'로 표시한 건만 본 일치율이 출력됩니다.
- 불일치한 건은 `docs/label_check/label_check_disagreements_<파일이름>.csv`에 AI 판정 사유와 함께 저장됩니다. 팀 토의 때 이 파일을 같이 보면 됩니다.
- 표본은 `scripts/build_label_check_sample.py`가 만듭니다(`random_state=42`, 기존 분류 비율대로 긍정 29 / 부정 34 / 소음 37). 다시 실행해도 같은 100건이 나옵니다.

**발표에서 말하는 방법 (예시)**
> "트윗 분류는 AI로 1차 작업을 했고, 팀원이 AI 결과를 보지 않은 채 무작위 100건을 직접 다시 분류했습니다. 그 결과 ○○건이 일치했습니다(kappa ○.○○). 서로 다르게 판단한 건은 주로 △△ 유형이었습니다."

kappa는 "우연히 맞을 확률을 뺀 일치도"입니다. 보통 0.6 이상이면 상당히 일치한다고 봅니다. 일치율이 낮게 나와도 숨기지 말고, 어떤 유형에서 갈렸는지를 한계로 말하는 편이 Q&A에서 더 유리합니다.
