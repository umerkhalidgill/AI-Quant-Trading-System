import MetaTrader5 as mt5
import pandas as pd

def liquidity_heatmap(symbol):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 500)

    df = pd.DataFrame(rates)

    df["volume_zone"] = df["tick_volume"]

    zones = df.sort_values("volume_zone", ascending=False).head(10)

    return zones[["high","low","volume_zone"]]