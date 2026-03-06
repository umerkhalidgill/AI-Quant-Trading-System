import random

def strategy_optimizer():

    ema_fast = random.randint(20,50)

    ema_slow = random.randint(100,200)

    atr_filter = random.uniform(1.0,4.0)

    return ema_fast, ema_slow, atr_filter