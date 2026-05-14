import os
import pandas as pd

from derivatives_portfolio import DerivativesPortfolio


def get_date_column(df: pd.DataFrame) -> str:
    if "date" in df.columns:
        return "date"

    if "timestamp" in df.columns:
        return "timestamp"

    raise ValueError("DataFrame cần có cột 'date' hoặc 'timestamp'.")


def run_derivatives_backtest(
    df: pd.DataFrame,
    initial_cash: float = 100_000_000,
    contract_multiplier: float = 100_000,
    margin_rate: float = 0.15,
    fee_per_contract: float = 3000,
    quantity: int = 1,
    execute_next_open: bool = True,
    stop_loss_pct: float | None = None,
    take_profit_pct: float | None = None
):
    """
    Backtest phái sinh theo logic LONG / SHORT.

    BUY:
        - Nếu đang SHORT -> đóng SHORT rồi mở LONG
        - Nếu đang không có vị thế -> mở LONG

    SELL:
        - Nếu đang LONG -> đóng LONG rồi mở SHORT
        - Nếu đang không có vị thế -> mở SHORT
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

    portfolio = DerivativesPortfolio(
        initial_cash=initial_cash,
        contract_multiplier=contract_multiplier,
        margin_rate=margin_rate,
        fee_per_contract=fee_per_contract
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

        exited_by_risk_rule = False

        # Risk management cho LONG
        if portfolio.position > 0 and portfolio.entry_price is not None:
            if stop_loss_pct is not None:
                stop_price = portfolio.entry_price * (1 - stop_loss_pct)

                if next_row["low"] <= stop_price:
                    portfolio.close_position(
                        date=trade_date,
                        price=stop_price,
                        reason="LONG_STOP_LOSS"
                    )
                    exited_by_risk_rule = True

            if not exited_by_risk_rule and take_profit_pct is not None:
                take_profit_price = portfolio.entry_price * (1 + take_profit_pct)

                if next_row["high"] >= take_profit_price:
                    portfolio.close_position(
                        date=trade_date,
                        price=take_profit_price,
                        reason="LONG_TAKE_PROFIT"
                    )
                    exited_by_risk_rule = True

        # Risk management cho SHORT
        elif portfolio.position < 0 and portfolio.entry_price is not None:
            if stop_loss_pct is not None:
                stop_price = portfolio.entry_price * (1 + stop_loss_pct)

                if next_row["high"] >= stop_price:
                    portfolio.close_position(
                        date=trade_date,
                        price=stop_price,
                        reason="SHORT_STOP_LOSS"
                    )
                    exited_by_risk_rule = True

            if not exited_by_risk_rule and take_profit_pct is not None:
                take_profit_price = portfolio.entry_price * (1 - take_profit_pct)

                if next_row["low"] <= take_profit_price:
                    portfolio.close_position(
                        date=trade_date,
                        price=take_profit_price,
                        reason="SHORT_TAKE_PROFIT"
                    )
                    exited_by_risk_rule = True

        if not exited_by_risk_rule:
            # BUY signal -> LONG
            if signal == "BUY":
                if portfolio.position < 0:
                    portfolio.close_position(
                        date=trade_date,
                        price=trade_price,
                        reason="CLOSE_SHORT_BY_BUY_SIGNAL"
                    )
                    portfolio.open_long(
                        date=trade_date,
                        price=trade_price,
                        quantity=quantity,
                        reason="OPEN_LONG_BY_BUY_SIGNAL"
                    )

                elif portfolio.position == 0:
                    portfolio.open_long(
                        date=trade_date,
                        price=trade_price,
                        quantity=quantity,
                        reason="OPEN_LONG_BY_BUY_SIGNAL"
                    )

            # SELL signal -> SHORT
            elif signal == "SELL":
                if portfolio.position > 0:
                    portfolio.close_position(
                        date=trade_date,
                        price=trade_price,
                        reason="CLOSE_LONG_BY_SELL_SIGNAL"
                    )
                    portfolio.open_short(
                        date=trade_date,
                        price=trade_price,
                        quantity=quantity,
                        reason="OPEN_SHORT_BY_SELL_SIGNAL"
                    )

                elif portfolio.position == 0:
                    portfolio.open_short(
                        date=trade_date,
                        price=trade_price,
                        quantity=quantity,
                        reason="OPEN_SHORT_BY_SELL_SIGNAL"
                    )

        portfolio.mark_to_market(next_row[date_col], next_row["close"])

    # Đóng vị thế cuối kỳ để chốt PnL
    if portfolio.position != 0:
        last_row = df.loc[last_index]
        portfolio.close_position(
            date=last_row[date_col],
            price=last_row["close"],
            reason="FORCE_CLOSE_END_OF_BACKTEST"
        )
        portfolio.mark_to_market(last_row[date_col], last_row["close"])

    trades_df = pd.DataFrame(portfolio.trades)
    equity_df = pd.DataFrame(portfolio.equity_curve)

    final_equity = portfolio.cash
    profit = final_equity - initial_cash
    return_pct = profit / initial_cash * 100

    if not trades_df.empty and "realized_pnl" in trades_df.columns:
        closed_trades = trades_df[
            trades_df["action"].isin(["CLOSE_LONG", "CLOSE_SHORT"])
        ]

        total_closed_trades = len(closed_trades)
        wins = len(closed_trades[closed_trades["realized_pnl"] > 0])
        losses = len(closed_trades[closed_trades["realized_pnl"] <= 0])
        win_rate = wins / total_closed_trades * 100 if total_closed_trades > 0 else 0
    else:
        total_closed_trades = 0
        wins = 0
        losses = 0
        win_rate = 0

    summary = {
        "initial_cash": initial_cash,
        "final_equity": final_equity,
        "profit": profit,
        "return_pct": return_pct,
        "total_closed_trades": total_closed_trades,
        "wins": wins,
        "losses": losses,
        "win_rate_pct": win_rate,
        "ending_cash": portfolio.cash,
        "ending_position": portfolio.position
    }

    return trades_df, equity_df, summary


def save_derivatives_backtest_results(
    trades_df: pd.DataFrame,
    equity_df: pd.DataFrame,
    summary: dict,
    symbol: str,
    output_dir: str = "data/derivatives/backtest"
):
    os.makedirs(output_dir, exist_ok=True)

    trades_file = os.path.join(output_dir, f"{symbol}_derivatives_trades.csv")
    equity_file = os.path.join(output_dir, f"{symbol}_derivatives_equity.csv")
    summary_file = os.path.join(output_dir, f"{symbol}_derivatives_summary.csv")

    trades_df.to_csv(trades_file, index=False, encoding="utf-8-sig")
    equity_df.to_csv(equity_file, index=False, encoding="utf-8-sig")
    pd.DataFrame([summary]).to_csv(summary_file, index=False, encoding="utf-8-sig")

    print(f"Saved trades: {trades_file}")
    print(f"Saved equity curve: {equity_file}")
    print(f"Saved summary: {summary_file}")