import os
import argparse
from datetime import date

import pandas as pd


def collect_vietnam_stock_data(
    symbol: str = "FPT",
    start: str = "2020-01-01",
    end: str | None = None,
    interval: str = "1D",
    source: str = "KBS",
    output_dir: str = "data/raw"
) -> pd.DataFrame:
    """
    Thu thập dữ liệu OHLCV cho một cổ phiếu Việt Nam.

    Output:
    data/raw/FPT.csv

    Các cột sau khi xử lý:
    date, ticker, open, high, low, close, volume
    """

    if end is None:
        end = date.today().isoformat()

    try:
        from vnstock import Quote
    except ImportError as exc:
        raise ImportError(
            "Bạn chưa cài thư viện vnstock. Hãy chạy: pip install vnstock"
        ) from exc

    symbol = symbol.upper()

    print(f"Đang lấy dữ liệu {symbol} từ {start} đến {end}...")
    print(f"Nguồn dữ liệu: {source}")
    print(f"Khung thời gian: {interval}")

    quote = Quote(symbol=symbol, source=source)

    df = quote.history(
        start=start,
        end=end,
        interval=interval
    )

    if df is None or df.empty:
        raise ValueError(f"Không lấy được dữ liệu cho mã {symbol}")

    df = df.copy()

    # Chuẩn hóa tên cột
    if "time" in df.columns:
        df = df.rename(columns={"time": "date"})

    required_columns = ["date", "open", "high", "low", "close", "volume"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Thiếu cột dữ liệu: {col}")

    df = df[required_columns]

    # Thêm mã cổ phiếu
    df.insert(1, "ticker", symbol)

    # Ép kiểu dữ liệu
    df["date"] = pd.to_datetime(df["date"])

    numeric_columns = ["open", "high", "low", "close", "volume"]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Làm sạch dữ liệu
    df = df.dropna(subset=["date", "open", "high", "low", "close"])
    df = df.drop_duplicates(subset=["date"])
    df = df.sort_values("date")
    df = df.reset_index(drop=True)

    # Tạo thư mục nếu chưa có
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{symbol}.csv")

    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print("Lấy dữ liệu thành công.")
    print(f"Đã lưu file: {output_file}")
    print(df.tail())

    return df


def main():
    parser = argparse.ArgumentParser(
        description="Thu thập dữ liệu cổ phiếu Việt Nam cho algotrade"
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
        help="Ngày bắt đầu, định dạng YYYY-MM-DD"
    )

    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help="Ngày kết thúc, định dạng YYYY-MM-DD. Nếu bỏ trống sẽ lấy hôm nay"
    )

    parser.add_argument(
        "--interval",
        type=str,
        default="1D",
        help="Khung thời gian: 1D, 1W, 1M, 1H, 15m..."
    )

    parser.add_argument(
        "--source",
        type=str,
        default="KBS",
        help="Nguồn dữ liệu: KBS hoặc VCI"
    )

    args = parser.parse_args()

    collect_vietnam_stock_data(
        symbol=args.symbol,
        start=args.start,
        end=args.end,
        interval=args.interval,
        source=args.source,
        output_dir="data/raw"
    )


if __name__ == "__main__":
    main()