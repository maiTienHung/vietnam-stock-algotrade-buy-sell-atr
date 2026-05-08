# Vietnam Stock Algotrade - Buy Sell ATR

A basic Python project for collecting Vietnamese stock market data, calculating Buy/Sell ATR Type A signals, running a simple backtest, and exporting trading reports.

The project currently focuses on one stock symbol at a time, for example: `FPT`.

## Features

- Collect Vietnamese stock OHLCV data using `vnstock`
- Save raw stock data to CSV
- Calculate Buy/Sell ATR signals
- Generate trading signals:
  - `BUY`
  - `SELL`
  - `HOLD`
- Run a simple backtest
- Simulate portfolio management
- Export trade history, equity curve, and backtest summary

## Project Structure

```text
buy-sell-atr/
│
├── src/
│   ├── collect_data.py
│   ├── buy_sell_atr.py
│   ├── backtest.py
│   ├── portfolio.py
│   └── main.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── backtest/
│
├── reports/
├── requirements.txt
├── README.md
└── .gitignore
```

## Main Files

| File              | Description                                 |
| ----------------- | ------------------------------------------- |
| `collect_data.py` | Collects Vietnamese stock market data       |
| `buy_sell_atr.py` | Calculates Buy/Sell ATR Type A signals      |
| `portfolio.py`    | Manages cash, shares, and portfolio value   |
| `backtest.py`     | Runs the backtest based on BUY/SELL signals |
| `main.py`         | Main entry point of the project             |

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

## How to Run

### First run: collect data and run backtest

```bash
python src/main.py --symbol FPT --start 2020-01-01 --collect
```

This command will:

1. Collect historical stock data for `FPT`
2. Save raw data to `data/raw/FPT.csv`
3. Calculate Buy/Sell ATR signals
4. Run the backtest
5. Export reports and result files

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

## Update Stock Data

To download the latest data again, run:

```bash
python src/main.py --symbol FPT --start 2020-01-01 --collect
```

When using `--collect`, the old raw CSV file will be overwritten:

```text
data/raw/FPT.csv
```

## Run With Stop Loss and Take Profit

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

## Output Files

After running the project, the following files will be generated:

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

If you run the project with `--collect`, the CSV file will be created automatically.

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

## Full Example

```bash
python src/main.py --symbol FPT --start 2020-01-01 --collect --stop-loss 0.07 --take-profit 0.15
```

## Purpose

This project was created for learning and portfolio-building purposes.  
It helps me practice Python programming, financial data processing, technical indicator implementation, backtesting, and basic portfolio simulation.

I built this project to gain practical experience and demonstrate my ability to develop a simple algorithmic trading system as part of my preparation for internship applications.
