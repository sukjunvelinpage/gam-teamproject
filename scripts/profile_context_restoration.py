"""문맥 복원 대상의 형태와 추적 상태를 원본을 보존하며 정리한다."""
from pathlib import Path
import hashlib
import json
import re
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'docs/tweet_audit_2026-11-02/restoration'
SOURCE = BASE / 'docs/tweet_audit_2026-11-02/remaining_context_required.csv'


def main():
    np.random.seed(42)
    OUT.mkdir(parents=True, exist_ok=True)
    d = pd.read_csv(SOURCE, dtype={'id': str}).fillna({'text': ''})
    assert len(d) == 3627 and d.raw_row.is_unique
    text = d.text.astype(str)
    no_url = text.str.replace(r'https?://\S+', '', regex=True).str.strip()
    d['url_count'] = text.str.count(r'https?://\S+')
    d['url_only'] = (d.url_count > 0) & no_url.eq('')
    d['short_with_url'] = (d.url_count > 0) & no_url.str.len().between(1, 35)
    d['retweet'] = text.str.match(r'^\s*RT\s+@', case=False)
    d['ellipsis'] = text.str.contains(r'\.{2,}|…', regex=True)
    d['possible_thread_fragment'] = text.str.contains(r'^\s*(?:\.{2,}|…)|(?:\.{2,}|…)\s*$', regex=True)
    d['assigned_priority'] = np.select(
        [d.ellipsis & ~d.url_only, d.retweet & ~d.url_only, d.short_with_url, d.url_only],
        ['본문단편_우선', '리트윗_확인', '링크와짧은본문', '링크만'],
        default='기타_문맥검토')
    d['restoration_status'] = '미확인'
    d.to_csv(OUT / 'restoration_population.csv', index=False, encoding='utf-8-sig')
    stats = {'rows': len(d), 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
             'priority_exclusive_counts': d.assigned_priority.value_counts().to_dict(),
             'overlapping_flags': {c: int(d[c].sum()) for c in ['url_only','short_with_url','retweet','ellipsis','possible_thread_fragment']},
             'note': '형태 분류는 확인 우선순위이며 복원 또는 정책 관련성 판단이 아니다. 유형 간 중복 플래그와 상호배타 우선순위 수치를 구분한다.'}
    (OUT / 'population_profile.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
