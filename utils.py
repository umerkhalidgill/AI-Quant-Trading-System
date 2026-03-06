def log_trade(symbol, trade_type, price, profit):

    with open("trade_log.csv","a") as f:

        f.write(f"{symbol},{trade_type},{price},{profit}\n")
