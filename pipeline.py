"""
Trump 1st Term (2017-01-20 ~ 2021-01-20) Twitter & Financial Market Data Pipeline
---------------------------------------------------------------------------------
Objective:
Collect Donald Trump's tweets and key financial indicators (S&P 500, Dollar Index, VIX),
perform trading hours alignment (UTC -> US/Eastern -> Trading Day mapping),
aggregate daily tweet signals, and merge them into a research-ready dataset.
"""

import os
import re
import requests
import pandas as pd
import numpy as np
import yfinance as yf

# -----------------------------------------------------------------------------
# Configuration & Constants
# -----------------------------------------------------------------------------
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(DATA_DIR, "trump_market_event_data.csv")

# Date range for Trump's first presidential term
START_DATE = "2017-01-20"
END_DATE = "2021-01-20"

# Public Trump Twitter Archive (complete archive up to account suspension in Jan 2021)
TWEET_ARCHIVE_URL = (
    "https://raw.githubusercontent.com/ttzztztz/TrumpTwitterArchive/master/trump.json"
)

# Financial tickers:
# ^GSPC: S&P 500 Index
# DX-Y.NYB: US Dollar Index (ICE / NYBOT)
# UUP: Invesco DB US Dollar Index Bullish Fund (ETF alternative)
# ^VIX: CBOE Volatility Index
TICKERS = {
    "SP500": "^GSPC",
    "DXY": "DX-Y.NYB",
    "UUP": "UUP",
    "VIX": "^VIX",
}

