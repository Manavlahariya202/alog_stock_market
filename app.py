# import streamlit as st
# import pandas as pd

# # Import your existing backend functions
# from config import settings
# from src.data_ingestion import fetch_data
# from src.strategy import run_backtest
# from src.ml_model import get_ml_prediction

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="Algo-Trading Strategy Analyzer",
#     page_icon="📈",
#     layout="wide"
# )

# # --- App Title ---
# st.title("📈 Algo-Trading Strategy Analyzer")
# st.caption("Backtest an RSI + Moving Average Crossover strategy and get ML-based predictions.")

# # --- UI: Sidebar for User Inputs ---
# with st.sidebar:
#     st.header("⚙️ Configuration")
    
#     # Stock selection dropdown
#     selected_stocks = st.multiselect(
#         "Select Nifty 50 Stocks for Analysis",
#         options=settings.NIFTY_50_STOCKS,
#         default=['RELIANCE.NS', 'TCS.NS']  # Default selected stocks
#     )
    
#     # Analysis button
#     run_button = st.button("Run Analysis", type="primary")

# # --- Main Page Logic ---
# if run_button:
#     if not selected_stocks:
#         st.warning("Please select at least one stock to analyze.")
#     else:
#         # Show a spinner while the backend runs
#         with st.spinner("Fetching data and running analysis... This may take a moment."):
            
#             # 1. Fetch data for all selected stocks
#             stock_data_dict = fetch_data(selected_stocks, settings.DATA_PERIOD, settings.DATA_INTERVAL)
            
#             st.success("Data fetched! Now processing strategies...")

#         # 2. Loop through each stock and display results
#         for ticker, df in stock_data_dict.items():
#             if df.empty:
#                 st.error(f"Could not retrieve data for {ticker}. It might be delisted or a temporary network issue.")
#                 continue

#             # Clean data (handle MultiIndex columns)
#             if isinstance(df.columns, pd.MultiIndex):
#                 df.columns = df.columns.get_level_values(0)
            
#             # --- Display Results for each stock ---
#             st.header(f"Results for {ticker}", divider="rainbow")

#             # Run backtest and ML model
#             trade_log, total_pnl, win_ratio = run_backtest(df.copy())
#             prediction, accuracy = get_ml_prediction(df.copy())

#             # Display key metrics in columns
#             col1, col2, col3, col4 = st.columns(4)
#             col1.metric("Total P&L (%)", f"{total_pnl:.2f}%")
#             col2.metric("Win Ratio (%)", f"{win_ratio:.2f}%")
#             col3.metric("ML Prediction", prediction)
#             col4.metric("ML Model Accuracy", f"{accuracy*100:.2f}%")
            
# else:
#     st.info("Select stocks from the sidebar and click 'Run Analysis' to begin.")




import streamlit as st
import pandas as pd

# Import your existing backend functions
from config import settings
from src.data_ingestion import fetch_data
from src.strategy import run_backtest
from src.ml_model import get_ml_prediction
from src.sheets_logger import log_to_google_sheets # <-- Import the logger

# --- Page Configuration ---
st.set_page_config(
    page_title="Algo-Trading Strategy Analyzer",
    page_icon="📈",
    layout="wide"
)

# --- App Title ---
st.title("📈 Algo-Trading Strategy Analyzer")
st.caption("Backtest an RSI + Moving Average Crossover strategy and get ML-based predictions.")

# --- UI: Sidebar for User Inputs ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    selected_stocks = st.multiselect(
        "Select Nifty 50 Stocks for Analysis",
        options=settings.NIFTY_50_STOCKS,
        default=['RELIANCE.NS', 'TCS.NS']
    )
    
    run_button = st.button("Run Analysis", type="primary")

# --- Main Page Logic ---
if run_button:
    if not selected_stocks:
        st.warning("Please select at least one stock to analyze.")
    else:
        with st.spinner("Fetching data and running analysis..."):
            
            stock_data_dict = fetch_data(selected_stocks, settings.DATA_PERIOD, settings.DATA_INTERVAL)
            
            # --- NEW: Initialize dictionaries to store all results for logging ---
            all_trade_logs = {}
            all_summaries = {}

            st.success("Data fetched! Now processing strategies...")

            for ticker, df in stock_data_dict.items():
                if df.empty:
                    st.error(f"Could not retrieve data for {ticker}.")
                    continue

                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                
                st.header(f"Results for {ticker}", divider="rainbow")

                trade_log, total_pnl, win_ratio = run_backtest(df.copy())
                prediction, accuracy = get_ml_prediction(df.copy())

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total P&L (%)", f"{total_pnl:.2f}%")
                col2.metric("Win Ratio (%)", f"{win_ratio:.2f}%")
                col3.metric("ML Prediction", prediction)
                col4.metric("ML Model Accuracy", f"{accuracy*100:.2f}%")
                
                with st.expander("View Trade Log"):
                    if not trade_log.empty:
                        st.dataframe(trade_log)
                    else:
                        st.info("No trades were executed for this stock.")

                # --- NEW: Store results for the current ticker ---
                all_trade_logs[ticker] = trade_log
                all_summaries[ticker] = {
                    'Total P&L (%)': round(total_pnl, 2),
                    'Win Ratio (%)': round(win_ratio, 2),
                    'ML Prediction': prediction,
                    'ML Accuracy': round(accuracy, 2)
                }

            # --- NEW: After the loop, log all collected results to Google Sheets ---
            if all_summaries:
                st.info("Logging results to Google Sheets...")
                log_to_google_sheets(all_trade_logs, all_summaries, settings.GOOGLE_SHEET_NAME)
                st.success("✅ Results have been successfully logged to your Google Sheet!")

else:
    st.info("Select stocks from the sidebar and click 'Run Analysis' to begin.")