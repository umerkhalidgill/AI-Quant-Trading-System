import MetaTrader5 as mt5

def calculate_lot():

    account = mt5.account_info()

    balance = account.balance

    risk = balance * 0.01

    lot = round(risk / 1000,2)

    if lot < 0.01:
        lot = 0.01

    if lot > 1.0:
        lot = 1.0

    return lot