# -----------------------------------------------------------------------------
# 1. Trump Twitter Data Collection & Filtering
# -----------------------------------------------------------------------------
def load_trump_tweets(url: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Downloads the Trump Twitter Archive JSON and extracts tweets during the 1st term.
    
    Fields extracted:
      - date: UTC timestamp
      - text: Tweet body
      - retweets: Retweet count
      - favorites: Favorite (like) count
      - isRetweet: Whether it is an RT
    """
    print(f"[1/4] Loading Trump Twitter Archive from {url} ...")
    raw_df = pd.read_json(url)
    print(f"      Total raw tweets loaded: {len(raw_df):,}")

    # Ensure UTC timezone
    raw_df["date_utc"] = pd.to_datetime(raw_df["date"], utc=True)

    # Filter by 1st term range (2017-01-20 ~ 2021-01-20)
    # Trump was inaugurated at noon EST on 2017-01-20 (~17:00 UTC).
    # We include all tweets from 2017-01-20 00:00:00 UTC through 2021-01-20 23:59:59 UTC.
    mask = (raw_df["date_utc"] >= f"{start_date} 00:00:00+00:00") & (
        raw_df["date_utc"] <= f"{end_date} 23:59:59+00:00"
    )
    tweets = raw_df.loc[mask].copy()
    print(f"      1st term tweets count: {len(tweets):,}")

    # Standardize field names
    tweets = tweets.rename(
        columns={
            "text": "tweet_text",
            "retweets": "retweet_count",
            "favorites": "favorite_count",
        }
    )

    # Fill NaNs in numerical metrics
    tweets["retweet_count"] = tweets["retweet_count"].fillna(0).astype(int)
    tweets["favorite_count"] = tweets["favorite_count"].fillna(0).astype(int)
    tweets["tweet_text"] = tweets["tweet_text"].fillna("").astype(str)

    return tweets


def apply_keyword_filters(tweets: pd.DataFrame) -> pd.DataFrame:
    """
    Applies keyword filters for Trade/Tariffs and Fed/Monetary Policy.
    Uses regex word boundaries to prevent false positives (e.g., 'fed' in 'confederate').
    """
    print("[1b/4] Applying keyword filters ...")

    # Trade / Tariff keywords
    trade_keywords = ["tariff", "tariffs", "trade war", "china", "beijing", "xi jinping"]
    # Build regex: case-insensitive word/phrase match
    trade_pattern = r"(?i)\b(" + "|".join([re.escape(k) for k in trade_keywords]) + r")\b"
    tweets["is_trade_tweet"] = tweets["tweet_text"].str.contains(trade_pattern, regex=True).astype(int)

    # Fed / Monetary Policy keywords
    # Special care: 'fed' must be matched as a standalone word (e.g. \bfed\b or \bfed's\b)
    # to avoid false positives like 'federalist', 'confederate', 'unaffected', 'offered'.
    fed_keywords = [
        r"\bfed\b",
        r"\bfed's\b",
        r"federal reserve",
        r"powell",
        r"interest rate[s]?",
        r"rate cut[s]?",
        r"quantitative",
    ]
    fed_pattern = r"(?i)(" + "|".join(fed_keywords) + r")"
    tweets["is_fed_tweet"] = tweets["tweet_text"].str.contains(fed_pattern, regex=True).astype(int)

    trade_count = tweets["is_trade_tweet"].sum()
    fed_count = tweets["is_fed_tweet"].sum()
    print(f"      Identified Trade-related tweets: {trade_count:,}")
    print(f"      Identified Fed-related tweets:   {fed_count:,}")

    return tweets


# -----------------------------------------------------------------------------
# 2. Financial Market Data Collection
# -----------------------------------------------------------------------------
def load_financial_data(tickers: dict, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Downloads daily OHLC data from Yahoo Finance and calculates daily returns.
    Downloads with a small lookback buffer to compute the return for the first target day.
    """
    print(f"[2/4] Downloading financial market indicators via yfinance ...")
    # Buffer lookback by 10 calendar days so that 2017-01-20 has a valid previous close
    fetch_start = (pd.to_datetime(start_date) - pd.Timedelta(days=15)).strftime("%Y-%m-%d")
    fetch_end = (pd.to_datetime(end_date) + pd.Timedelta(days=5)).strftime("%Y-%m-%d")

    ticker_list = list(tickers.values())
    raw_data = yf.download(ticker_list, start=fetch_start, end=fetch_end, group_by="ticker", auto_adjust=False)

    records = []
    # Invert dictionary for clean column naming
    inv_map = {v: k for k, v in tickers.items()}

    combined_fin = pd.DataFrame()

    for ticker_symbol, alias in inv_map.items():
        if ticker_symbol not in raw_data.columns.levels[0]:
            print(f"      [Warning] Ticker {ticker_symbol} missing from download.")
            continue

        df_t = raw_data[ticker_symbol].copy()
        df_t = df_t[["Open", "High", "Low", "Close"]].dropna(how="all")

        # Daily Return: (Close_t - Close_{t-1}) / Close_{t-1}
        df_t["Daily_Return"] = df_t["Close"].pct_change()

        # Prefix columns with alias (e.g., SP500_Close, SP500_Return)
        df_t = df_t.rename(
            columns={
                "Open": f"{alias}_Open",
                "High": f"{alias}_High",
                "Low": f"{alias}_Low",
                "Close": f"{alias}_Close",
                "Daily_Return": f"{alias}_Return",
            }
        )

        if combined_fin.empty:
            combined_fin = df_t
        else:
            combined_fin = combined_fin.join(df_t, how="outer")

    # Slice to strictly 2017-01-20 to 2021-01-20
    combined_fin.index = pd.to_datetime(combined_fin.index)
    fin_df = combined_fin.loc[start_date:end_date].copy()
    print(f"      Total trading days in target window: {len(fin_df)}")
    print(f"      First day: {fin_df.index.min().strftime('%Y-%m-%d')}, Last day: {fin_df.index.max().strftime('%Y-%m-%d')}")

    return fin_df


# -----------------------------------------------------------------------------
# 3. Trading Hours Alignment & Day Mapping
# -----------------------------------------------------------------------------
def align_tweets_to_trading_days(tweets: pd.DataFrame, trading_calendar: pd.DatetimeIndex) -> pd.DataFrame:
    """
    Rules for trading hours alignment:
      1. Timezone conversion: UTC -> US Eastern Time (US/Eastern handles EST and EDT).
      2. Regular US Market hours: 09:30 ~ 16:00 US/Eastern.
      3. Before market or during market hours (00:00 ~ 16:00 Eastern):
         - Maps to today (T) if today is a trading day.
         - If today is weekend or market holiday, maps to the immediate next trading day.
      4. After market close (16:00 ~ 23:59 Eastern) or weekend/holiday:
         - Maps to the immediate next trading day (T+1).

    Implementation logic:
      - If time < 16:00: Target search date = Tweet Eastern Date (T)
      - If time >= 16:00: Target search date = Tweet Eastern Date + 1 Day (T+1)
      - Mapped Trading Day = Smallest valid trading_day >= Target search date.
    """
    print("[3/4] Aligning tweet timestamps to US Eastern Time and Trading Calendar ...")

    # Step 1: Convert UTC to America/New_York (automatically accounts for EST/EDT transitions)
    tweets["date_eastern"] = tweets["date_utc"].dt.tz_convert("America/New_York")

    # Extract time components in Eastern Time
    eastern_dates = tweets["date_eastern"].dt.normalize().dt.tz_localize(None)
    time_minutes = tweets["date_eastern"].dt.hour * 60 + tweets["date_eastern"].dt.minute

    # Indicator: True if post-market (>= 16:00 Eastern)
    is_post_market = time_minutes >= (16 * 60)

    # Effective target date: add 1 calendar day if post-market
    target_dates = eastern_dates + pd.to_timedelta(np.where(is_post_market, 1, 0), unit="D")

    # Step 2: Map to trading calendar
    # Ensure calendar is sorted normalized timestamps
    clean_trading_days = pd.Series(trading_calendar.tz_localize(None).normalize()).sort_values().values

    # Find the earliest trading day that is >= target_date using searchsorted
    idx = np.searchsorted(clean_trading_days, target_dates.values)

    # If any tweet falls after the last trading day, clip or mark
    valid_mask = idx < len(clean_trading_days)
    mapped_days = np.full(len(tweets), np.nan, dtype="datetime64[ns]")
    mapped_days[valid_mask] = clean_trading_days[idx[valid_mask]]

    tweets["mapped_trading_date"] = pd.to_datetime(mapped_days)

    print(f"      Successfully mapped {valid_mask.sum():,} tweets to trading dates.")
    return tweets


# -----------------------------------------------------------------------------
# 4. Daily Aggregation & Merging
# -----------------------------------------------------------------------------
def aggregate_and_merge(tweets: pd.DataFrame, fin_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates tweet metrics by mapped trading day and left-joins with the financial calendar.
    
    Variables created:
      - Trade_Tweet_Dummy: 1 if >= 1 trade tweet mapped to trading day, else 0
      - Trade_Tweet_Count: Total trade tweets mapped
      - Fed_Tweet_Dummy: 1 if >= 1 Fed tweet mapped to trading day, else 0
      - Fed_Tweet_Count: Total Fed tweets mapped
      - Total_Tweet_Count: Total Trump tweets mapped to trading day
      - Trade_Retweet_Sum, Trade_Favorite_Sum: Total engagement metrics for trade tweets
      - Fed_Retweet_Sum, Fed_Favorite_Sum: Total engagement metrics for Fed tweets
    """
    print("[4/4] Aggregating tweet metrics and merging with financial time series ...")

    # Filter tweets that successfully mapped to a trading day
    mapped_tweets = tweets.dropna(subset=["mapped_trading_date"]).copy()

    # Daily aggregation
    daily_agg = mapped_tweets.groupby("mapped_trading_date").agg(
        Total_Tweet_Count=("tweet_text", "count"),
        Trade_Tweet_Count=("is_trade_tweet", "sum"),
        Fed_Tweet_Count=("is_fed_tweet", "sum"),
        Trade_Retweet_Sum=("retweet_count", lambda s: s[mapped_tweets.loc[s.index, "is_trade_tweet"] == 1].sum()),
        Trade_Favorite_Sum=("favorite_count", lambda s: s[mapped_tweets.loc[s.index, "is_trade_tweet"] == 1].sum()),
        Fed_Retweet_Sum=("retweet_count", lambda s: s[mapped_tweets.loc[s.index, "is_fed_tweet"] == 1].sum()),
        Fed_Favorite_Sum=("favorite_count", lambda s: s[mapped_tweets.loc[s.index, "is_fed_tweet"] == 1].sum()),
    )

    # Generate Dummy variables
    daily_agg["Trade_Tweet_Dummy"] = (daily_agg["Trade_Tweet_Count"] > 0).astype(int)
    daily_agg["Fed_Tweet_Dummy"] = (daily_agg["Fed_Tweet_Count"] > 0).astype(int)

    # Align financial index to normalized datetime
    fin_df_clean = fin_df.copy()
    fin_df_clean.index = fin_df_clean.index.tz_localize(None).normalize()
    fin_df_clean.index.name = "Trading_Date"

    # Left Join: The base spine is the US Regular Trading Day Calendar
    merged_df = fin_df_clean.join(daily_agg, how="left")

    # Handling Missing Values for Tweet variables:
    # On trading days where Trump did not tweet, fill count/dummy with 0
    tweet_columns = [
        "Total_Tweet_Count",
        "Trade_Tweet_Count",
        "Trade_Tweet_Dummy",
        "Fed_Tweet_Count",
        "Fed_Tweet_Dummy",
        "Trade_Retweet_Sum",
        "Trade_Favorite_Sum",
        "Fed_Retweet_Sum",
        "Fed_Favorite_Sum",
    ]
    for col in tweet_columns:
        if col in merged_df.columns:
            merged_df[col] = merged_df[col].fillna(0).astype(int)

    # Reset index so 'Date' is a column
    merged_df = merged_df.reset_index().rename(columns={"Trading_Date": "Date"})
    merged_df["Date"] = merged_df["Date"].dt.strftime("%Y-%m-%d")

    return merged_df


# -----------------------------------------------------------------------------
# Main Execution Pipeline
# -----------------------------------------------------------------------------
def run_pipeline():
    print("=" * 70)
    print("Trump 1st Term Twitter & Financial Market Data Pipeline Starting")
    print("=" * 70)

    # 1. Load tweets and filter keywords
    tweets = load_trump_tweets(TWEET_ARCHIVE_URL, START_DATE, END_DATE)
    tweets = apply_keyword_filters(tweets)

    # 2. Load financial data
    fin_df = load_financial_data(TICKERS, START_DATE, END_DATE)

    # 3. Timezone conversion and trading day mapping
    tweets = align_tweets_to_trading_days(tweets, fin_df.index)

    # 4. Daily aggregation and merge
    merged_df = aggregate_and_merge(tweets, fin_df)

    # 5. Export to CSV
    merged_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print("=" * 70)
    print(f"Data Pipeline completed successfully!")
    print(f"Output saved to: {OUTPUT_CSV}")
    print(f"Final shape: {merged_df.shape[0]} rows x {merged_df.shape[1]} columns")
    print("=" * 70)

    # Quick summary statistics
    print("\nSummary Statistics of Merged Dataset:")
    print(f"  - Total Trading Days: {len(merged_df)}")
    print(f"  - Trade Tweet Days (Trade_Tweet_Dummy == 1): {merged_df['Trade_Tweet_Dummy'].sum()} days ({merged_df['Trade_Tweet_Dummy'].mean():.1%})")
    print(f"  - Total Trade Tweets Mapped: {merged_df['Trade_Tweet_Count'].sum():,}")
    print(f"  - Fed Tweet Days (Fed_Tweet_Dummy == 1): {merged_df['Fed_Tweet_Dummy'].sum()} days ({merged_df['Fed_Tweet_Dummy'].mean():.1%})")
    print(f"  - Total Fed Tweets Mapped: {merged_df['Fed_Tweet_Count'].sum():,}")
    print(f"  - Non-Tweet Days: {(merged_df['Total_Tweet_Count'] == 0).sum()} days")

    return merged_df


if __name__ == "__main__":
    run_pipeline()
