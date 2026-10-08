"""
Merge Script for Multi-Member Tweet Audit CSVs
----------------------------------------------
Combines multiple team members' manual audit CSV files into one unified final dataset:
- Reads all 'trade_tweets_*.csv' files in Draft/ directory
- Merges manual_audit_label (O/X) across all chunked ranges
- If overlapping votes exist, calculates agreement rate and consensus (majority vote)
- Outputs: Draft/trade_tweets_final_consensus.csv
"""

import os
import glob
import pandas as pd

DRAFT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_CSV = os.path.join(DRAFT_DIR, "trade_tweets_raw_audit.csv")
OUTPUT_FINAL_CSV = os.path.join(DRAFT_DIR, "trade_tweets_final_consensus.csv")

def merge_member_csvs():
    print("=" * 70)
    print("팀원별 수기 감사(Manual Audit) CSV 파일 자동 병합 시작")
    print("=" * 70)
    
    # 1. Load base template
    if not os.path.exists(BASE_CSV):
        print(f"[Error] 기준 파일이 없습니다: {BASE_CSV}")
        return
    base_df = pd.read_csv(BASE_CSV)
    total_tweets = len(base_df)
    print(f"• 기준 데이터셋 총 건수: {total_tweets:,}건")
    
    # 2. Find all submitted CSV files in Draft/
    all_csvs = glob.glob(os.path.join(DRAFT_DIR, "*.csv"))
    member_files = [
        f for f in all_csvs 
        if os.path.basename(f) not in ["trade_tweets_raw_audit.csv", "trade_tweets_final_consensus.csv"]
    ]
    
    if not member_files:
        print("\n[안내] 병합할 팀원 CSV 파일이 발견되지 않았습니다.")
        print("  팀원들이 내보낸 CSV 파일들을 Draft/ 폴더에 넣고 다시 실행해주세요.")
        print("  (예: Draft/trade_tweets_철수.csv, Draft/trade_tweets_영희.csv 등)")
        return
        
    print(f"\n• 발견된 팀원 파일 ({len(member_files)}개):")
    for f in member_files:
        print(f"  - {os.path.basename(f)}")
        
    # 3. Collect labels from each file
    member_labels = {}
    for f in member_files:
        member_name = os.path.splitext(os.path.basename(f))[0].replace("trade_tweets_", "").replace("manual_audited_", "")
        try:
            m_df = pd.read_csv(f)
            if "manual_audit_label" in m_df.columns:
                labels = m_df["manual_audit_label"].fillna("").astype(str).str.strip().str.upper()
                # filter only valid O / X
                labels = labels.apply(lambda x: x if x in ["O", "X"] else "")
                member_labels[member_name] = labels
                valid_count = (labels != "").sum()
                print(f"    ➔ [{member_name}]: {valid_count:,}건 라벨링 확인됨")
            else:
                print(f"    [Warning] {os.path.basename(f)}에 manual_audit_label 열이 없습니다.")
        except Exception as e:
            print(f"    [Error] {os.path.basename(f)} 읽기 실패: {e}")
            
    if not member_labels:
        print("\n[Error] 유효한 라벨링 데이터가 없습니다.")
        return

    # 4. Merge Logic (Consensus / Majority / Priority fill)
    merged_labels = []
    consensus_stats = []
    
    for i in range(total_tweets):
        votes = []
        for m_name, l_series in member_labels.items():
            if i < len(l_series) and l_series.iloc[i] in ["O", "X"]:
                votes.append(l_series.iloc[i])
                
        if not votes:
            merged_labels.append("")
            consensus_stats.append("Pending")
        elif len(votes) == 1:
            merged_labels.append(votes[0])
            consensus_stats.append("Single_Vote")
        else:
            # Multi-vote (Agreement check)
            o_count = votes.count("O")
            x_count = votes.count("X")
            if o_count > x_count:
                merged_labels.append("O")
                consensus_stats.append(f"Consensus_O ({o_count}/{len(votes)})")
            elif x_count > o_count:
                merged_labels.append("X")
                consensus_stats.append(f"Consensus_X ({x_count}/{len(votes)})")
            else:
                # Tie: conservative policy (Mark as O for closer inspection or tie)
                merged_labels.append("O")
                consensus_stats.append(f"Tie ({o_count}:{x_count})")
                
    base_df["manual_audit_label"] = merged_labels
    base_df["audit_vote_status"] = consensus_stats
    
    # Save final
    base_df.to_csv(OUTPUT_FINAL_CSV, index=False, encoding="utf-8-sig")
    
    # 5. Print Summary
    decided = sum(1 for l in merged_labels if l in ["O", "X"])
    o_tot = merged_labels.count("O")
    x_tot = merged_labels.count("X")
    pending = total_tweets - decided
    
    print("\n" + "=" * 70)
    print("병합 완료 요약 보고서")
    print("=" * 70)
    print(f"• 최종 저장 파일: {OUTPUT_FINAL_CSV}")
    print(f"• 전체 트윗 수  : {total_tweets:,}건")
    print(f"• 총 판별 완료  : {decided:,}건 ({decided/total_tweets*100:.1f}%)")
    print(f"  - ⭕ 시장 임팩트 (O): {o_tot:,}건 ({o_tot/total_tweets*100:.1f}%)")
    print(f"  - ❌ 단순 언급   (X): {x_tot:,}건 ({x_tot/total_tweets*100:.1f}%)")
    print(f"• 미판별 남은 트윗: {pending:,}건 ({pending/total_tweets*100:.1f}%)")
    print("=" * 70)

if __name__ == "__main__":
    merge_member_csvs()
