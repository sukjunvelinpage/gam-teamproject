"""실제 원문 열람이 끝난 배치의 명시적 판단만 저장한다."""
import json
from pathlib import Path
import pandas as pd

P=Path(__file__).resolve().parent

def write(start,stop,overrides,unclear):
    source=pd.read_csv(P/'part_0.csv').iloc[start:stop]
    path=P/'part_0_tail_a_decisions.jsonl'
    old=[json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
    assert not set(source.raw_row)&{x['raw_row'] for x in old}
    rows=[]
    for r in source.itertuples():
        status,themes,direction,reason=overrides.get(r.raw_row,('exclude',['Politics_Ceremony_Personal'],'na','선거·정치 공방·지지·행사·개인 논평으로 신규 무역·통화·기업 정책조치가 본문에 제시되지 않음'))
        if r.raw_row in unclear: status,themes,direction,reason='needs_context',['Context_Required'],'uncertain','URL·짧은 반응·주어와 조치가 생략된 단편으로 연결 매체나 이전 원문 없이는 정책 관련성과 부호 확정 불가'
        rows.append(dict(raw_row=int(r.raw_row),status=status,themes=themes,direction=direction,reason_ko=reason+' [본문: '+str(r.text).replace('\n',' ')[:110]+']',reviewer='finish_tail_a',batch_id=f'tail_a_{start}_{stop}'))
    assert len(rows)==stop-start
    with path.open('a',encoding='utf-8') as f:
        for x in rows:f.write(json.dumps(x,ensure_ascii=False)+'\n')
    print('saved',len(rows),'total',len(old)+len(rows))
