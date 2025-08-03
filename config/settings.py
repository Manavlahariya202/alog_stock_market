# config/settings.py

# Stock tickers to analyze
NIFTY_TICKERS = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS']

# Data fetching parameters
DATA_PERIOD = "7mo"  # Fetch 7 months to ensure enough data for 6mo backtest + indicators
DATA_INTERVAL = "1d"

# Google Sheets configuration
GOOGLE_SHEET_NAME = "stock_market"
CREDENTIALS_FILE = "config/creds.json"

# Strategy parameters
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
SMA_SHORT = 20
SMA_LONG = 50