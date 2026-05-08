# Vietnam Stock Algotrade - Buy Sell ATR

A Python-based learning project for collecting Vietnamese stock market data, calculating Buy/Sell ATR signals, running backtests, and exporting trading reports.

This project was built to practice algorithmic trading concepts, financial data processing, technical indicator implementation, portfolio simulation, and systematic backtesting.

The system supports both:

- Single-stock backtesting
- Batch backtesting across multiple Vietnamese stocks

Example stock symbols:

```text
FPT, HPG, VNM, VCB, MWG, SSI, CTG, BID, TCB, MBB
```

---

## Project Purpose

This project was created for learning and portfolio-building purposes.

The main goal is to gain hands-on experience with:

- Python programming
- Financial data collection
- OHLCV data preprocessing
- Technical indicator implementation
- Buy/Sell signal generation
- Backtesting
- Portfolio simulation
- Batch strategy evaluation across multiple stocks

I built this project to demonstrate my ability to develop a simple algorithmic trading research system as part of my preparation for internship opportunities in software engineering, data analysis, fintech, quantitative research, or algorithmic trading.

---

## Features

- Collect Vietnamese stock OHLCV data using `vnstock`
- Save raw stock data to CSV
- Preprocess stock price data
- Calculate Buy/Sell ATR signals
- Generate trading signals:
  - `BUY`
  - `SELL`
  - `HOLD`
- Run a simple backtest for one stock
- Run batch backtests for multiple Vietnamese stocks
- Simulate portfolio management
- Support stop loss and take profit
- Export:
  - trade history
  - equity curve
  - individual stock summary
  - all-stocks summary report

---

## Project Structure

```text
buy-sell-atr/
│
├── src/
│   ├── collect_data.py
│   ├── buy_sell_atr.py
│   ├── backtest.py
│   ├── portfolio.py
│   ├── main.py
│   └── batch_backtest.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── backtest/
│
├── reports/
│   └── all_stocks_summary.csv
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Main Files

| File                | Description                                       |
| ------------------- | ------------------------------------------------- |
| `collect_data.py`   | Collects Vietnamese stock market data             |
| `buy_sell_atr.py`   | Calculates Buy/Sell ATR signals                   |
| `portfolio.py`      | Manages cash, shares, trades, and portfolio value |
| `backtest.py`       | Runs the backtest based on BUY/SELL/HOLD signals  |
| `main.py`           | Runs the full pipeline for one stock              |
| `batch_backtest.py` | Runs backtests for multiple Vietnamese stocks     |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/maiTienHung/vietnam-stock-algotrade-buy-sell-atr.git
cd vietnam-stock-algotrade-buy-sell-atr
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```txt
pandas
numpy
vnstock
```

---

## How to Run Single-Stock Backtest

### First run: collect data and run backtest

Example with `FPT`:

```bash
python src/main.py --symbol FPT --start 2020-01-01 --collect
```

This command will:

1. Collect historical stock data for `FPT`
2. Save raw data to `data/raw/FPT.csv`
3. Calculate Buy/Sell ATR signals
4. Run the backtest
5. Export reports and result files

---

## Run Again Without Downloading New Data

After the first run, the raw data is already saved in:

```text
data/raw/FPT.csv
```

You can run the project again using:

```bash
python src/main.py --symbol FPT
```

This will reuse the existing data, recalculate the signals, and run the backtest again.

---

## Update Stock Data

To download the latest data again, run:

```bash
python src/main.py --symbol FPT --start 2020-01-01 --collect
```

When using `--collect`, the old raw CSV file will be overwritten:

```text
data/raw/FPT.csv
```

---

## Run Single Stock With Stop Loss and Take Profit

Run with a 7% stop loss:

```bash
python src/main.py --symbol FPT --stop-loss 0.07
```

Run with a 15% take profit:

```bash
python src/main.py --symbol FPT --take-profit 0.15
```

Run with both stop loss and take profit:

```bash
python src/main.py --symbol FPT --stop-loss 0.07 --take-profit 0.15
```

Full example:

```bash
python src/main.py --symbol FPT --start 2020-01-01 --collect --stop-loss 0.07 --take-profit 0.15
```

---

## Batch Backtest Multiple Vietnamese Stocks

To backtest multiple Vietnamese stocks at once, use `batch_backtest.py`.

### First run: collect data and backtest multiple stocks

```bash
python src/batch_backtest.py --symbols FPT HPG VNM VCB MWG SSI --start 2020-01-01 --collect
```

This command will:

1. Download data for all selected stocks
2. Save raw CSV files to `data/raw/`
3. Calculate Buy/Sell ATR signals for each stock
4. Run backtests for each stock
5. Export individual result files
6. Export one combined summary report

---

## Run Batch Backtest Again Without Downloading New Data

After the data has already been collected, run:

```bash
python src/batch_backtest.py --symbols FPT HPG VNM VCB MWG SSI
```

This will reuse existing CSV files in:

```text
data/raw/
```

---

## Batch Backtest With Stop Loss and Take Profit

Run multiple stocks with a 7% stop loss and 15% take profit:

```bash
python src/batch_backtest.py --symbols FPT HPG VNM VCB MWG SSI --stop-loss 0.07 --take-profit 0.15
```

---

## Example Stock Groups

You can test different groups of Vietnamese stocks.

### Large-cap stocks

```bash
python src/batch_backtest.py --symbols FPT VNM VCB HPG MWG --start 2020-01-01 --collect
```

### Banking stocks

```bash
python src/batch_backtest.py --symbols VCB CTG BID TCB MBB --start 2020-01-01 --collect
```

### Securities stocks

```bash
python src/batch_backtest.py --symbols SSI VND HCM --start 2020-01-01 --collect
```

### Mixed portfolio test

```bash
python src/batch_backtest.py --symbols FPT HPG VNM VCB MWG SSI CTG BID TCB MBB --start 2020-01-01 --collect
```

---

## Output Files

### Single-stock output

Example with `FPT`:

```text
data/raw/FPT.csv
data/processed/FPT_signals.csv
data/backtest/FPT_trades.csv
data/backtest/FPT_equity.csv
data/backtest/FPT_summary.csv
reports/FPT_report.csv
```

| File              | Description                           |
| ----------------- | ------------------------------------- |
| `FPT.csv`         | Raw OHLCV stock data                  |
| `FPT_signals.csv` | Stock data with BUY/SELL/HOLD signals |
| `FPT_trades.csv`  | Simulated trade history               |
| `FPT_equity.csv`  | Portfolio value over time             |
| `FPT_summary.csv` | Backtest summary                      |
| `FPT_report.csv`  | Final report                          |

---

### Batch backtest output

Example with `FPT`, `HPG`, and `VNM`:

```text
data/raw/FPT.csv
data/raw/HPG.csv
data/raw/VNM.csv

