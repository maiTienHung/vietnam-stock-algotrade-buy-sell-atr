import os
import numpy as np
import pandas as pd


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def calculate_atr(df: pd.DataFrame, period: int = 5) -> pd.Series:
    high = df["high"]
    low = df["low"]
    close = df["close"]
    prev_close = close.shift(1)

    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()

    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # ATR cơ bản
    atr = true_range.rolling(window=period).mean()

    return atr


def calculate_buy_sell_atr(
    df: pd.DataFrame,
    trend_period: int = 20,
    atr_period: int = 5,
    atr_multiplier: float = 0.5,
    use_ema_smoother: bool = False,
    src_ema_period: int = 3
) -> pd.DataFrame:
    """
    Buy/Sell ATR Type A.

    Logic chính:
    BUY  khi giá cắt lên hoặc nằm trên upper_band.
    SELL khi giá cắt xuống hoặc nằm dưới lower_band.

    upper_band = middle + epsilon
    lower_band = middle - epsilon

    middle = (highest + lowest) / 2
    epsilon = ATR trước đó * atr_multiplier
    """

    df = df.copy()

    required_columns = ["open", "high", "low", "close"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Thiếu cột bắt buộc: {col}")

    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if "volume" in df.columns:
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

    # Source mặc định là close
    df["src"] = df["close"]

    # Nếu muốn làm mượt source bằng EMA
    if use_ema_smoother:
        df["src"] = ema(df["src"], src_ema_period)

    # Highest và Lowest trong trend_period nến
    df["highest"] = df["src"].rolling(window=trend_period).max()
    df["lowest"] = df["src"].rolling(window=trend_period).min()

    # Đường giữa
    df["middle"] = (df["highest"] + df["lowest"]) / 2

    # ATR
    df["atr"] = calculate_atr(df, atr_period)

    # ATR của nến trước
    df["atr_prev"] = df["atr"].shift(1)

    # Khoảng đệm ATR
    df["epsilon"] = df["atr_prev"] * atr_multiplier

    # Band trên và band dưới
    df["upper_band"] = df["middle"] + df["epsilon"]
    df["lower_band"] = df["middle"] - df["epsilon"]

    df["trend_state"] = None
    df["signal"] = "HOLD"

    last_state = None

    for i in range(len(df)):
        src = df.loc[i, "src"]
        upper = df.loc[i, "upper_band"]
        lower = df.loc[i, "lower_band"]

        if pd.isna(src) or pd.isna(upper) or pd.isna(lower):
            continue

        prev_src = df.loc[i - 1, "src"] if i > 0 else np.nan
        prev_upper = df.loc[i - 1, "upper_band"] if i > 0 else np.nan
        prev_lower = df.loc[i - 1, "lower_band"] if i > 0 else np.nan

        # Type A:
        # BUY khi src crossover upper_band
        cross_up = (
            i > 0
            and not pd.isna(prev_src)
            and not pd.isna(prev_upper)
            and prev_src <= prev_upper
            and src > upper
        )

        # SELL khi src crossunder lower_band
        cross_down = (
            i > 0
            and not pd.isna(prev_src)
            and not pd.isna(prev_lower)
            and prev_src >= prev_lower
            and src < lower
        )

        
        # change_up = crossover(...) or src > upper_band
        # change_down = crossunder(...) or src < lower_band
        change_up = cross_up or src > upper
        change_down = cross_down or src < lower

        if change_up:
            current_state = "B"
        elif change_down:
            current_state = "S"
        else:
            current_state = last_state

        # Chỉ báo BUY một lần khi đổi từ trạng thái khác sang B
        if current_state == "B" and last_state != "B":
            df.loc[i, "signal"] = "BUY"

        # Chỉ báo SELL một lần khi đổi từ trạng thái khác sang S
        elif current_state == "S" and last_state != "S":
            df.loc[i, "signal"] = "SELL"

        else:
            df.loc[i, "signal"] = "HOLD"

        df.loc[i, "trend_state"] = current_state
        last_state = current_state

    return df


if __name__ == "__main__":
    input_file = "data/raw/FPT.csv"
    output_file = "data/processed/FPT_signals.csv"

    os.makedirs("data/processed", exist_ok=True)

    df = pd.read_csv(input_file)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    result = calculate_buy_sell_atr(
        df,
        trend_period=20,
        atr_period=5,
        atr_multiplier=0.5,
        use_ema_smoother=False,
        src_ema_period=3
    )

    result.to_csv(output_file, index=False)

    print("Đã tính xong tín hiệu Buy/Sell ATR Type A.")
    print(f"File kết quả: {output_file}")

    show_columns = []

    for col in [
        "date",
        "timestamp",
        "close",
        "middle",
        "upper_band",
        "lower_band",
        "trend_state",
        "signal"
    ]:
        if col in result.columns:
            show_columns.append(col)

    print(result[show_columns].tail(20))