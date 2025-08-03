# Algo-Trading System with ML & Google Sheets Automation

A Python-based prototype for an algorithmic trading system that backtests a trading strategy, uses a simple ML model for prediction, and logs results automatically to Google Sheets.

## Features 🚀
Fetches daily stock data for specified tickers (e.g., NIFTY 50 stocks) using the yfinance library.

Implements and backtests a trading strategy based on RSI + Moving Average Crossover.

Includes a Machine Learning model (Decision Tree) to predict the next day's price movement.

Automatically logs detailed trade data and performance summaries (P&L, Win Ratio) to Google Sheets.

Built with a modular and scalable project structure for easy maintenance and expansion.

## Tech Stack & Libraries 🛠️

Pandas: For data manipulation and analysis.

yfinance: To download historical market data from Yahoo Finance.

pandas-ta: For calculating technical analysis indicators like RSI and Moving Averages.

scikit-learn: For building and evaluating the machine learning model.

gspread: To interact with the Google Sheets API.

schedule: For scheduling the script to run automatically.

## Configuration 🔑
You must configure two things before running the script:

### 1. Google Sheets API Credentials
The script needs a Google Service Account to write to Google Sheets.

Go to the Google Cloud Console, create a new project.

Enable the Google Drive API and Google Sheets API for this project.

Create a Service Account. In the "Keys" section, create a new key and download the JSON file.

Crucial Step: Rename the downloaded file to creds.json and place it inside the config/ directory.

Open the creds.json file, find the client_email address, and copy it.

Create a new Google Sheet, click "Share", and paste the client_email to give it Editor access.

### 2. Project Settings
Open config/settings.py to customize the algorithm:

NIFTY_TICKERS: Change the list of stock tickers you want to analyze.

GOOGLE_SHEET_NAME: Ensure this matches the name of your Google Sheet.

RSI_PERIOD, SMA_SHORT, SMA_LONG, etc.: Adjust the parameters for your trading strategy.

## How to Run ▶️
Once the setup and configuration are complete, you can run the script from the root directory.

code- python main.py