data/processed/FPT_signals.csv
data/processed/HPG_signals.csv
data/processed/VNM_signals.csv

data/backtest/FPT_trades.csv
data/backtest/HPG_trades.csv
data/backtest/VNM_trades.csv

data/backtest/FPT_equity.csv
data/backtest/HPG_equity.csv
data/backtest/VNM_equity.csv

data/backtest/FPT_summary.csv
data/backtest/HPG_summary.csv
data/backtest/VNM_summary.csv

reports/all_stocks_summary.csv
```

The most important batch result file is:

```text
reports/all_stocks_summary.csv
```

This file compares the backtest results of all selected stocks.

---

## Input Data Format

The input stock data should contain the following columns:

```csv
date,ticker,open,high,low,close,volume
```

Example:

```csv
date,ticker,open,high,low,close,volume
2024-01-02,FPT,95000,97000,94500,96500,1200000
2024-01-03,FPT,96500,98000,96000,97500,1350000
```

If the project is run with `--collect`, the CSV files will be created automatically.

---

## Data Preprocessing

The project includes basic data preprocessing before calculating trading signals and running the backtest.

The preprocessing steps include:

- Standardizing column names
- Converting date values to datetime format
- Converting OHLCV columns to numeric values
- Removing rows with missing price data
- Removing duplicate records by date
- Sorting data chronologically

These steps help ensure that the OHLCV data is clean and suitable for indicator calculation and backtesting.

---

## Strategy Logic

This project uses the Buy/Sell ATR indicator.

Default parameters:

```text
Trend Period = 20
ATR Period = 5
ATR Multiplier = 0.5
```

Basic logic:

```text
BUY  when price breaks above the bullish ATR trend zone
SELL when price breaks below the bearish ATR trend zone
HOLD when there is no new signal
```

Backtest behavior:

```text
BUY  -> buy shares if there is no open position
SELL -> sell shares if a position is currently held
HOLD -> do nothing
```

The current backtest is long-only, meaning the system buys stocks and later sells them. It does not support short selling.

---

## What ATR Means

ATR stands for Average True Range.

It is a volatility indicator that measures how much the price typically moves over a given period.

ATR does not predict whether the price will go up or down. Instead, it measures whether the market is moving strongly or quietly.

In this project, ATR is used as a dynamic buffer around the trend midpoint:

```text
epsilon = ATR * ATR Multiplier
upper_band = middle + epsilon
lower_band = middle - epsilon
```

This helps reduce noisy signals.

When volatility is high, the ATR buffer becomes wider.  
When volatility is low, the ATR buffer becomes narrower.

---

## Default Backtest Settings

```text
Initial cash: 100,000,000 VND
Lot size: 100 shares
Trading fee: 0.1%
Selling tax/fee: 0.1%
```

You can change these values using command-line arguments:

```bash
python src/main.py --symbol FPT --initial-cash 50000000 --fee-rate 0.001 --sell-tax-rate 0.001
```

For batch backtesting:

```bash
python src/batch_backtest.py --symbols FPT HPG VNM --initial-cash 50000000 --fee-rate 0.001 --sell-tax-rate 0.001
```

---

## Example Commands

### Single stock

```bash
python src/main.py --symbol FPT --start 2020-01-01 --collect
```

### Single stock with risk management

```bash
python src/main.py --symbol FPT --start 2020-01-01 --collect --stop-loss 0.07 --take-profit 0.15
```

### Multiple stocks

```bash
python src/batch_backtest.py --symbols FPT HPG VNM VCB MWG SSI --start 2020-01-01 --collect
```

### Multiple stocks with risk management

```bash
python src/batch_backtest.py --symbols FPT HPG VNM VCB MWG SSI --start 2020-01-01 --collect --stop-loss 0.07 --take-profit 0.15
```

---

## Limitations

This is a simplified backtesting project.

Current limitations include:

- No slippage modeling
- No liquidity constraint modeling
- No advanced position sizing
- No benchmark comparison yet
- No dividend or corporate action adjustment
- No futures or derivatives mechanics
- No short selling
- No live trading execution

## Purposes

The project is designed for learning, research, and portfolio demonstration purposes.

It helps me practice Python programming, financial data processing, technical indicator implementation, backtesting, and basic portfolio simulation.

I built this project to gain practical experience and demonstrate my ability to develop a simple algorithmic trading system as part of my preparation for internship applications.
