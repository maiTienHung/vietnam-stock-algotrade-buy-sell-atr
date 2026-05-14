# Vietnam Stock & Derivatives Algotrade - Buy Sell ATR

A Python-based learning project for collecting Vietnamese market data, calculating Buy/Sell ATR signals, running backtests, and exporting trading reports.

This project supports two main backtesting modes:

1. **Vietnamese stock backtesting**
   - Long-only strategy
   - Supports single-stock and multi-stock batch backtesting
   - Example symbols: `FPT`, `HPG`, `VNM`, `VCB`, `MWG`, `SSI`

2. **Vietnamese derivatives backtesting**
   - Long/Short strategy
   - Example symbol: `VN30F1M`

The project was created to practice algorithmic trading concepts, financial data processing, technical indicator implementation, portfolio simulation, derivatives long/short logic, and systematic backtesting.

---

## Project Purpose

This project was created for learning and portfolio-building purposes.

The main goal is to gain hands-on experience with:

- Python programming
- Financial data collection
- OHLCV data preprocessing
- Technical indicator implementation
- Buy/Sell signal generation
- Stock backtesting
- Derivatives long/short backtesting
- Portfolio simulation
- Strategy evaluation across multiple symbols

I built this project to demonstrate my ability to develop a simple algorithmic trading research system as part of my preparation for internship opportunities in software engineering, data analysis, fintech, quantitative research, or algorithmic trading.

---

## Features

- Collect Vietnamese market OHLCV data using `vnstock`
- Save raw market data to CSV
- Preprocess OHLCV price data
- Calculate Buy/Sell ATR signals
- Generate trading signals:
  - `BUY`
  - `SELL`
  - `HOLD`
- Run single-stock backtests
- Run batch backtests across multiple Vietnamese stocks
- Run VN30F1M derivatives long/short backtests
- Simulate stock portfolio management
- Simulate derivatives long/short position management
- Support stop loss and take profit
- Export:
  - trade history
  - equity curve
  - individual symbol summary
  - stock batch summary report
  - derivatives summary report

---

## Supported Markets

### 1. Vietnamese Stock Market

This mode is designed for Vietnamese listed equities.

Example symbols:

```text
FPT, HPG, VNM, VCB, MWG, SSI, CTG, BID, TCB, MBB
```

Stock mode uses a **long-only strategy**:

```text
BUY  -> buy shares if there is no open position
SELL -> sell shares if a position is currently held
HOLD -> do nothing
```

This mode does not support short selling.

---

### 2. Vietnamese Derivatives Market

This mode is designed for Vietnamese index futures simulation, especially:

```text
VN30F1M
```

Derivatives mode uses **long/short logic**:

```text
BUY  -> open LONG, or close SHORT and open LONG
SELL -> open SHORT, or close LONG and open SHORT
HOLD -> keep the current position
```

For derivatives data collection, using source `VCI` is recommended:

```bash
python src/derivatives_backtest.py --symbols VN30F1M --start 2025-01-01 --end 2025-12-31 --interval 1D --source VCI --collect
```

---

## Project Structure

