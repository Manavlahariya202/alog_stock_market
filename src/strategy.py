# src/strategy.py
import pandas as pd
import pandas_ta as ta
import logging
from config import settings

def run_backtest(df):
    """Backtests a trading strategy and returns trade logs and P&L."""
    df.ta.rsi(length=settings.RSI_PERIOD, append=True)
    df.ta.sma(length=settings.SMA_SHORT, append=True)
    df.ta.sma(length=settings.SMA_LONG, append=True)
    df.dropna(inplace=True)

    trades = []
    position = None
    buy_price = 0

    for i in range(1, len(df)):
        current_row = df.iloc[i]
        previous_row = df.iloc[i-1]

        is_golden_cross = current_row[f'SMA_{settings.SMA_SHORT}'] > current_row[f'SMA_{settings.SMA_LONG}'] and \
                          previous_row[f'SMA_{settings.SMA_SHORT}'] <= previous_row[f'SMA_{settings.SMA_LONG}']
        
        if not position and current_row[f'RSI_{settings.RSI_PERIOD}'] < settings.RSI_OVERSOLD and is_golden_cross:
            position = 'LONG'
            buy_price = current_row['Close']
            trades.append({'Date': current_row.name.date(), 'Signal': 'BUY', 'Price': buy_price, 'P&L (%)': 0})

        elif position == 'LONG' and current_row[f'RSI_{settings.RSI_PERIOD}'] > settings.RSI_OVERBOUGHT:
            sell_price = current_row['Close']
            pnl_percent = ((sell_price - buy_price) / buy_price) * 100
            trades[-1]['Signal'] = 'SELL'
            trades[-1]['P&L (%)'] = round(pnl_percent, 2)
            position = None
            
    trade_log = pd.DataFrame(trades)

    # --- FIX: Handle case where no trades are made ---
    if trade_log.empty:
        logging.warning("No trades were generated during the backtest period.")
        return trade_log, 0, 0
    # --- End of FIX ---
    
    completed = trade_log[trade_log['Signal'] == 'SELL']
    
    if completed.empty:
        logging.info("No trades were completed (sold). P&L and Win Ratio are 0.")
        return trade_log, 0, 0

    total_pnl = completed['P&L (%)'].sum()
    win_ratio = (len(completed[completed['P&L (%)'] > 0]) / len(completed)) * 100

    logging.info(f"Backtest complete. Total P&L: {total_pnl:.2f}%, Win Ratio: {win_ratio:.2f}%")
    return trade_log, total_pnl, win_ratio