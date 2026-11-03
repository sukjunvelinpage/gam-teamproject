"""참조본문 141건을 읽고 작성한 개별 판정 목록을 검증·내보낸다."""
from pathlib import Path
import pandas as pd

p = Path(__file__).parent
d = pd.read_csv(p/'archive_independent_text_candidates.csv', dtype=str).fillna('')
# 판단 단위는 전재문 본문이며 괄호 밖 연결물에 의존하는 사실은 추론하지 않는다.
groups = [
('경제정책 관련 후보','positive','CARES 경기부양법에 서명했다는 긍정적 정책 발표', '3569'),
('경제정책 관련 후보','positive','USMCA 통과를 지지하는 무역협정 관련 발언', '20849 22780'),
('경제정책 관련 후보','negative','불공정한 중국 무역 관행을 비판하고 도전을 지지함; 대중 무역갈등 방향', '5649'),
('경제정책 관련 후보','negative','TVA의 미국 노동자 해고와 그에 대한 정부 압박을 언급; 기업 고용 관련 부정적 개입', '4151'),
('경제정책 관련 후보','uncertain','Section 230 폐지 누락을 비판하는 NDAA 거부권 관련 발언; 법안 전체의 경제적 방향은 불명', '1244 2541'),
('경제정책 관련 후보','uncertain','방역 검사비 본인부담 면제와 치료 보장에 관한 보험사 합의를 직접 언급', '4499'),
('경제정책 관련 후보','uncertain','정부계약 배제를 제안하나 대상 기업과 구체 기술은 연결 글 확인 필요', '4198'),
('경제정책 관련 후보','uncertain','FDA의 특정 약물 사용 승인 및 공급을 언급하나 본문은 다른 게시자의 평가임', '4736'),
('경제정책 관련 후보','uncertain','경기 및 노동자 지원을 직접 논의하나 정책 내용·시점·규모가 특정되지 않음', '8096 8134 11927'),
('경제정책 관련 후보','uncertain','미국 이민 일시 중단 행정명령 예고; 노동시장 관련이지만 시장효과의 부호는 불명', '10785'),
('경제정책 관련 후보','uncertain','에너지 정책에 대한 선거 비판이나 구체적 정책 내용은 연결물에 있음', '11473'),
('경제정책 관련 후보','uncertain','상대 후보의 증세 등 경제정책을 비판하나 선거 주장이고 제도 변경이 아님', '12469'),
('경제정책 관련 후보','uncertain','농민의 공정한 경쟁 조건을 언급하나 앞 문장이 누락된 연속 트윗', '17553'),
('경제정책 관련 후보','uncertain','세금 인하와 증세를 선거 지지 맥락에서 언급; 구체 입법 발표는 아님', '20326'),
('경제정책 관련 후보','uncertain','덤핑과 대외무역의 불공정성을 비판하나 구체 대상과 조치는 본문에서 특정되지 않음', '24510'),
('문맥 추가 필요','uncertain','연결된 뉴욕포스트 기사 내용은 본문에서 확인되지 않으며 세금 신고 언급은 보도의 비교 맥락임', '8199'),
('문맥 추가 필요','uncertain','기존 질환 보장 관련 법안 HR 986을 비판하나 법안 내용·경제정책 분류 기준은 추가 확인 필요', '24565'),
('문맥 추가 필요','uncertain','연결된 자료나 앞뒤 게시물이 없으면 정책 대상 또는 실제 주장을 특정할 수 없음', '933 1362 1903 2819 3646 4319 4359 4703 4845 5097 5924 6980 7460 8056 8340 8764 8911 9089 9141 10070 10822 10994 12964 15838 16905 19786 22434 22580 22706 23335 23708 24475 25949 25973 25982 26210'),
('범위 밖 잠정','neutral','복원된 본문은 정치적 지지·선거·일반적 성과 주장 또는 행사 언급이며 구체 경제정책 조치는 명시하지 않음', '209 389 2085 2411 2804 2815 3729 3789 4071 4132 4365 4699 5044 5059 8149 8520 9008 9012 9046 9154 9264 12411 13800 15496 19100 19755 19893 20062 20261 20420 21482 21845 21961 22008 22009 22010 22437 22749 22788 23560 23707 23909 25669'),
('범위 밖 잠정','neutral','방역·의료 또는 우주·안보 등 내용은 있으나 본문에 경제정책이나 구체 경제조치가 드러나지 않음', '361 907 943 1047 2308 2538 2545 2812 2886 3614 4076 4443 4502 4503 5037 5358 5421 6465 6511 6703 6998 7258 7675 7776 8180 8362 9164 9220 9775 10874 10941 11075 11233 11645 12108 12161 21089 21115 25975 25976 26110'),
]
lookup = {}
for status, direction, reason, ids in groups:
    for ident in ids.split():
        assert ident not in lookup, f'duplicate manual judgment {ident}'
        lookup[ident] = (status, direction, reason)
ids = set(d.raw_row)
assert len(d)==141 and len(ids)==141 and ids==set(lookup), (ids-set(lookup), set(lookup)-ids)
rows=[]
for row in d.to_dict('records'):
    status, direction, reason = lookup[row['raw_row']]
    # 범위 밖 판정은 감성 중립이라는 뜻이 아니므로 분석용 중립값을 생성하지 않는다.
    if status == '범위 밖 잠정':
        direction = 'not_applicable'
    text=row['reference_text']
    haslink=('https://' in text or 'pic.twitter.com/' in text)
    partial=row['completion_status']=='partial_extension_review_required' or text.startswith('...') or '(3/3)' in text or '(3/4)' in text
    # 정책 관련성 판단과 본문 완결성은 분리: 링크는 원문 외 내용 미확인.
    completeness = '불완전_전후본문필요' if partial else ('본문확장_연결매체미확인' if haslink else '본문확장_완전성미검증')
    row.update(policy_relevance=status, proposed_direction=direction, reasoning_ko=reason,
               restoration_completeness=completeness, external_content_reviewed='아니오',
               time_note='ID 유래 시각은 트럼프 계정의 해당 트윗·RT 시각이며 RT 원작성 시각이 아님',
               review_note='참조본문 개별 열람; 시장 수익률 미사용; RT 원작성자와 트럼프를 구분; 참조본 정확성과 완결성은 추가 검증 필요; 방향은 잠정')
    rows.append(row)
out=pd.DataFrame(rows)
out.to_csv(p/'archive_independent_review.csv',index=False,encoding='utf-8-sig')
earlier=pd.read_csv(p/'archive_reviewed_cases.csv', dtype=str)
print('rows',len(out),'unique',out.raw_row.nunique(),'overlap',sorted(set(out.raw_row)&set(earlier.raw_row)))
print('policy',out.policy_relevance.value_counts().to_dict())
print('direction',out.proposed_direction.value_counts().to_dict())
print('completeness',out.restoration_completeness.value_counts().to_dict())
