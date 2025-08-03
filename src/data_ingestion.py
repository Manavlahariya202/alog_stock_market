# src/data_ingestion.py
import yfinance as yf
import pandas as pd
import logging

def fetch_data(tickers, period, interval):
    """Fetches historical stock data for a list of tickers."""
    data = {}
    for ticker in tickers:
        try:
            stock_data = yf.download(ticker, period=period, interval=interval)
            if not stock_data.empty:
                data[ticker] = stock_data
                logging.info(f"Successfully fetched data for {ticker}.")
            else:
                logging.warning(f"No data found for {ticker}.")
        except Exception as e:
            logging.error(f"Could not fetch data for {ticker}: {e}")
    return data