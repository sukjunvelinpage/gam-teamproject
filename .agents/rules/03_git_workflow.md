# Git 및 협업 컨벤션 가이드 (Git & Collaboration Workflow)

## 1. 브랜치 전략 (Git Flow Lightweight)
- `main`: 최종 배포 및 발표용 안정 브랜치. 직접 커밋/푸시를 지양하고 Pull Request(PR)를 통한 병합 권장.
- 기능별 브랜치 규칙:
  - `feature/<name>`: 새 분석 모델, 지표 수집 등 기능 추가
  - `analysis/<name>`: 통계 검정 및 가설 검증 작업
  - `viz/<name>`: 차트 디자인 및 시각화 코드 개발
  - `docs/<name>`: README, 발표 대본, 보고서 문서 수정
  - `fix/<name>`: 버그 수정 및 데이터 정제 오류 개선

## 2. 커밋 메시지 컨벤션 (Conventional Commits)
커밋 메시지는 한눈에 변경 사항을 파악할 수 있도록 아래 프리픽스를 사용합니다:
- `feat: `: 새로운 기능/분석 스크립트 추가
- `fix: `: 버그 수정, 수식 오차 정정, 결측치 로직 수정
- `data: `: 데이터 수집/정제, 신규 지표/변수 추가
- `viz: `: 차트 생성 스크립트 수정 및 이미지 업데이트
- `docs: `: README, 발표 대본, 주석 등 문서 작성/수정
- `refactor: `: 기능 변경 없는 코드 구조 개선
- `chore: `: 설정 파일 변경, requirements.txt 수정 등

*예시:*
```bash
git commit -m "feat: 중국 위안화 환율 변동성 Welch t-test 추가"
git commit -m "viz: VIX vs S&P500 2일 CAR 비교 차트 디자인 개선"
git commit -m "docs: 발표 대본 슬라이드 8번 질의응답 보강"
```

## 3. 충돌(Conflict) 방지 및 대용량 파일 관리
1. **작업 시작 전 동기화:**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/<내작업>
   ```
2. **대용량 파일 관리:**
   - 100MB 이상의 대용량 파일은 GitHub에 커밋하지 않습니다.
   - 로컬 캐시, 임시 파일, 엑셀 잠금 파일(`~$*.xlsx`) 등은 반드시 `.gitignore`에 유지합니다.
3. **PR 전 자체 점검:**
   - 파이썬 스크립트가 로컬에서 정상 실행되는지 확인 (`python <파일명>.py`)
   - 다른 팀원의 분석 결과 요약 파일(`extended_empirical_summary.csv` 등)과 충돌이 없는지 확인
