import os
import pandas as pd

from portfolio import Portfolio


def get_date_column(df: pd.DataFrame) -> str:
    if "date" in df.columns:
        return "date"

    if "timestamp" in df.columns:
        return "timestamp"

    raise ValueError("DataFrame cần có cột 'date' hoặc 'timestamp'.")


def run_backtest(
    df: pd.DataFrame,
    initial_cash: float = 100_000_000,
    lot_size: int = 100,
    fee_rate: float = 0.001,
    sell_tax_rate: float = 0.001,
    allocation_pct: float = 1.0,
    execute_next_open: bool = True,
    stop_loss_pct: float | None = None,
    take_profit_pct: float | None = None
):
    """
    Backtest chiến lược Buy/Sell ATR cho một cổ phiếu.

    Logic:
    - BUY  -> mua nếu chưa có cổ phiếu.
    - SELL -> bán nếu đang giữ cổ phiếu.
    - HOLD -> không làm gì.

    Nếu execute_next_open=True:
    - Tín hiệu xuất hiện ở ngày hôm nay.
    - Lệnh sẽ được khớp ở giá open của ngày tiếp theo.
    """

    df = df.copy()

    required_columns = ["open", "high", "low", "close", "signal"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Thiếu cột bắt buộc: {col}")

    date_col = get_date_column(df)

    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).reset_index(drop=True)

    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    portfolio = Portfolio(
        initial_cash=initial_cash,
        lot_size=lot_size,
        fee_rate=fee_rate,
        sell_tax_rate=sell_tax_rate
    )

    if len(df) == 0:
        raise ValueError("Dữ liệu rỗng, không thể backtest.")

    portfolio.mark_to_market(df.loc[0, date_col], df.loc[0, "close"])

    last_index = len(df) - 1

    for i in range(last_index):
        current_row = df.loc[i]
        next_row = df.loc[i + 1]

        signal = str(current_row["signal"]).upper()

        if execute_next_open:
            trade_date = next_row[date_col]
            trade_price = next_row["open"]

            if pd.isna(trade_price):
                trade_price = next_row["close"]
        else:
            trade_date = current_row[date_col]
            trade_price = current_row["close"]

        # Kiểm tra Stop Loss / Take Profit nếu đang có vị thế
        exited_by_risk_rule = False

        if portfolio.shares > 0 and portfolio.avg_price is not None:
            if stop_loss_pct is not None:
                stop_price = portfolio.avg_price * (1 - stop_loss_pct)

                if next_row["low"] <= stop_price:
                    portfolio.sell(
                        date=trade_date,
                        price=stop_price,
                        reason="STOP_LOSS"
                    )
                    exited_by_risk_rule = True

            if not exited_by_risk_rule and take_profit_pct is not None:
                take_profit_price = portfolio.avg_price * (1 + take_profit_pct)

                if next_row["high"] >= take_profit_price:
                    portfolio.sell(
                        date=trade_date,
                        price=take_profit_price,
                        reason="TAKE_PROFIT"
                    )
                    exited_by_risk_rule = True

        # Xử lý tín hiệu BUY / SELL
        if not exited_by_risk_rule:
            if signal == "BUY" and portfolio.shares == 0:
                portfolio.buy(
                    date=trade_date,
                    price=trade_price,
                    allocation_pct=allocation_pct,
                    reason="BUY_SIGNAL"
                )

            elif signal == "SELL" and portfolio.shares > 0:
                portfolio.sell(
                    date=trade_date,
                    price=trade_price,
                    reason="SELL_SIGNAL"
                )

        portfolio.mark_to_market(next_row[date_col], next_row["close"])

    trades_df = pd.DataFrame(portfolio.trades)
    equity_df = pd.DataFrame(portfolio.equity_curve)

    final_value = portfolio.total_value(df.loc[last_index, "close"])
    profit = final_value - initial_cash
    return_pct = profit / initial_cash * 100

    if not trades_df.empty and "action" in trades_df.columns:
        sell_trades = trades_df[trades_df["action"] == "SELL"]
        total_trades = len(sell_trades)
        wins = len(sell_trades[sell_trades["pnl"] > 0])
        losses = len(sell_trades[sell_trades["pnl"] <= 0])
        win_rate = wins / total_trades * 100 if total_trades > 0 else 0
    else:
        total_trades = 0
        wins = 0
        losses = 0
        win_rate = 0

    summary = {
        "initial_cash": initial_cash,
        "final_value": final_value,
        "profit": profit,
        "return_pct": return_pct,
        "total_closed_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate_pct": win_rate,
        "ending_cash": portfolio.cash,
        "ending_shares": portfolio.shares
    }

    return trades_df, equity_df, summary


def save_backtest_results(
    trades_df: pd.DataFrame,
    equity_df: pd.DataFrame,
    summary: dict,
    symbol: str = "FPT",
    output_dir: str = "data/backtest"
):
    os.makedirs(output_dir, exist_ok=True)

    trades_file = os.path.join(output_dir, f"{symbol}_trades.csv")
    equity_file = os.path.join(output_dir, f"{symbol}_equity.csv")
    summary_file = os.path.join(output_dir, f"{symbol}_summary.csv")

    trades_df.to_csv(trades_file, index=False, encoding="utf-8-sig")
    equity_df.to_csv(equity_file, index=False, encoding="utf-8-sig")
    pd.DataFrame([summary]).to_csv(summary_file, index=False, encoding="utf-8-sig")

    print(f"Đã lưu lịch sử giao dịch: {trades_file}")
    print(f"Đã lưu equity curve: {equity_file}")
    print(f"Đã lưu tổng kết backtest: {summary_file}")


if __name__ == "__main__":
    symbol = "FPT"
    input_file = f"data/processed/{symbol}_signals.csv"

    df = pd.read_csv(input_file)

    trades_df, equity_df, summary = run_backtest(
        df,
        initial_cash=100_000_000,
        lot_size=100,
        fee_rate=0.001,
        sell_tax_rate=0.001,
        allocation_pct=1.0,
        execute_next_open=True,
        stop_loss_pct=None,
        take_profit_pct=None
    )

    save_backtest_results(
        trades_df=trades_df,
        equity_df=equity_df,
        summary=summary,
        symbol=symbol
    )

    print("Kết quả backtest:")
    for key, value in summary.items():
        print(f"{key}: {value}")