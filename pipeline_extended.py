"""
Trump 1st Term (2017-01-20 ~ 2021-01-20) Extended Financial Market Pipeline
----------------------------------------------------------------------------
Collects Donald Trump's tweets and an extended set of financial indicators:
- Broad Macro: S&P 500, Dollar Index, VIX, UUP
- US Industry / Sector: Nucor (NUE), Steel ETF (SLX), Industrials (XLI), Semis (SOXX)
- Target Companies: Apple (AAPL), Boeing (BA), Caterpillar (CAT)
- Fed / Bonds: 10Y Treasury (^TNX), 1-3Y Treasury (SHY), Financials (XLF)
- China & Safe Haven: China Large-Cap (FXI), USD/CNY (CNY=X), Gold (GLD)
"""

import os
import re
import pandas as pd
import numpy as np
import yfinance as yf

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(DATA_DIR, "trump_market_extended_data.csv")

START_DATE = "2017-01-20"
END_DATE = "2021-01-20"

TWEET_ARCHIVE_URL = (
    "https://raw.githubusercontent.com/ttzztztz/TrumpTwitterArchive/master/trump.json"
)

EXTENDED_TICKERS = {
    # Broad Macro
    "SP500": "^GSPC",
    "DXY": "DX-Y.NYB",
    "UUP": "UUP",
    "VIX": "^VIX",
    # US Industry / Tariff Protection vs Hurt
    "NUE": "NUE",       # Nucor (US Steel Producer - Tariff beneficiary)
    "SLX": "SLX",       # Steel ETF
    "XLI": "XLI",       # Industrial Select Sector SPDR (Tariff victim)
    "SOXX": "SOXX",     # Semiconductor ETF (Tech war victim)
    # Direct Target / China Exposure US Firms
    "AAPL": "AAPL",     # Apple (Supply chain & China market)
    "BA": "BA",         # Boeing (Direct Trump tweet target & China retaliation)
    "CAT": "CAT",       # Caterpillar (Capital goods export)
    # Fed / Interest Rates / Financials
    "TNX": "^TNX",       # 10-Year US Treasury Yield (Level in %)
    "SHY": "SHY",       # 1-3 Year Treasury Bond ETF (Short-term rate proxy)
    "XLF": "XLF",       # Financial Sector SPDR
    # China Spillover & Safe Havens
    "FXI": "FXI",       # iShares China Large-Cap ETF
    "CNY": "CNY=X",     # USD/CNY Exchange Rate
    "GLD": "GLD",       # SPDR Gold Trust (Safe haven asset)
}


def load_trump_tweets(url: str, start_date: str, end_date: str) -> pd.DataFrame:
    print(f"[1/4] Loading Trump Twitter Archive from {url} ...")
    raw_df = pd.read_json(url)
    raw_df["date_utc"] = pd.to_datetime(raw_df["date"], utc=True)

    mask = (raw_df["date_utc"] >= f"{start_date} 00:00:00+00:00") & (
        raw_df["date_utc"] <= f"{end_date} 23:59:59+00:00"
    )
    tweets = raw_df.loc[mask].copy()

    tweets = tweets.rename(
        columns={
            "text": "tweet_text",
            "retweets": "retweet_count",
            "favorites": "favorite_count",
        }
    )
    tweets["retweet_count"] = tweets["retweet_count"].fillna(0).astype(int)
    tweets["favorite_count"] = tweets["favorite_count"].fillna(0).astype(int)
    tweets["tweet_text"] = tweets["tweet_text"].fillna("").astype(str)
    return tweets


def apply_keyword_filters(tweets: pd.DataFrame) -> pd.DataFrame:
    print("[1b/4] Applying keyword filters ...")
    trade_keywords = ["tariff", "tariffs", "trade war", "china", "beijing", "xi jinping"]
    trade_pattern = r"(?i)\b(" + "|".join([re.escape(k) for k in trade_keywords]) + r")\b"
    tweets["is_trade_tweet"] = tweets["tweet_text"].str.contains(trade_pattern, regex=True).astype(int)

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

    print(f"      Trade tweets: {tweets['is_trade_tweet'].sum():,}")
    print(f"      Fed tweets:   {tweets['is_fed_tweet'].sum():,}")
    return tweets


def load_extended_financial_data(tickers: dict, start_date: str, end_date: str) -> pd.DataFrame:
    print("[2/4] Downloading extended financial tickers via yfinance ...")
    fetch_start = (pd.to_datetime(start_date) - pd.Timedelta(days=15)).strftime("%Y-%m-%d")
    fetch_end = (pd.to_datetime(end_date) + pd.Timedelta(days=5)).strftime("%Y-%m-%d")

    ticker_list = list(tickers.values())
    raw_data = yf.download(
        ticker_list,
        start=fetch_start,
        end=fetch_end,
        group_by="ticker",
        auto_adjust=False,
        progress=False,
    )

    combined_fin = pd.DataFrame()
    inv_map = {v: k for k, v in tickers.items()}

    for ticker_symbol, alias in inv_map.items():
        if ticker_symbol not in raw_data.columns.levels[0]:
            print(f"      [Warning] Missing {ticker_symbol}")
            continue

        df_t = raw_data[ticker_symbol].copy()
        df_t = df_t[["Open", "High", "Low", "Close"]].dropna(how="all")

        # Daily Return
        df_t["Daily_Return"] = df_t["Close"].pct_change()

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

    combined_fin.index = pd.to_datetime(combined_fin.index)

    # Use regular US equity market calendar (^GSPC) as the authoritative trading day spine
    sp500_calendar = raw_data["^GSPC"].dropna(how="all").index
    fin_df = combined_fin.reindex(sp500_calendar).loc[start_date:end_date].copy()
    
    # Fill any minor foreign exchange or asset holidays with previous valid market price
    fin_df = fin_df.ffill().bfill()
    print(f"      Total trading days in target window (aligned to US Equities): {len(fin_df)}")
    return fin_df


