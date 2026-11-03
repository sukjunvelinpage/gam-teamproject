import json
from pathlib import Path
import pandas as pd

p = Path(__file__).resolve().parent
path = p / 'part_0_tail_a_decisions.jsonl'
rows = [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
fixes = {
    1415: ('exclude', ['Political_Censorship'], 'na', '정부와 제3자 정보검열을 비판하는 정치적 논평으로 대상 기업이나 구체 경제규제 조치 없음'),
    1549: ('exclude', ['Political_Company_Criticism'], 'na', '트위터의 본인 관련 트렌드를 비판하는 정치적 재전송이며 규제·제재 요구가 본문에 없음'),
    3190: ('include_core', ['Drug_Price_Regulation'], 'mixed', '제약사 반대광고를 약가인하의 신호로 해석하며 업계를 압박하나 이 글만으로 새 명령의 시점은 확정할 수 없음'),
}
source = pd.read_csv(p / 'part_0.csv').set_index('raw_row')
for row in rows:
    if row['raw_row'] in fixes:
        status, themes, direction, reason = fixes[row['raw_row']]
        row.update(status=status, themes=themes, direction=direction, reason_ko=reason + ' [본문: ' + str(source.loc[row['raw_row'], 'text']).replace('\n', ' ')[:110] + ']')
path.write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows), encoding='utf-8')
ids = [1338,1367,1415,1549,1563,1767,1851,1999,2090,2204,2242,2518,2570,2638,2648,2725,2726,2987,3016,3069,3133,3168,3190,3288,3465,3492,3495,3558,3611,3700,3710,3721,3744,3812,3813]
byid = {x['raw_row']: x for x in rows}
text = ['# part_0 tail_a 원문 개별검토 사례', '', '검토 범위: part_0.csv iloc[1250:3700], 2,450개 고유 raw_row. 기존 400행과 후속 2,050행의 행별 판정 포함. CSV에 저장된 본문을 개별 열람했으며, RT 자체의 말줄임·URL 연결 내용은 복원하지 않았다. needs_context는 무관 판정이 아니다.', '', 'direction은 본문이 서술하는 정책·경제 방향의 보조 표지이며 사후 주가 수익률이나 객관적 사실 검증 결과가 아니다. mixed는 소비자·업계 또는 결합 정책의 방향이 다르다는 뜻이다. 광의 보건·재정·에너지 글은 extended로 분리했다. 선거 지지문 속 세금·일자리 단어만으로 core에 편입하지 않았다.', '', '## 주요 및 애매 사례', '']
for i in ids:
    if i not in byid:
        continue
    r = byid[i]
    text += [f"### R{i} — {r['status']} / {r['direction']}", '', '> ' + str(source.loc[i, 'text']).replace('\n', '\n> '), '', r['reason_ko'].split(' [본문:')[0], '']
text += ['## 경계 판단', '', '- R1415의 일반적 검열 비판과 R1549의 트위터 트렌드 불만은 구체 규제요구가 없어 제외했다. R1338은 Section 230을 직접 연결하고 R1563은 의회 규제 논의를 명시하여 별도로 보존했다.', '- R3465는 FDA의 신속처리 요구만 있고 승인 대상이 본문에 없어 문맥보류했다. R3492는 Battelle와 마스크 살균장비를 명시하므로 개별 기업 승인압박으로 편입했다. 인접 글을 소급해 R3465의 대상을 확정하지 않았다.', '- R2242는 Babylon Bee의 IV 식사 의무화 풍자이므로 실제 캘리포니아 보건정책으로 편입하지 않았다.', '- R2725 등 JOBS 문구와 URL만 있는 글은 고용정책이나 긍정방향을 자동 확정하지 않았다.', '- R1999와 R3812는 각각 최혜국 약가명령 유지와 새 서명이라는 다른 정보다. R3813의 리베이트 폐지는 글 자체에 조치가 명시되어 있으며 후속 시장반응을 사용하지 않았다.', '- R3288 격리 검토는 당시의 미결정 상태로 판정했다. 이후의 격리 불필요 선언이나 여행권고를 거꾸로 적용하지 않았다.', '']
(p / 'part_0_tail_a_cases.md').write_text('\n'.join(text), encoding='utf-8')
expected = set(pd.read_csv(p/'part_0.csv').iloc[1250:3700].raw_row)
assert len(rows) == len({x['raw_row'] for x in rows}) == 2450
assert {x['raw_row'] for x in rows} == expected
assert all(set(['raw_row','status','themes','direction','reason_ko','reviewer','batch_id']) <= set(x) for x in rows)
from collections import Counter
print(Counter(x['status'] for x in rows))
print('exact coverage PASS; cases', sum(i in byid for i in ids))