```text
buy-sell-atr/
│
├── src/
│   ├── collect_data.py
│   ├── buy_sell_atr.py
│   ├── portfolio.py
│   ├── backtest_engine.py
│   ├── backtest.py
│   ├── main.py
│   │
│   ├── derivatives_portfolio.py
│   ├── derivatives_backtest_engine.py
│   └── derivatives_backtest.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── backtest/
│   │
│   └── derivatives/
│       ├── raw/
│       ├── processed/
│       └── backtest/
│
├── reports/
│   ├── all_stocks_summary.csv
│   └── derivatives_summary.csv
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Folder Description

| Folder                        | Description                                             |
| ----------------------------- | ------------------------------------------------------- |
| `src/`                        | Contains all Python source code                         |
| `data/raw/`                   | Stores raw OHLCV stock data                             |
| `data/processed/`             | Stores stock data after Buy/Sell ATR signal calculation |
| `data/backtest/`              | Stores stock backtest results                           |
| `data/derivatives/raw/`       | Stores raw derivatives data such as `VN30F1M`           |
| `data/derivatives/processed/` | Stores derivatives data with Buy/Sell ATR signals       |
| `data/derivatives/backtest/`  | Stores derivatives long/short backtest results          |
| `reports/`                    | Stores final summary reports                            |

---

## Main Files

| File                             | Description                                             |
| -------------------------------- | ------------------------------------------------------- |
| `collect_data.py`                | Collects Vietnamese stock and derivatives OHLCV data    |
| `buy_sell_atr.py`                | Calculates Buy/Sell ATR signals                         |
| `portfolio.py`                   | Manages long-only stock portfolio simulation            |
| `backtest_engine.py`             | Core engine for stock long-only backtesting             |
| `backtest.py`                    | Runs batch backtests for multiple Vietnamese stocks     |
| `main.py`                        | Runs the full pipeline for one stock                    |
| `derivatives_portfolio.py`       | Manages derivatives long/short position simulation      |
| `derivatives_backtest_engine.py` | Core engine for derivatives long/short backtesting      |
| `derivatives_backtest.py`        | Runs derivatives backtest for symbols such as `VN30F1M` |

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

# Stock Backtesting

## Run Single-Stock Backtest

Example with `FPT`:

```bash
python src/main.py --symbol FPT --start 2020-01-01 --collect
```

This command will:

1. Collect historical stock data for `FPT`
2. Save raw data to `data/raw/FPT.csv`
3. Calculate Buy/Sell ATR signals
4. Run the stock backtest
5. Export reports and result files

---

## Run Single-Stock Backtest Again Without Downloading Data

After the first run, the raw data is already saved in:

```text
data/raw/FPT.csv
```

Run again without `--collect`:

```bash
python src/main.py --symbol FPT
```

This will reuse the existing data, recalculate signals, and run the backtest again.

---

## Update Stock Data

To download the latest data again:

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

To backtest multiple Vietnamese stocks at once, use:

```bash
python src/backtest.py --symbols FPT HPG VNM VCB MWG SSI --start 2020-01-01 --collect
```

This command will:

1. Download data for all selected stocks
2. Save raw CSV files to `data/raw/`
3. Calculate Buy/Sell ATR signals for each stock
4. Run backtests for each stock
5. Export individual result files
6. Export one combined summary report

---

## Run Batch Backtest Again Without Downloading Data

After data has already been collected:

```bash
python src/backtest.py --symbols FPT HPG VNM VCB MWG SSI
```

This will reuse existing CSV files in:

```text
data/raw/
```

---

## Batch Backtest With Stop Loss and Take Profit

Run multiple stocks with a 7% stop loss and 15% take profit:

```bash
python src/backtest.py --symbols FPT HPG VNM VCB MWG SSI --stop-loss 0.07 --take-profit 0.15
```

---

## Example Stock Groups

### Large-cap stocks

```bash
python src/backtest.py --symbols FPT VNM VCB HPG MWG --start 2020-01-01 --collect
```

### Banking stocks

```bash
python src/backtest.py --symbols VCB CTG BID TCB MBB --start 2020-01-01 --collect
```

### Securities stocks

```bash
python src/backtest.py --symbols SSI VND HCM --start 2020-01-01 --collect
```

### Mixed stock group

```bash
python src/backtest.py --symbols FPT HPG VNM VCB MWG SSI CTG BID TCB MBB --start 2020-01-01 --collect
```

---

# Derivatives Backtesting

## Run VN30F1M Derivatives Backtest

Example with `VN30F1M`:

```bash
python src/derivatives_backtest.py --symbols VN30F1M --start 2025-01-01 --end 2025-12-31 --interval 1D --source VCI --collect
```

This command will:

1. Collect historical data for `VN30F1M`
2. Save raw data to `data/derivatives/raw/VN30F1M.csv`
3. Calculate Buy/Sell ATR signals
4. Run a long/short derivatives backtest
5. Export derivatives trade history, equity curve, and summary

---

## Run Derivatives Backtest Without Downloading Data

After the first run, the raw data is already saved in:

```text
data/derivatives/raw/VN30F1M.csv
```

Run again without `--collect`:

```bash
python src/derivatives_backtest.py --symbols VN30F1M --start 2025-01-01 --end 2025-12-31 --interval 1D --source VCI
```

---

## Run Derivatives Backtest With Stop Loss and Take Profit

Example with 3% stop loss and 6% take profit:

```bash
python src/derivatives_backtest.py --symbols VN30F1M --start 2025-01-01 --end 2025-12-31 --interval 1D --source VCI --stop-loss 0.03 --take-profit 0.06 --collect
```

---

## Run Derivatives Backtest With Custom ATR Parameters

```bash
python src/derivatives_backtest.py --symbols VN30F1M --start 2025-01-01 --end 2025-12-31 --interval 1D --source VCI --trend-period 50 --atr-period 14 --atr-multiplier 1.0 --collect
```

---

## Derivatives Backtest Settings

Default settings:

```text
Initial cash: 100,000,000 VND
Contract multiplier: 100,000
Margin rate: 15%
Fee per contract: 3,000 VND
Quantity: 1 contract per trade
```

Example with custom settings:

```bash
python src/derivatives_backtest.py --symbols VN30F1M --initial-cash 100000000 --contract-multiplier 100000 --margin-rate 0.15 --fee-per-contract 3000 --quantity 1
```

---

# Output Files

## Stock Single-Symbol Output

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

## Stock Batch Output

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

The most important stock batch result file is:

```text
reports/all_stocks_summary.csv
```

---

## Derivatives Output

Example with `VN30F1M`:

```text
data/derivatives/raw/VN30F1M.csv
data/derivatives/processed/VN30F1M_signals.csv
data/derivatives/backtest/VN30F1M_derivatives_trades.csv
data/derivatives/backtest/VN30F1M_derivatives_equity.csv
data/derivatives/backtest/VN30F1M_derivatives_summary.csv
reports/derivatives_summary.csv
```

| File                              | Description                      |
| --------------------------------- | -------------------------------- |
| `VN30F1M.csv`                     | Raw OHLCV derivatives data       |
| `VN30F1M_signals.csv`             | Data with BUY/SELL/HOLD signals  |
| `VN30F1M_derivatives_trades.csv`  | Long/short trade history         |
| `VN30F1M_derivatives_equity.csv`  | Derivatives equity curve         |
| `VN30F1M_derivatives_summary.csv` | Individual derivatives summary   |
| `derivatives_summary.csv`         | Final derivatives summary report |

---

# Input Data Format

The input data should contain the following columns:

```csv
date,ticker,open,high,low,close,volume
```

Example:

```csv
date,ticker,open,high,low,close,volume
2025-01-02,VN30F1M,1280,1290,1270,1285,10000
2025-01-03,VN30F1M,1285,1300,1280,1295,12000
```

If the project is run with `--collect`, the CSV files will be created automatically.

---

# Data Preprocessing

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

# Strategy Logic

This project uses the Buy/Sell ATR indicator.

Default parameters:

```text
Trend Period = 20
ATR Period = 5
ATR Multiplier = 0.5
```

Basic signal logic:

```text
BUY  when price breaks above the bullish ATR trend zone
SELL when price breaks below the bearish ATR trend zone
HOLD when there is no new signal
```

---

## ATR Explanation

ATR stands for **Average True Range**.

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

# Backtest Logic

## Stock Mode

Stock mode is long-only:

```text
BUY  -> buy shares if there is no open position
SELL -> sell shares if a position is currently held
HOLD -> do nothing
```

This mode is suitable for Vietnamese listed stocks.

---

## Derivatives Mode

Derivatives mode supports both long and short positions:

```text
BUY:
    if currently SHORT -> close SHORT and open LONG
    if no position      -> open LONG

