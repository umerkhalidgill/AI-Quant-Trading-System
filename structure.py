
def market_structure(df):

    prev_high = df["high"].iloc[-2]
    prev_low = df["low"].iloc[-2]

    last_close = df["close"].iloc[-1]

    if last_close > prev_high:
        return "buy"

    if last_close < prev_low:
        return "sell"

    return None


def liquidity_sweep(df):

    prev_high = df["high"].iloc[-2]
    prev_low = df["low"].iloc[-2]

    last_high = df["high"].iloc[-1]
    last_low = df["low"].iloc[-1]
    last_close = df["close"].iloc[-1]

    if last_high > prev_high and last_close < prev_high:
        return "sell"

    if last_low < prev_low and last_close > prev_low:
        return "buy"

    return None


def order_block(df):

    candle = df.iloc[-2]

    body = abs(candle["close"] - candle["open"])

    avg = (df["close"] - df["open"]).abs().rolling(20).mean().iloc[-1]

    if body > avg:

        if candle["close"] < candle["open"]:
            return "bullish"

        else:
            return "bearish"

    return None


def smart_money_signal(df):

    prev_high = df["high"].iloc[-3]
    prev_low = df["low"].iloc[-3]

    last_close = df["close"].iloc[-1]

    if last_close > prev_high:
        return "buy"

    if last_close < prev_low:
        return "sell"

    return None
