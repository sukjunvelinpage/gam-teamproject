# [글로벌금융자산관리 1조] 트럼프 1기 트윗 충격의 다각도 실증 분석 및 자산배분 전략

> **숭실대학교 글로벌금융자산관리 (김수현 교수님) 팀프로젝트 1조**  
> **발표 대주제:** *"소음(Noise) 뒤에 숨겨진 진짜 신호(Signal): 트럼프 트윗 충격의 자산군·국가별 전이 지도와 글로벌 자산배분 전략"*  
> **핵심 질문:** *"대통령의 트윗 한 줄에 거시경제 지수(S&P 500)가 정말로 흔들렸는가, 아니면 심리(VIX)와 특정 산업, 채권, 그리고 상대국(중국)으로 흘러들어갔는가?"*

---

## 1. 프로젝트 구성 파일

| 파일/디렉터리 | 구분 | 설명 |
| :--- | :---: | :--- |
| [`pipeline_extended.py`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/pipeline_extended.py) | 파이프라인 | 트윗 2.6만 건 + 13개 글로벌 자산 OHLC 수집, 미국 동부시각 정렬 및 병합 파이프라인 |
| [`trump_market_extended_data.csv`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/trump_market_extended_data.csv) | 데이터셋 | **1,007개 정규 거래일 × 95개 변수**로 구성된 최종 실증 데이터셋 (결측치 0건) |
| [`empirical_analysis_extended.py`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/empirical_analysis_extended.py) | 분석 코드 | 자산군·섹터별 Welch's $t$-test 및 2일 누적 비정상수익률(CAR) 통계 검정 스크립트 |
| [`extended_empirical_summary.csv`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/extended_empirical_summary.csv) | 분석 결과 | 전 자산군별 트윗 발생일 vs 미발생일 평균, 차이($\Delta$), $t$-stat, $p$-value 요약표 |
| [`generate_presentation_charts.py`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/generate_presentation_charts.py) | 시각화 | 15분 발표용 고해상도 핵심 차트 4종 자동 렌더링 스크립트 (Pure matplotlib) |
| [`presentation_charts/`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/presentation_charts) | 시각화 산출물 | 발표 슬라이드 삽입용 고품질 PNG 차트 4종 저장 디렉터리 |
| [`presentation_script_15min.md`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/presentation_script_15min.md) | 발표 자료 | **슬라이드 15장 기준 15분 발표용 상세 발표자 대본 및 시간 배분 가이드** |
| [`gam_final_project_plan.md`](file:///C:/Users/StoneXI/.gemini/antigravity/brain/1171441f-9100-41bf-8c65-4871aaf0006f/gam_final_project_plan.md) | 연구 계획서 | 글로벌 자산배분 관점의 연구 프레임워크 및 단계별 로드맵 명세서 |
| [`requirements.txt`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/requirements.txt) | 환경 설정 | 프로젝트 실행에 필요한 파이썬 라이브러리 목록 (`pandas`, `numpy`, `scipy`, `yfinance`, `matplotlib`) |
| [`GEMINI.md`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/GEMINI.md) | 협업 규칙 | **Antigravity 팀 프로젝트 공통 룰셋** (데이터 무결성, 통계 표준, Git 컨벤션) |
| [`.agents/rules/`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/.agents/rules) | 모듈형 규칙 | 도메인 가이드라인, 파이썬/시각화 표준, Git 워크플로우 세부 룰셋 |

---

## 2. 자료 출처 (Data Sources)

### 2.1. 트럼프 트윗 아카이브 (Twitter / X)
* **출처:** Trump Twitter Archive (TTA) 오픈소스 공공 저장소
* **엔드포인트:** `https://raw.githubusercontent.com/ttzztztz/TrumpTwitterArchive/master/trump.json`
* **수집 범위:** 트럼프 1기 공식 재임 기간(**2017.01.20 ~ 2021.01.20**) 동안 작성된 트윗 **총 26,239건 전수 수집**
* **추출 필드:** 작성 일시(UTC), 트윗 본문(`text`), 리트윗 수(`retweets`), 좋아요 수(`favorites`)
* **이벤트 키워드 분류 (정규식 단어 경계 검증):**
  * **무역/관세 트윗 (`Trade_Tweet`):** `tariff`, `tariffs`, `trade war`, `china`, `beijing`, `xi jinping` (총 729건 / 331개 거래일 매핑)
  * **연준/금리 트윗 (`Fed_Tweet`):** `fed`, `federal reserve`, `powell`, `interest rate`, `rate cut`, `quantitative` (총 175건 / 111개 거래일 매핑)

### 2.2. 글로벌 금융시장 시계열 데이터 (Yahoo Finance API)
2017년 1월 20일부터 2021년 1월 20일까지 **총 1,007개 미국 정규 거래일**의 일별 시가·고가·저가·종가(OHLC) 및 일별 수익률을 전수 무결 수집하였습니다.

| 자산 분류 | 티커 (Ticker) | 명칭 및 연구 목적 |
| :--- | :--- | :--- |
| **거시 주식** | `^GSPC` | **S&P 500 지수:** 미국 증시 벤치마크 (거시 펀더멘털 반응성 검증) |
| **시장 심리** | `^VIX` | **CBOE 변동성 지수:** 투자자 공포 및 내재 변동성 기대치 |
| **달러 통화** | `DX-Y.NYB` / `UUP` | **달러 인덱스 & 달러 ETF:** 글로벌 기축통화 가치 변동 추적 |
| **관세 수혜 산업** | `NUE`, `SLX` | **Nucor 철강사 & 철강 ETF:** 관세 보호 무역정책 수혜 섹터 |
| **관세 피해 섹터** | `XLI`, `SOXX` | **산업재 ETF & 반도체 ETF:** 글로벌 공급망 교란 피해 섹터 |
| **타깃 개별 기업** | `BA`, `CAT`, `AAPL` | **보잉, 캐터필러, 애플:** 트윗 직접 비판 및 대중국 보복관세 표적 기업 |
| **연준 / 채권** | `^TNX`, `SHY`, `XLF` | **미 10년물 국채 금리, 1-3년 단기 국채, 금융 ETF:** 금리 인하 압박 반응 |
| **중국 / 안전자산** | `FXI`, `CNY=X`, `GLD` | **중국 대형주 ETF, 달러-위안 환율, 금(Gold):** 무역전쟁 해외 전이 및 피난처 |

---

## 3. 시점 정렬(Trading Hours Alignment) 규칙

트윗 작성 시점과 금융시장 체결 시점 간의 시차로 인한 정보 왜곡(Look-ahead bias)을 방지하기 위해 다음 엄밀한 규칙을 적용하였습니다:

1. **타임존 정규화:** 모든 트윗의 작성 시각(UTC)을 뉴욕 현지 시각(`America/New_York`, EST/EDT 서머타임 자동 반영)으로 변환.
2. **거래일 매핑:**
   * **00:00 ~ 16:00 EST (장 개장 전 및 정규 장중):** 당일($T$) 거래일로 매핑 (휴일/주말인 경우 직후 첫 거래일).
   * **16:00 ~ 23:59 EST (정규 장 마감 후):** 익일($T+1$) 거래일로 전환 후 직후 첫 거래일로 매핑.
3. **일별 집계 변수 생성:**
   * `Trade_Tweet_Dummy`: 해당 거래일로 매핑된 무역/관세 트윗 존재 여부 (1 or 0, 총 331일)
   * `Fed_Tweet_Dummy`: 해당 거래일로 매핑된 연준/금리 트윗 존재 여부 (1 or 0, 총 111일)
   * 리트윗 및 좋아요 합계(`Retweet_Sum`, `Favorite_Sum`): 시장 주목도 가중치 산출

---

## 4. 15분 발표 핵심 실증 결과 요약

### ① 출발점: 거시 지수(S&P 500) vs 시장 심리(VIX)의 괴리
* **S&P 500 일별 수익률:** 트윗 발생일 $+0.007\%$ vs 미발생일 $+0.088\%$ ($\Delta = -0.080\%p$, $t = -0.840$, **$p = 0.4013$ 비유의**)
* **S&P 500 2일 누적 CAR:** 트윗 발생일 $+0.035\%$ vs 미발생일 $-0.017\%$ ($\Delta = +0.053\%p$, **$p = 0.6386$ 비유의**)
* **VIX 일별 등락률:** 트윗 발생일 **$+1.483\%$** vs 미발생일 **$-0.092\%$** ($\Delta = \mathbf{+1.575\%p}$, $t = +2.575$, **$p = 0.0102$ ★★ 유의수준 1% 유의**)
> **해석:** 시장 전체는 트윗 당일 하락 압력을 받더라도 익일 빠르게 회복하여 누적 충격이 0에 수렴했으나, 투자자의 불안 심리(변동성)는 즉각 폭증했습니다.

### ② 미국 내 산업 비대칭성: 상쇄 효과(Offsetting Effect)
* **보잉 (`BA`):** 트윗 발생일 하루 평균 **$-0.223\%p$ 언더퍼폼**
* **캐터필러 (`CAT`):** 트윗 발생일 하루 평균 **$-0.126\%p$ 언더퍼폼**
* **반도체 ETF (`SOXX`):** 트윗 발생일 하루 평균 **$-0.119\%p$ 언더퍼폼**
* **산업재 ETF (`XLI`):** 트윗 발생일 하루 평균 **$-0.113\%p$ 언더퍼폼**
* **애플 (`AAPL`):** 트윗 발생일 하루 평균 **$-0.097\%p$ 언더퍼폼**
> **해석:** S&P 500 전체가 평온했던 이유는 관세 보호를 받는 미국 철강 산업과, 글로벌 공급망에 노출된 제조·기술주의 하락이 지수 내부에서 서로를 상쇄시켰기 때문입니다.

### ③ 연준 트윗과 채권/금리 시장
* **미국 10년물 국채 금리 (`TNX`):** 연준 비판 트윗 발생 시 **$-0.208\%p$ 하락 압력** (통화 완화 기대 선반영)
* **금융 섹터 ETF (`XLF`):** 순이자마진(NIM) 축소 우려로 **$-0.029\%p$ 둔화**
> **해석:** 주식보다 채권 시장이 대통령의 파월 비판 트윗을 연준의 금리 인하 압박으로 먼저 해석하여 가격에 반영했습니다.

### ④ 무역전쟁의 진앙: 중국 시장 및 안전자산 전이
* **안전자산 금 (`GLD`):** 무역 트윗 발생 시 **$+0.071\%p$ 추가 상승** (피난처 자금 유입)
* **달러-위안 환율 (`CNY=X`):** **$+0.020\%p$ 상승** (위안화 가치 절하 압력)
> **해석:** 트럼프의 관세 트윗 포격은 미국 내부보다 상대국인 중국 통화와 안전자산으로 거대한 자금 이동을 유발했습니다.

---

## 5. 교수님 평가 기준 부합 및 글로벌 자산배분(GAM) 시사점

1. **이해도 우선:** 복잡한 계량 수식 대신, 직관적인 **[트윗 발생일 vs 미발생일] 평균 차이 검정($t$-test)** 및 4장의 핵심 비교 차트 중심으로 구성.
2. **선명한 단 하나의 스토리:**  
   *"거시 지수(S&P 500)는 소음이었다. 진짜 충격은 지수 내부의 섹터 불균형, 채권 금리, 그리고 중국으로 분산되었다."*
3. **글로벌 자산배분(GAM) 실무 원칙:**
   * **소음에 의한 거시 지수 패닉 셀링 금지:** S&P 500 지수는 1~2일 내에 회복하므로 투매하지 말 것.
   * **섹터 간 페어 트레이딩 (Pair Trading):** 관세 수혜주(철강/내수) Long + 피해 기업(보잉/글로벌 수출주) Short.
   * **다자산 테일 리스크 헤지:** 정치적 노이즈 발생 시 금(GLD)과 국채 바스켓을 활용한 방어 포트폴리오 구축.

---

## 6. 실행 방법

```bash
# 1. 의존 패키지 설치
pip install -r requirements.txt

# 2. 확장 데이터 수집 및 시점 정렬 파이프라인 실행
python pipeline_extended.py

# 3. 다각도 실증 통계 검정 실행
python empirical_analysis_extended.py

# 4. 15분 발표용 고해상도 차트 4종 생성
python generate_presentation_charts.py
```

---

## 7. 팀 협업 및 Antigravity 에이전트 룰셋 안내

모든 팀원이 동일한 품질과 일관된 기준(데이터 무결성, 통계 검정, 시각화 스타일, Git 규칙)으로 개발할 수 있도록 Antigravity 룰셋이 구축되어 있습니다.

* **룰셋 파일:**
  * [`GEMINI.md`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/GEMINI.md) / [`AGENTS.md`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/AGENTS.md): 저장소 루트에 위치하며, Antigravity 에이전트 구동 시 자동 로드되는 기본 원칙.
  * [`.agents/rules/01_project_guidelines.md`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/.agents/rules/01_project_guidelines.md): 연구 질문, 데이터 무결성(1,007일 결측치 0건 유지), 시점 정렬 규칙.
  * [`.agents/rules/02_python_code_standards.md`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/.agents/rules/02_python_code_standards.md): Python 3.10+, PEP 8, Welch's $t$-test 표준, Matplotlib 고해상도 한글 폰트 설정.
  * [`.agents/rules/03_git_workflow.md`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/.agents/rules/03_git_workflow.md): Feature 브랜치 전략, Conventional 커밋 메시지 컨벤션, 충돌 방지 원칙.
* **팀원 적용 방법:**
  * 레포지토리를 GitHub에서 clone한 후 Antigravity(IDE 또는 데스크톱 앱)에서 해당 폴더를 열면, 에이전트가 위 룰셋을 **별도 설정 없이 자동으로 인식 및 적용**합니다.
