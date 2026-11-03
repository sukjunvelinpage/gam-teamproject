from pathlib import Path
import pandas as pd

root=Path(__file__).resolve().parents[2]
d=pd.read_csv(root/'docs/tweet_audit_2026-11-02/remaining_individual_review_ledger.csv',dtype=str,keep_default_na=False)
batch=d[d.status.eq('include_extended')].iloc[2600:2900].copy()
hold=set(('16093 16117 16118 16132 16133 16143 16147 16150 16168 16172 16269 16294 16305 16363 16403 '
          '16455 16474 16520 16541 16563 16585 16607 16608 16620 16631 16663 16665 16666 16672 16695 16718 16769 16773 16792 16812 16846 16849 '
          '16851 16900 16909 16911 16936 17022 17039 17116 17117 17170 17263 17264 17265 17293 17295 17310 17311 17312 '
          '17365 17368 17369 17425 17451 17457 17484 17529 17530 17537 17544 17550 17589 17593 17602 17605 17612 17654 17658 17661 17663 17665 17717 17732 17758 17786 '
          '17878 17897 17951 17952 17953 17966 17967 18014 18015 18024 18057 18062 18063 18064 18121 18123 18124 18125 18175 18227 18228 '
          '18319 18410 18420 18421 18427 18428 18429 18431 18432 18434 18439 18440 18455 18461 18466 18467 18478 18480 18496 18500 18501 18514 18556 18557 18558 18560 18561 18569 18570').split())
assert len(batch)==300 and hold <= set(batch.raw_row)
out=[]
for r in batch.itertuples():
    if r.raw_row in hold:
        decision='hold'; reason='연결 자료 또는 잘린 문맥을 확인해야 하므로 무역·관세 핵심 여부를 보류한다.'
    else:
        decision='exclude_core'; reason='저장 본문은 경제 실적·정치·선거·보건·재난 또는 정부 지원 관련이며 신규 무역·관세 조치를 담고 있지 않다. 보조 경제정책 연구는 별도 판단한다.'
    out.append({'raw_row':r.raw_row,'decision':decision,'direction':'uncertain','reason_ko':reason})
pd.DataFrame(out).to_csv(root/'docs/tweet_audit_2026-11-02/conservative_extended_last_round3.csv',encoding='utf-8-sig',index=False)
