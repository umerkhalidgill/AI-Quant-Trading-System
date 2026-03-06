import MetaTrader5 as mt5
import pandas as pd

symbol = "XAUUSD"

rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 2000)

df = pd.DataFrame(rates)

profit = 0

for i in range(200,len(df)):

    if df["close"].iloc[i] > df["close"].iloc[i-1]:
        profit += 1
    else:
        profit -= 1

print("Backtest result:",profit)