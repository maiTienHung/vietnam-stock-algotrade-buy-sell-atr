import os
import argparse
import pandas as pd

from collect_data import collect_vietnam_stock_data
from buy_sell_atr import calculate_buy_sell_atr
from derivatives_backtest_engine import (
    run_derivatives_backtest,
    save_derivatives_backtest_results
)


def run_single_derivatives_symbol(
    symbol: str,
    start: str,
    end: str | None,
    interval: str,
    source: str,
    collect: bool,
    initial_cash: float,
    contract_multiplier: float,
    margin_rate: float,
    fee_per_contract: float,
    quantity: int,
    trend_period: int,
    atr_period: int,
    atr_multiplier: float,
    stop_loss: float | None,
    take_profit: float | None
) -> dict:
    symbol = symbol.upper()

    raw_dir = "data/derivatives/raw"
    processed_dir = "data/derivatives/processed"
    backtest_dir = "data/derivatives/backtest"
    report_dir = "reports"

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(backtest_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)

    raw_file = os.path.join(raw_dir, f"{symbol}.csv")
    signal_file = os.path.join(processed_dir, f"{symbol}_signals.csv")

    print("=" * 70)
    print(f"Running derivatives LONG/SHORT backtest for {symbol}")
    print("=" * 70)

    if collect or not os.path.exists(raw_file):
        collect_vietnam_stock_data(
            symbol=symbol,
            start=start,
            end=end,
            interval=interval,
            source=source,
            output_dir=raw_dir
        )
    else:
        print(f"Raw data already exists: {raw_file}")
        print("Skip data collection. Use --collect to download again.")

    df = pd.read_csv(raw_file)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    signals_df = calculate_buy_sell_atr(
        df,
        trend_period=trend_period,
        atr_period=atr_period,
        atr_multiplier=atr_multiplier,
        use_ema_smoother=False,
        src_ema_period=3
    )

    signals_df.to_csv(signal_file, index=False, encoding="utf-8-sig")
    print(f"Saved signal file: {signal_file}")

    trades_df, equity_df, summary = run_derivatives_backtest(
        signals_df,
        initial_cash=initial_cash,
        contract_multiplier=contract_multiplier,
        margin_rate=margin_rate,
        fee_per_contract=fee_per_contract,
        quantity=quantity,
        execute_next_open=True,
        stop_loss_pct=stop_loss,
        take_profit_pct=take_profit
    )

    save_derivatives_backtest_results(
        trades_df=trades_df,
        equity_df=equity_df,
        summary=summary,
        symbol=symbol,
        output_dir=backtest_dir
    )

    summary["symbol"] = symbol

    print(f"Finished derivatives backtest for {symbol}")
    print(f"Final equity: {summary['final_equity']:,.0f} VND")
    print(f"Profit: {summary['profit']:,.0f} VND")
    print(f"Return: {summary['return_pct']:.2f}%")
    print(f"Win rate: {summary['win_rate_pct']:.2f}%")

    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Derivatives LONG/SHORT backtest using Buy/Sell ATR signals"
    )

    parser.add_argument(
        "--symbols",
        nargs="+",
        default=["VN30F1M"],
        help="Derivative symbols, example: --symbols VN30F1M"
    )

    parser.add_argument(
        "--start",
        type=str,
        default="2025-01-01",
        help="Start date, format YYYY-MM-DD"
    )

    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help="End date, format YYYY-MM-DD"
    )

    parser.add_argument(
        "--interval",
        type=str,
        default="1D",
        help="Time interval, example: 1D"
    )

    parser.add_argument(
        "--source",
        type=str,
        default="KBS",
        help="Data source, example: KBS or VCI"
    )

    parser.add_argument(
        "--collect",
        action="store_true",
        help="Download data again and overwrite old raw CSV files"
    )

    parser.add_argument(
        "--initial-cash",
        type=float,
        default=100_000_000,
        help="Initial cash"
    )

    parser.add_argument(
        "--contract-multiplier",
        type=float,
        default=100_000,
        help="Contract multiplier"
    )

    parser.add_argument(
        "--margin-rate",
        type=float,
        default=0.15,
        help="Margin rate, example: 0.15"
    )

    parser.add_argument(
        "--fee-per-contract",
        type=float,
        default=3000,
        help="Fixed fee per contract per transaction"
    )

    parser.add_argument(
        "--quantity",
        type=int,
        default=1,
        help="Number of contracts per trade"
    )

    parser.add_argument(
        "--trend-period",
        type=int,
        default=20,
        help="Buy/Sell ATR trend period"
    )

    parser.add_argument(
        "--atr-period",
        type=int,
        default=5,
        help="ATR period"
    )

    parser.add_argument(
        "--atr-multiplier",
        type=float,
        default=0.5,
        help="ATR multiplier"
    )

    parser.add_argument(
        "--stop-loss",
        type=float,
        default=None,
        help="Stop loss, example: 0.03 means 3 percent"
    )

    parser.add_argument(
        "--take-profit",
        type=float,
        default=None,
        help="Take profit, example: 0.06 means 6 percent"
    )

    args = parser.parse_args()

    all_summaries = []

    for symbol in args.symbols:
        try:
            summary = run_single_derivatives_symbol(
                symbol=symbol,
                start=args.start,
                end=args.end,
                interval=args.interval,
                source=args.source,
                collect=args.collect,
                initial_cash=args.initial_cash,
                contract_multiplier=args.contract_multiplier,
                margin_rate=args.margin_rate,
                fee_per_contract=args.fee_per_contract,
                quantity=args.quantity,
                trend_period=args.trend_period,
                atr_period=args.atr_period,
                atr_multiplier=args.atr_multiplier,
                stop_loss=args.stop_loss,
                take_profit=args.take_profit
            )

            all_summaries.append(summary)

        except Exception as error:
            print(f"Error while backtesting {symbol}: {error}")

            all_summaries.append({
                "symbol": symbol.upper(),
                "initial_cash": args.initial_cash,
                "final_equity": None,
                "profit": None,
                "return_pct": None,
                "total_closed_trades": None,
                "wins": None,
                "losses": None,
                "win_rate_pct": None,
                "ending_cash": None,
                "ending_position": None,
                "error": str(error)
            })

    os.makedirs("reports", exist_ok=True)

    summary_df = pd.DataFrame(all_summaries)

    if "symbol" in summary_df.columns:
        cols = ["symbol"] + [col for col in summary_df.columns if col != "symbol"]
        summary_df = summary_df[cols]

    output_file = "reports/derivatives_summary.csv"
    summary_df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print("\n" + "=" * 70)
    print("DERIVATIVES BACKTEST COMPLETED")
    print("=" * 70)
    print(f"Saved summary report: {output_file}")
    print(summary_df)


if __name__ == "__main__":
    main()