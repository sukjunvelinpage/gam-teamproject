# 파이썬 코드 및 시각화 표준 (Python & Visualization Standards)

## 1. 코드 작성 표준
- **Python 버전:** 3.10+
- **코드 스타일:** PEP 8 준수, Type Hinting 권장
- **Docstring & 주석:**
  - 주요 함수와 클래스는 한국어 독스트링으로 작성 (기능, 입력 매개변수, 반환값 설명).
  - 금융 수식 또는 통계 공식이 적용되는 부분에는 수식의 수학적/경제학적 의미를 주석으로 명시.
- **재현성 (Reproducibility):**
  - 난수 생성이 포함된 경우 반드시 시드 고정 (`random_state=42` 또는 `np.random.seed(42)`).
  - 단독 실행 가능하도록 `if __name__ == '__main__':` 블록 포함.

## 2. 시각화 (Matplotlib) 표준
- **출력 경로:** 차트 생성 코드는 결과를 `presentation_charts/` 디렉터리에 자동 저장.
- **해상도:** 슬라이드 발표용 차트는 최소 `dpi=300` 이상으로 저장 (`plt.savefig(path, dpi=300, bbox_inches='tight')`).
- **한글 폰트 설정:**
  ```python
  import matplotlib.pyplot as plt
  import platform

  if platform.system() == 'Windows':
      plt.rcParams['font.family'] = 'Malgun Gothic'
  elif platform.system() == 'Darwin':
      plt.rcParams['font.family'] = 'AppleGothic'
  else:
      plt.rcParams['font.family'] = 'NanumGothic'
  plt.rcParams['axes.unicode_minus'] = False
  ```
- **스타일 가이드:**
  - 발표 슬라이드에 적합하게 폰트 크기(`fontsize=11` 이상), 선 굵기(`linewidth=2`), 수치 레이블(Data Labels)을 명확하게 적용.
  - 색상 팔레트: 하락/부정(빨간색/주황색 계열), 상승/긍정(초록/파란색 계열), 중립/벤치마크(회색/남색).

## 3. 의존성 관리
- 새로운 라이브러리가 필요할 경우 `requirements.txt`에 버전 명시 후 추가.
- 불필요한 무거운 패키지(예: 대규모 딥러닝 프레임워크) 도입을 지양하고 가벼운 표준 통계/분석 라이브러리(`pandas`, `numpy`, `scipy`, `yfinance`, `matplotlib`) 중심 유지.