def align_tweets_to_trading_days(tweets: pd.DataFrame, trading_calendar: pd.DatetimeIndex) -> pd.DataFrame:
    print("[3/4] Aligning tweet timestamps to US Eastern Time and Trading Calendar ...")
    tweets["date_eastern"] = tweets["date_utc"].dt.tz_convert("America/New_York")
    eastern_dates = tweets["date_eastern"].dt.normalize().dt.tz_localize(None)
    time_minutes = tweets["date_eastern"].dt.hour * 60 + tweets["date_eastern"].dt.minute

    is_post_market = time_minutes >= (16 * 60)
    target_dates = eastern_dates + pd.to_timedelta(np.where(is_post_market, 1, 0), unit="D")

    clean_trading_days = pd.Series(trading_calendar.tz_localize(None).normalize()).sort_values().values
    idx = np.searchsorted(clean_trading_days, target_dates.values)

    valid_mask = idx < len(clean_trading_days)
    mapped_days = np.full(len(tweets), np.nan, dtype="datetime64[ns]")
    mapped_days[valid_mask] = clean_trading_days[idx[valid_mask]]

    tweets["mapped_trading_date"] = pd.to_datetime(mapped_days)
    return tweets


def aggregate_and_merge(tweets: pd.DataFrame, fin_df: pd.DataFrame) -> pd.DataFrame:
    print("[4/4] Aggregating tweet metrics and merging with extended financial time series ...")
    mapped_tweets = tweets.dropna(subset=["mapped_trading_date"]).copy()

    daily_agg = mapped_tweets.groupby("mapped_trading_date").agg(
        Total_Tweet_Count=("tweet_text", "count"),
        Trade_Tweet_Count=("is_trade_tweet", "sum"),
        Fed_Tweet_Count=("is_fed_tweet", "sum"),
        Trade_Retweet_Sum=("retweet_count", lambda s: s[mapped_tweets.loc[s.index, "is_trade_tweet"] == 1].sum()),
        Trade_Favorite_Sum=("favorite_count", lambda s: s[mapped_tweets.loc[s.index, "is_trade_tweet"] == 1].sum()),
        Fed_Retweet_Sum=("retweet_count", lambda s: s[mapped_tweets.loc[s.index, "is_fed_tweet"] == 1].sum()),
        Fed_Favorite_Sum=("favorite_count", lambda s: s[mapped_tweets.loc[s.index, "is_fed_tweet"] == 1].sum()),
    )

    daily_agg["Trade_Tweet_Dummy"] = (daily_agg["Trade_Tweet_Count"] > 0).astype(int)
    daily_agg["Fed_Tweet_Dummy"] = (daily_agg["Fed_Tweet_Count"] > 0).astype(int)

    fin_df_clean = fin_df.copy()
    fin_df_clean.index = fin_df_clean.index.tz_localize(None).normalize()
    fin_df_clean.index.name = "Trading_Date"

    merged_df = fin_df_clean.join(daily_agg, how="left")

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

    # Forward fill financial prices if small holidays exist
    price_cols = [c for c in merged_df.columns if "_Close" in c or "_Return" in c]
    merged_df[price_cols] = merged_df[price_cols].ffill()

    merged_df = merged_df.reset_index().rename(columns={"Trading_Date": "Date"})
    merged_df["Date"] = merged_df["Date"].dt.strftime("%Y-%m-%d")
    return merged_df


def run_extended_pipeline():
    print("=" * 75)
    print("Trump 1st Term Extended Financial Pipeline Starting")
    print("=" * 75)
    tweets = load_trump_tweets(TWEET_ARCHIVE_URL, START_DATE, END_DATE)
    tweets = apply_keyword_filters(tweets)
    fin_df = load_extended_financial_data(EXTENDED_TICKERS, START_DATE, END_DATE)
    tweets = align_tweets_to_trading_days(tweets, fin_df.index)
    merged_df = aggregate_and_merge(tweets, fin_df)

    merged_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print("=" * 75)
    print(f"Extended Pipeline completed successfully!")
    print(f"Output saved to: {OUTPUT_CSV}")
    print(f"Final shape: {merged_df.shape[0]} rows x {merged_df.shape[1]} columns")
    print("=" * 75)
    return merged_df


if __name__ == "__main__":
    run_extended_pipeline()
