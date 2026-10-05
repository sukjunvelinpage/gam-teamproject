# 트럼프 1기 주요 트윗과 금융시장 지표 영향 실증 분석

> **프로젝트 목표:**  
> 트럼프 1기 재임 기간(2017.01.20 ~ 2021.01.20) 동안 작성된 트윗이 미국 주요 금융시장 지표(S&P 500, 달러 인덱스, VIX)에 미친 영향을 실증 분석하기 위한 원천 데이터 수집, 시점 정렬(Trading Hours Alignment), 전처리, 병합 및 통계 검정 파이프라인.

---

## 1. 프로젝트 구성 파일

| 파일명 | 설명 |
| :--- | :--- |
| [`pipeline.py`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/pipeline.py) | 트윗 아카이브 다운로드, 키워드 필터링, yfinance 금융 지표 수집, 거래일 매핑 및 병합 전체 파이프라인 |
| [`trump_market_event_data.csv`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/trump_market_event_data.csv) | 1,007개 정규 거래일 × 30개 컬럼으로 구성된 최종 분석용 병합 데이터셋 (결측치 0건) |
| [`empirical_analysis.py`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/empirical_analysis.py) | 무역 및 연준 트윗 이벤트 발생일 vs 미발생일 간의 평균 차이 검정($t$-test) 스크립트 |
| [`requirements.txt`](file:///C:/Users/StoneXI/Antigravity_dev/gam-teamproject/requirements.txt) | 프로젝트 실행에 필요한 파이썬 라이브러리 목록 |

---

## 2. 데이터 출처 (Data Sources)

1. **트럼프 트윗 아카이브 (Twitter/X):**
   - **출처:** Trump Twitter Archive (TTA) 오픈소스 저장소
   - **엔드포인트:** `https://raw.githubusercontent.com/ttzztztz/TrumpTwitterArchive/master/trump.json`
   - **범위:** 트럼프 1기 공식 재임 기간(2017.01.20 ~ 2021.01.20) 동안의 트윗 총 **26,239건** 전수 수집
   - **필드:** 작성 시각(UTC), 트윗 본문, 리트윗 수, 좋아요 수

2. **금융시장 데이터 (Yahoo Finance API):**
   - **S&P 500 지수 (`^GSPC`):** S&P Dow Jones Indices / NYSE / NASDAQ 종합
   - **미국 달러 인덱스 (`DX-Y.NYB`):** ICE (Intercontinental Exchange)
   - **달러 ETF (`UUP`):** Invesco DB US Dollar Index Bullish Fund (보완용)
   - **CBOE 변동성 지수 (`^VIX`):** Chicago Board Options Exchange (변동성 기대치)
   - **기간:** 2017-01-20 ~ 2021-01-20 (총 **1,007개** 정규 거래일 전수 무결 수집)

---

## 3. 시점 정렬(Trading Hours Alignment) 규칙

금융 시장과 트윗 발생 시점의 시차 문제를 방지하기 위해 다음 규칙을 적용하였습니다:
1. **타임존 변환:** 트윗 작성 시각(UTC)을 미국 동부 시각(`America/New_York`, EST/EDT 서머타임 자동 적용)으로 변환.
2. **거래일 매핑:**
   - **00:00 ~ 16:00 EST (장 개장 전 및 장중):** 당일($T$) 거래일로 매핑 (단, 휴일/주말인 경우 직후 첫 거래일).
   - **16:00 ~ 23:59 EST (장 마감 후):** 익일($T+1$)로 전환 후 직후 첫 거래일로 매핑.
3. **일별 집계 변수:**
   - `Trade_Tweet_Dummy`: 해당 거래일로 매핑된 무역/관세 트윗이 1건 이상이면 1, 없으면 0
   - `Trade_Tweet_Count`: 무역 트윗 총 건수 (총 729건 매핑, 331거래일)
   - `Fed_Tweet_Dummy`: 해당 거래일로 매핑된 연준/금리 트윗이 1건 이상이면 1, 없으면 0
   - `Fed_Tweet_Count`: 연준 트윗 총 건수 (총 175건 매핑, 111거래일)

---

## 4. 실증 검정 결과 요약

`python empirical_analysis.py` 실행 결과:

| 분석 지표 | 무역 트윗 발생일 ($N=331$) | 미발생일 ($N=676$) | 차이 ($\Delta$) | $t$-통계량 ($p$-값) | 통계적 유의성 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **VIX 일별 등락률** | **+1.483%** | **-0.092%** | **+1.575%p** | **2.575 ($p=0.0102$)** | **유의수준 1%에서 유의함!** |
| **VIX 종가 레벨** | **21.03 pt** | **16.89 pt** | **+4.14 pt** | **6.132 ($p=0.0000$)** | **유의수준 0.1%에서 유의함!** |
| **S&P 500 일별 수익률** | **+0.007%** | **+0.088%** | **-0.081%p** | -0.840 ($p=0.4013$) | 방향성은 음(-)이나 일별 노이즈 존재 |
| **달러 인덱스 수익률** | **-0.035%** | **+0.002%** | **-0.036%p** | -1.463 ($p=0.1441$) | 무역 갈등 시 달러 약세 경향 ($p \approx 0.14$) |

---

## 5. 실행 방법

```bash
# 1. 의존 패키지 설치
pip install -r requirements.txt

# 2. 데이터 수집 및 병합 파이프라인 재실행 (필요 시)
python pipeline.py

# 3. 실증 통계 검정 실행
python empirical_analysis.py
```
