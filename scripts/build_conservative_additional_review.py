from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1] / 'docs/tweet_audit_2026-11-02'

def main():
    core = pd.read_csv(BASE / 'additional_core_candidates.csv', dtype=str, keep_default_na=False)
    omissions = pd.read_csv(BASE / 'confirmed_scope_omissions.csv', dtype=str, keep_default_na=False)
    # Manual reading limited to all 59 initial omission cases and 106 additional
    # cases whose existing theme contains Trade/Tariff/USMCA/Sanction.
    subset = core[core.themes.str.contains('Trade|Tariff|USMCA|Sanction', case=False, regex=True)].copy()
    subset['prior_theme'] = subset.themes
    omissions['prior_theme'] = omissions.proposed_themes
    subset['review_population'] = 'additional_core_471_trade_sanction_theme'
    omissions['review_population'] = 'first_screen_59'
    df = pd.concat([subset, omissions], ignore_index=True)
    assert len(df) == 165 and df.raw_row.is_unique
    df['review_status'] = 'hold_not_core'
    df['candidate_subject'] = '무역·관세 직접조치 여부 재확인'
    df['reason_ko'] = '보수적 핵심 편입을 위한 조치의 구체성, 무역 관련성 또는 게시 당시 신규성이 확인되지 않으므로 핵심 편입을 보류한다.'
    df['novelty_verification'] = 'independent_prior_publication_not_verified'
    df['time_verification'] = 'not_verified'
    details = {
      '23057':('hold_concrete_candidate','무역규칙·WTO','WTO의 개도국 우대 문제와 관련해 USTR에 당일 조치를 지시했다고 밝힌다. 실제 조치 내용, 선행 공개 및 정확 시각을 확인해야 한다.'),
      '18565':('hold_already_announced','한미 FTA','USTR이 이미 원칙적 합의를 발표했다고 글이 밝힌다. 트윗 자체를 최초 공개로 취급할 수 없다.'),
      '16994':('hold_link_only','미국·멕시코 무역협정','링크·제목만 있어 본문에서 합의의 구체 내용과 이전 공개 여부를 확인할 수 없다.'),
      '16603':('hold_link_only','한미 FTA','공동성명 링크이며 서명과 발표의 선후관계를 확인해야 한다.'),
      '3145':('hold_retweet','미중 1단계 무역합의','백악관 라이브 방송을 재전송하므로 합의 내용과 최초 공개 시각은 별도 확인이 필요하다.'),
      '14137':('hold_vague','북한 관련 무역 제재','무역 중단을 검토한다고만 밝혀 시행이나 구체적 명령은 확인되지 않는다.'),
      '18710':('hold_rhetoric','보호무역 수사','무역전쟁에 대한 일반적 주장으로 구체적인 신규 조치를 명시하지 않는다.'),
      '473':('hold_concrete_sanctions','수단 제재 완화','3.35억 달러 지급을 조건으로 테러지원국 명단 해제를 예고했으나 선행 발표와 실제 조치 시점을 별도 확인한다. 무역 핵심이 아닌 제재 보조 후보.'),
      '25290':('hold_concrete_sanctions','북한 제재','추가 제재 철회를 지시했다고 주장하나 대상 제재의 식별 및 기존 공개 여부를 확인해야 한다. 무역 핵심이 아닌 제재 보조 후보.'),
      '17385':('hold_concrete_sanctions','터키 제재','큰 제재 부과를 예고하나 제재 종류와 세부 조치가 불명확해 보류한다.'),
      '21810':('hold_concrete_sanctions','이란 제재','재무장관에게 제재 강화를 지시했다고 하나 구체 제재와 발표 선후관계를 확인해야 한다.'),
      '23733':('hold_concrete_sanctions','이란 제재','월요일 추가 제재를 예고하나 내용과 발표 선후관계, 후속 스레드 여부를 확인해야 한다.'),
      '17703':('hold_threat','개별 기업·관세 위협','해외 이전 시 과세 위협은 구체 조치나 세율이 없으며 기존 보도 확인이 필요하다.'),
      '7436':('hold_context','미국·캐나다 국경','필수적이지 않은 이동을 중단하되 무역은 영향을 받지 않는다고 명시한다. 국경 정책과 무역정책 핵심 사건을 구분해야 한다.'),
      '3829':('hold_retweet','기술규제','틱톡 행정명령 관련 뉴스의 잘린 재전송이며 최초 발표가 확인되지 않는다.'),
      '60':('hold_truncated_retweet','브렉시트','영국의 EU 시장 이탈 관련 잘린 재전송이며 트럼프의 새로운 정책 발표가 아니다.'),
      '14682':('hold_already_announced','미국·멕시코 설탕 협상','이미 협상된 합의를 평가한다. 트윗 전 합의 발표와 시점 확인 전 새로운 사건으로 볼 수 없다.'),
      '6529':('hold_retrospective','USMCA','이미 2018년에 발표된 협상 결과를 회고하는 백악관 재전송이다.'),
      '21241':('hold_retweet','미일 무역협정','서명 관련 잘린 제3자 재전송이며 트럼프의 최초 공개 또는 새로운 정보로 확정할 수 없다.'),
      '16920':('hold_link_only','캐나다 무역협상','뉴스 링크만 인용하여 협상 결렬의 새로운 공개 및 정확한 기사 시점이 미검증이다.'),
      '18592':('hold_link_only','미국 무역조치','중요한 조치를 했다고만 말하고 구체적 내용은 링크에 의존한다.'),
      '16605':('hold_ceremony','한미 FTA','서명식 공지만으로 구체 합의 내용이나 최초 발표 여부를 확인할 수 없다.'),
      '24181':('hold_vague','미일 무역협상','협상 진전이라는 일반적 서술이며 합의나 조치의 구체 내용이 없다.'),
    }
    for raw,(status,subject,reason) in details.items():
        mask=df.raw_row.eq(raw)
        assert mask.sum()==1, raw
        df.loc[mask,['review_status','candidate_subject','reason_ko']]=[status,subject,reason]
    columns=['raw_row','audit_key','date_utc','text','review_population','prior_theme','review_status','candidate_subject','reason_ko','novelty_verification','time_verification']
    df[columns].to_csv(BASE/'conservative_additional_review.csv',index=False,encoding='utf-8-sig')
    print('reviewed',len(df),'statuses',df.review_status.value_counts().to_dict())

if __name__ == '__main__': main()
