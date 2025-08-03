# src/sheets_logger.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import logging
from config import settings

def log_to_google_sheets(trade_logs, summaries, sheet_name):
    """Logs trade data and summaries to a Google Sheet."""
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(settings.CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name)
        logging.info("Successfully connected to Google Sheets.")

        for ticker, log_df in trade_logs.items():
            if not log_df.empty:
                worksheet_name = f"{ticker}_Trades"
                try:
                    worksheet = sheet.worksheet(worksheet_name)
                    worksheet.clear()
                except gspread.WorksheetNotFound:
                    worksheet = sheet.add_worksheet(title=worksheet_name, rows=len(log_df)+1, cols=len(log_df.columns))
                worksheet.update([log_df.columns.values.tolist()] + log_df.values.tolist())
        
        summary_df = pd.DataFrame(summaries).T.reset_index()
        summary_df.columns = ['Ticker', 'Total P&L (%)', 'Win Ratio (%)', 'ML Prediction', 'ML Accuracy']
        
        try:
            summary_ws = sheet.worksheet("Summary")
            summary_ws.clear()
        except gspread.WorksheetNotFound:
            summary_ws = sheet.add_worksheet(title="Summary", rows=len(summary_df)+1, cols=len(summary_df.columns))
        summary_ws.update([summary_df.columns.values.tolist()] + summary_df.values.tolist())
        logging.info("Updated summary sheet.")

    except Exception as e:
        logging.error(f"Failed to write to Google Sheets: {e}")