SELL:
    if currently LONG -> close LONG and open SHORT
    if no position    -> open SHORT

HOLD:
    keep the current position
```

This mode is suitable for basic VN30 futures strategy simulation.

---

# Default Backtest Settings

## Stock Mode

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

For batch stock backtesting:

```bash
python src/backtest.py --symbols FPT HPG VNM --initial-cash 50000000 --fee-rate 0.001 --sell-tax-rate 0.001
```

---

## Derivatives Mode

```text
Initial cash: 100,000,000 VND
Contract multiplier: 100,000
Margin rate: 15%
Fee per contract: 3,000 VND
Quantity: 1 contract
```

You can change these values using command-line arguments:

```bash
python src/derivatives_backtest.py --symbols VN30F1M --initial-cash 100000000 --contract-multiplier 100000 --margin-rate 0.15 --fee-per-contract 3000 --quantity 1
```

---

# Example Commands

## Single Stock

```bash
python src/main.py --symbol FPT --start 2020-01-01 --collect
```

## Single Stock With Risk Management

```bash
python src/main.py --symbol FPT --start 2020-01-01 --collect --stop-loss 0.07 --take-profit 0.15
```

## Multiple Stocks

```bash
python src/backtest.py --symbols FPT HPG VNM VCB MWG SSI --start 2020-01-01 --collect
```

## Multiple Stocks With Risk Management

```bash
python src/backtest.py --symbols FPT HPG VNM VCB MWG SSI --start 2020-01-01 --collect --stop-loss 0.07 --take-profit 0.15
```

## VN30F1M Derivatives

```bash
python src/derivatives_backtest.py --symbols VN30F1M --start 2025-01-01 --end 2025-12-31 --interval 1D --source VCI --collect
```

## VN30F1M Derivatives With Risk Management

```bash
python src/derivatives_backtest.py --symbols VN30F1M --start 2025-01-01 --end 2025-12-31 --interval 1D --source VCI --stop-loss 0.03 --take-profit 0.06 --collect
```

---

# Notes

When tested across multiple Vietnamese stocks, the Buy/Sell ATR strategy does not always produce positive returns.

This is expected because the strategy is sensitive to:

- market conditions
- stock characteristics
- volatility
- parameter settings
- transaction costs
- test period

Negative backtest results are useful for evaluating the limitations of the strategy and identifying areas for improvement.

---

# Limitations

This is a simplified backtesting project.

Current limitations include:

- No slippage modeling
- No liquidity constraint modeling
- No advanced position sizing
- No benchmark comparison yet
- No dividend or corporate action adjustment
- No contract rollover logic for derivatives
- No margin call simulation
- No detailed exchange-level derivatives fee model
- No live trading execution
- No real-time data feed

The derivatives module is a simplified long/short simulation and should not be treated as a production-ready futures trading system.

---

# Future Improvements

Possible future improvements:

- Add Buy and Hold benchmark comparison
- Add chart visualization for BUY/SELL signals
- Add equity curve charts
- Add max drawdown calculation
- Add Sharpe ratio
- Add win/loss average metrics
- Add parameter optimization
- Add support for more technical indicators
- Add better risk management
- Add derivatives rollover logic
- Add unit tests
- Add live data integration

---

# Disclaimer

This project is for educational, research, and portfolio demonstration purposes only.

It is not financial advice and should not be used as a direct investment recommendation.

Trading strategies should be tested carefully with proper risk management before being considered for real-world use.
