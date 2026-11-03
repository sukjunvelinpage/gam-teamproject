"""Assemble a traceable restoration ledger without changing source data."""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/tweet_audit_2026-11-02'
OUT = BASE / 'restoration'

def main():
    source = pd.read_csv(BASE / 'remaining_context_required.csv', dtype=str, keep_default_na=False)
    assert len(source) == 3627 and source.raw_row.is_unique
    archive = pd.read_csv(OUT / 'archive_restoration_ledger.csv', dtype=str, keep_default_na=False)
    archive = archive[['raw_row', 'archive_status', 'source_url', 'source_tweet_url', 'archived_full_text']]
    reviewed = pd.read_csv(OUT / 'archive_reviewed_cases.csv', dtype=str, keep_default_na=False)
    reviewed = reviewed[['raw_row', 'proposed_status', 'proposed_direction', 'reason_ko']].rename(columns={'proposed_status':'verified_proposed_status','proposed_direction':'verified_proposed_direction','reason_ko':'verified_reason_ko'})
    independent = pd.read_csv(OUT / 'archive_independent_review.csv', dtype=str, keep_default_na=False)
    independent = independent[['raw_row','reference_text','reference_tweet_url','completion_status','policy_relevance','proposed_direction','reasoning_ko','restoration_completeness','external_content_reviewed']]
    independent = independent.rename(columns={x:'candidate_'+x for x in independent.columns if x != 'raw_row'})
    threads = pd.read_csv(OUT / 'threads_overview.csv', dtype=str, keep_default_na=False)[['raw_row','earlier_candidate_count','later_candidate_count','same_second_uncertain_candidate_count','candidate_count']]
    links = pd.read_csv(OUT / 'links_restoration_evidence.csv', dtype=str, keep_default_na=False)
    link_counts = links.groupby('raw_row').agg(link_count=('original_url','size'), linked_earlier_text_count=('evidence_state', lambda s: (s == 'exact_linked_status_id_local_reference').sum()), media_link_count=('evidence_state', lambda s: (s == 'media_not_recovered').sum())).reset_index()
    ledger = source
    for frame in (archive, reviewed, independent, threads, link_counts):
        assert frame.raw_row.is_unique
        ledger = ledger.merge(frame, on='raw_row', how='left', validate='one_to_one')
    ledger = ledger.fillna('')
    ledger['restoration_status'] = 'unresolved'
    ledger.loc[ledger.candidate_reference_text.ne(''), 'restoration_status'] = 'longer_reference_candidate_reviewed_unverified'
    ledger.loc[ledger.verified_proposed_status.ne(''), 'restoration_status'] = 'archive_expansion_reviewed'
    assert len(ledger) == len(source) and ledger.raw_row.is_unique
    ledger.to_csv(OUT / 'combined_restoration_ledger.csv', index=False, encoding='utf-8-sig')
    summary = {'input_rows': len(ledger), 'exclusive_restoration_status': ledger.restoration_status.value_counts().to_dict(),
               'candidate_relevance': independent.candidate_policy_relevance.value_counts().to_dict(),
               'rows_with_linked_earlier_text': int((pd.to_numeric(ledger.linked_earlier_text_count, errors='coerce').fillna(0)>0).sum()),
               'rows_with_thread_candidates': int((pd.to_numeric(ledger.candidate_count, errors='coerce').fillna(0)>0).sum()),
               'source_sha256': hashlib.sha256((BASE / 'remaining_context_required.csv').read_bytes()).hexdigest(),
               'caveat': '상태는 배타적이지만 링크·스레드 수는 서로 겹침. 후보와 링크는 본문이 확인된 사건으로 확정하지 않음.'}
    (OUT / 'restoration_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
