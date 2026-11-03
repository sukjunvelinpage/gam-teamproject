"""실제 열람을 마친 배치의 명시적 판단만 저장하는 보조 함수. 자동 의미 분류 아님."""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'docs/tweet_audit_2026-11-02/remaining_review'


def record(part, start, stop, overrides, unclear_ids, reviewer):
    data = pd.read_csv(FOLDER / f'part_{part}.csv')
    batch = data.iloc[start:stop]
    output = FOLDER / f'part_{part}_decisions.jsonl'
    prior = [json.loads(x) for x in output.read_text(encoding='utf-8').splitlines()] if output.exists() else []
    assert not set(batch.raw_row) & {x['raw_row'] for x in prior}
    for row in batch.itertuples():
        status, themes, direction, reason = overrides.get(row.raw_row, ('exclude', ['Political_Personal_Ceremonial'], 'na', '선거·정치 공방, 지지·감사, 이동·행사 또는 개인 논평이다. 본문에 무역·통화·기업·농가 조치가 제시되지 않아 현행 정책 사건에서 제외한다.'))
        if row.raw_row in unclear_ids:
            status, themes, direction, reason = 'needs_context', ['Context_Required'], 'uncertain', '링크·짧은 반응 또는 지시 대상이 생략된 글이다. 연결 원문 없이는 경제정책 관련성과 부호를 확정할 수 없어 보류한다.'
        prior.append({'raw_row': int(row.raw_row), 'status': status, 'themes': themes, 'direction': direction, 'reason_ko': reason, 'reviewer': reviewer, 'batch_id': f'{reviewer}_{start}_{stop}', 'evidence_excerpt': str(row.text)[:110], 'review_method': '본문 도구 출력 개별 열람 후 명시적 배치 판정'})
    output.write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in prior)+'\n',encoding='utf-8')
    print(f'{part}: {len(prior)} reviewed rows saved')


if __name__ == '__main__':
    raise SystemExit('이 파일은 실제 열람 후 명시적 판단을 전달하는 record 함수를 제공한다.')
