import MetaTrader5 as mt5

def orderbook_analysis(symbol):

    book = mt5.market_book_get(symbol)

    buy_volume = 0
    sell_volume = 0

    if book:

        for order in book:

            if order.type == 1:
                buy_volume += order.volume

            if order.type == 2:
                sell_volume += order.volume

    return buy_volume, sell_volume