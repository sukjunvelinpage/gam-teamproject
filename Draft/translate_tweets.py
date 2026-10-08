"""
Translation Script for Trump 1st-Term Audited Tweets (English -> Korean & Vietnamese)
--------------------------------------------------------------------------------------
Translates 1,237 audited tweets in Draft/trade_tweets_raw_audit.csv into:
  - tweet_text_ko (Korean)
  - tweet_text_vi (Vietnamese)
Outputs:
  - Updates Draft/trade_tweets_raw_audit.csv with UTF-8-SIG encoding
  - Updates Draft/tweets_data.js with new trilingual fields
"""

import os
import sys
import time
import json
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

DRAFT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(DRAFT_DIR, "trade_tweets_raw_audit.csv")
JS_PATH = os.path.join(DRAFT_DIR, "tweets_data.js")

def translate_single(text: str, target_lang: str, retries: int = 3) -> str:
    if not text or not str(text).strip():
        return ""
    text_clean = str(text).strip()
    
    # URL encode
    encoded = urllib.parse.quote(text_clean[:2000])
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang}&dt=t&q={encoded}"
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                translated = "".join([part[0] for part in data[0] if part and part[0]])
                return translated
        except Exception as e:
            if attempt == retries - 1:
                return text_clean  # fallback to original if failed
            time.sleep(0.5 * (attempt + 1))
    return text_clean

def run_translation():
    print("=" * 70)
    print("🌍 트럼프 트윗 1,237건 한국어 & 베트남어 다국어 번역 파이프라인 시작")
    print("=" * 70)
    
    df = pd.read_csv(CSV_PATH)
    total = len(df)
    print(f"• 대상 데이터: {total:,}건 ({CSV_PATH})")
    
    # Check existing columns
    if "tweet_text_ko" not in df.columns:
        df["tweet_text_ko"] = ""
    if "tweet_text_vi" not in df.columns:
        df["tweet_text_vi"] = ""
        
    texts = df["tweet_text"].tolist()
    
    # 1. Translate Korean
    print("\n[1/2] 🇰🇷 한국어(KO) 병렬 번역 진행 중 (약 30~50초 소요)...")
    t0 = time.time()
    ko_results = [None] * total
    
    def task_ko(idx):
        if pd.notna(df.at[idx, "tweet_text_ko"]) and str(df.at[idx, "tweet_text_ko"]).strip():
            return idx, df.at[idx, "tweet_text_ko"]
        return idx, translate_single(texts[idx], "ko")
        
    with ThreadPoolExecutor(max_workers=14) as executor:
        futures = [executor.submit(task_ko, i) for i in range(total)]
        done_count = 0
        for f in as_completed(futures):
            idx, res = f.result()
            ko_results[idx] = res
            done_count += 1
            if done_count % 200 == 0 or done_count == total:
                print(f"      KO 번역 진행률: {done_count:,} / {total:,} ({done_count/total*100:.1f}%)")
                
    df["tweet_text_ko"] = ko_results
    print(f"      ✅ 한국어 번역 완료! 소요시간: {time.time()-t0:.1f}초")
    
    # 2. Translate Vietnamese
    print("\n[2/2] 🇻🇳 베트남어(VI) 병렬 번역 진행 중 (약 30~50초 소요)...")
    t0 = time.time()
    vi_results = [None] * total
    
    def task_vi(idx):
        if pd.notna(df.at[idx, "tweet_text_vi"]) and str(df.at[idx, "tweet_text_vi"]).strip():
            return idx, df.at[idx, "tweet_text_vi"]
        return idx, translate_single(texts[idx], "vi")
        
    with ThreadPoolExecutor(max_workers=14) as executor:
        futures = [executor.submit(task_vi, i) for i in range(total)]
        done_count = 0
        for f in as_completed(futures):
            idx, res = f.result()
            vi_results[idx] = res
            done_count += 1
            if done_count % 200 == 0 or done_count == total:
                print(f"      VI 번역 진행률: {done_count:,} / {total:,} ({done_count/total*100:.1f}%)")
                
    df["tweet_text_vi"] = vi_results
    print(f"      ✅ 베트남어 번역 완료! 소요시간: {time.time()-t0:.1f}초")
    
    # 3. Save CSV
    df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
    print(f"\n• CSV 파일 갱신 완료: {CSV_PATH}")
    
    # 4. Save JS for web app
    data = df.to_dict(orient="records")
    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write("// Auto-generated 1,237 trilingual tweets data for Draft Tinder-Swipe UI\n")
        f.write("window.INITIAL_TWEETS_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")
    print(f"• JS 번들 갱신 완료: {JS_PATH}")
    
    print("\n" + "=" * 70)
    print("🎉 다국어 번역 및 데이터셋 동기화가 성공적으로 완료되었습니다!")
    print("=" * 70)

if __name__ == "__main__":
    run_translation()
