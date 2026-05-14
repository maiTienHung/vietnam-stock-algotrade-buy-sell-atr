import os
import argparse
import pandas as pd

from collect_data import collect_vietnam_stock_data
from buy_sell_atr import calculate_buy_sell_atr
from backtest_engine import run_backtest, save_backtest_results


def main():
    parser = argparse.ArgumentParser(
        description="Algotrade cơ bản cho một cổ phiếu Việt Nam dùng Buy/Sell ATR"
    )

    parser.add_argument(
        "--symbol",
        type=str,
        default="FPT",
        help="Mã cổ phiếu, ví dụ: FPT, HPG, VNM"
    )

    parser.add_argument(
        "--start",
        type=str,
        default="2020-01-01",
        help="Ngày bắt đầu lấy dữ liệu, định dạng YYYY-MM-DD"
    )

    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help="Ngày kết thúc, định dạng YYYY-MM-DD"
    )

    parser.add_argument(
        "--interval",
        type=str,
        default="1D",
        help="Khung thời gian, ví dụ: 1D"
    )

    parser.add_argument(
        "--source",
        type=str,
        default="KBS",
        help="Nguồn dữ liệu vnstock, ví dụ: KBS hoặc VCI"
    )

    parser.add_argument(
        "--collect",
        action="store_true",
        help="Bật tùy chọn này nếu muốn tải lại dữ liệu mới"
    )

    parser.add_argument(
        "--initial-cash",
        type=float,
        default=100_000_000,
        help="Vốn ban đầu"
    )

    parser.add_argument(
        "--lot-size",
        type=int,
        default=100,
        help="Số cổ phiếu tối thiểu mỗi lô"
    )

    parser.add_argument(
        "--fee-rate",
        type=float,
        default=0.001,
        help="Phí giao dịch, ví dụ 0.001 = 0.1%%"
    )

    parser.add_argument(
        "--sell-tax-rate",
        type=float,
        default=0.001,
        help="Thuế/phí khi bán, ví dụ 0.001 = 0.1%%"
    )

    parser.add_argument(
        "--trend-period",
        type=int,
        default=20,
        help="Trend Period của Buy/Sell ATR"
    )

    parser.add_argument(
        "--atr-period",
        type=int,
        default=5,
        help="ATR Period"
    )

    parser.add_argument(
        "--atr-multiplier",
        type=float,
        default=0.5,
        help="ATR Multiplier"
    )

    parser.add_argument(
        "--stop-loss",
        type=float,
        default=None,
        help="Stop loss theo phần trăm, ví dụ 0.07 = 7%%. Bỏ trống nếu không dùng."
    )

    parser.add_argument(
        "--take-profit",
        type=float,
        default=None,
        help="Take profit theo phần trăm, ví dụ 0.15 = 15%%. Bỏ trống nếu không dùng."
    )

    args = parser.parse_args()

    symbol = args.symbol.upper()

    raw_dir = "data/raw"
    processed_dir = "data/processed"
    backtest_dir = "data/backtest"
    report_dir = "reports"

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(backtest_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)

    raw_file = os.path.join(raw_dir, f"{symbol}.csv")
    signal_file = os.path.join(processed_dir, f"{symbol}_signals.csv")

    # Bước 1: Thu thập dữ liệu
    if args.collect or not os.path.exists(raw_file):
        collect_vietnam_stock_data(
            symbol=symbol,
            start=args.start,
            end=args.end,
            interval=args.interval,
            source=args.source,
            output_dir=raw_dir
        )
    else:
        print(f"Đã có dữ liệu raw: {raw_file}")
        print("Bỏ qua bước tải dữ liệu. Nếu muốn tải lại, thêm --collect")

    # Bước 2: Đọc dữ liệu raw
    df = pd.read_csv(raw_file)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    # Bước 3: Tính tín hiệu Buy/Sell ATR Type A
    signals_df = calculate_buy_sell_atr(
        df,
        trend_period=args.trend_period,
        atr_period=args.atr_period,
        atr_multiplier=args.atr_multiplier,
        use_ema_smoother=False,
        src_ema_period=3
    )

    signals_df.to_csv(signal_file, index=False, encoding="utf-8-sig")

    print(f"Đã lưu file tín hiệu: {signal_file}")

    signal_count = signals_df["signal"].value_counts()
    print("Số lượng tín hiệu:")
    print(signal_count)

    # Bước 4: Backtest
    trades_df, equity_df, summary = run_backtest(
        signals_df,
        initial_cash=args.initial_cash,
        lot_size=args.lot_size,
        fee_rate=args.fee_rate,
        sell_tax_rate=args.sell_tax_rate,
        allocation_pct=1.0,
        execute_next_open=True,
        stop_loss_pct=args.stop_loss,
        take_profit_pct=args.take_profit
    )

    save_backtest_results(
        trades_df=trades_df,
        equity_df=equity_df,
        summary=summary,
        symbol=symbol,
        output_dir=backtest_dir
    )

    # Bước 5: Lưu báo cáo tổng hợp
    report_file = os.path.join(report_dir, f"{symbol}_report.csv")
    pd.DataFrame([summary]).to_csv(report_file, index=False, encoding="utf-8-sig")

    print(f"Đã lưu báo cáo: {report_file}")

    print("\n===== KẾT QUẢ BACKTEST =====")
    print(f"Mã cổ phiếu: {symbol}")
    print(f"Vốn ban đầu: {summary['initial_cash']:,.0f} VND")
    print(f"Giá trị cuối kỳ: {summary['final_value']:,.0f} VND")
    print(f"Lãi/Lỗ: {summary['profit']:,.0f} VND")
    print(f"Tỷ suất lợi nhuận: {summary['return_pct']:.2f}%")
    print(f"Số lệnh đã đóng: {summary['total_closed_trades']}")
    print(f"Số lệnh thắng: {summary['wins']}")
    print(f"Số lệnh thua: {summary['losses']}")
    print(f"Win rate: {summary['win_rate_pct']:.2f}%")
    print(f"Tiền mặt cuối kỳ: {summary['ending_cash']:,.0f} VND")
    print(f"Cổ phiếu còn giữ: {summary['ending_shares']}")


if __name__ == "__main__":
    main()