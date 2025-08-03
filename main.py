# main.py

import schedule
import time
import logging
import pandas as pd

# ... (your other imports) ...
from config import settings
from src.data_ingestion import fetch_data
from src.strategy import run_backtest
from src.ml_model import get_ml_prediction
from src.sheets_logger import log_to_google_sheets

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_trading_algo():
    """Main function to run the entire trading algorithm workflow."""
    logging.info("--- Starting Algo Trading Cycle ---")
    
    stock_data_dict = fetch_data(settings.NIFTY_TICKERS, settings.DATA_PERIOD, settings.DATA_INTERVAL)
    
    all_trade_logs = {}
    all_summaries = {}
    
    for ticker, df in stock_data_dict.items():
        if df.empty:
            continue
            
        # --- FIX: Flatten MultiIndex columns if they exist ---
        if isinstance(df.columns, pd.MultiIndex):
            logging.info(f"Flattening MultiIndex columns for {ticker}.")
            # Keeps the first level of the column index (e.g., 'Open', 'Close')
            df.columns = df.columns.get_level_values(0)
        # --- End of FIX ---

        logging.info(f"--- Processing {ticker} ---")
        trade_log, total_pnl, win_ratio = run_backtest(df.copy())
        prediction, accuracy = get_ml_prediction(df.copy())
        
        all_trade_logs[ticker] = trade_log
        all_summaries[ticker] = {
            'Total P&L (%)': round(total_pnl, 2),
            'Win Ratio (%)': round(win_ratio, 2),
            'ML Prediction': prediction,
            'ML Accuracy': round(accuracy, 2)
        }
        
    if all_summaries:
        log_to_google_sheets(all_trade_logs, all_summaries, settings.GOOGLE_SHEET_NAME)
        
    logging.info("--- Algo Trading Cycle Finished ---\n")


if __name__ == "__main__":
    run_trading_algo()
    # ... (your scheduling code) ...
    
    
    
    
    
    # Uncomment the lines below to schedule the job
    # schedule.every().day.at("09:00").do(run_trading_algo)
    # logging.info("Scheduler started. Bot will run daily at 09:00.")
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60) # Check every minute