import MetaTrader5 as mt5
import pandas as pd
import time
import random
from datetime import datetime

from ai_model import train_model, predict_signal, probability_score
from structure import market_structure, liquidity_sweep, order_block, smart_money_signal
from heatmap import liquidity_heatmap
from orderbook import orderbook_analysis
from risk import calculate_lot
from news_filter import news_filter

mt5.initialize()

symbols = [
"XAUUSD",
"EURUSD",
"GBPUSD",
"USDJPY",
"AUDUSD",
"USDCAD",
"USDCHF",
"NZDUSD"
]


def get_data(symbol):

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 500)

    df = pd.DataFrame(rates)

    df["ema50"] = df["close"].ewm(span=50).mean()

    df["ema200"] = df["close"].ewm(span=200).mean()

    df["atr"] = (df["high"] - df["low"]).rolling(14).mean()

    return df


def genetic_strategy():

    ema_fast = random.randint(10,50)

    ema_slow = random.randint(100,250)

    atr_filter = random.uniform(1.0,4.0)

    return ema_fast, ema_slow, atr_filter


def institutional_liquidity(df):

    df["volume_spike"] = df["tick_volume"].rolling(20).mean()

    last_volume = df["tick_volume"].iloc[-1]

    avg_volume = df["volume_spike"].iloc[-1]

    if last_volume > avg_volume * 1.5:

        return "institutional"

    return None


def log_trade(symbol,trade_type,price,profit):

    data = {

        "time":[datetime.now()],

        "symbol":[symbol],

        "type":[trade_type],

        "price":[price],

        "profit":[profit]

    }

    df = pd.DataFrame(data)

    df.to_csv("trade_log.csv",mode="a",header=False,index=False)


def open_trade(symbol,direction):

    tick = mt5.symbol_info_tick(symbol)

    price = tick.ask if direction=="buy" else tick.bid

    lot = calculate_lot()

    request = {

        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY if direction=="buy" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": 10,
        "magic": 100,
        "comment": "SELF_LEARNING_AI_BOT",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC

    }

    result = mt5.order_send(request)

    print("TRADE RESULT:",result)

    log_trade(symbol,direction,price,0)


def self_learning():

    try:

        df = pd.read_csv("trade_log.csv")

        win_rate = (df["profit"] > 0).mean()

        print("AI Learning — Win Rate:",win_rate)

        if win_rate < 0.4:

            print("Strategy adjustment triggered")

    except:

        print("Learning data not ready")


while True:

    if news_filter() == False:

        print("News filter active")

        time.sleep(60)

        continue


    ema_fast, ema_slow, atr_filter = genetic_strategy()

    self_learning()


    for symbol in symbols:

        df = get_data(symbol)

        train_model(df)

        ai_signal = predict_signal(df)

        prob = probability_score(df)

        structure = market_structure(df)

        sweep = liquidity_sweep(df)

        ob = order_block(df)

        smc = smart_money_signal(df)

        liq = institutional_liquidity(df)

        buy_vol, sell_vol = orderbook_analysis(symbol)

        heatmap = liquidity_heatmap(symbol)


        print("------")

        print("Symbol:",symbol)

        print("AI:",ai_signal)

        print("Probability:",prob)

        print("Structure:",structure)

        print("Sweep:",sweep)

        print("OrderBlock:",ob)

        print("SmartMoney:",smc)

        print("Liquidity:",liq)

        print("OrderBook:",buy_vol,sell_vol)

        print("Heatmap:")

        print(heatmap)


        if ai_signal=="buy" and structure=="buy" and smc=="buy" and prob > 0.65 and liq=="institutional":

            open_trade(symbol,"buy")


        elif ai_signal=="sell" and structure=="sell" and smc=="sell" and prob < 0.35 and liq=="institutional":

            open_trade(symbol,"sell")


        else:

            print("No trade:",symbol)


    time.sleep(60)
