import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import xgboost as xgb
import lightgbm as lgb


rf_model = RandomForestClassifier()
gb_model = GradientBoostingClassifier()
xgb_model = xgb.XGBClassifier()
lgb_model = lgb.LGBMClassifier()


def train_model(df):

    df["return"] = df["close"].pct_change()

    df["target"] = (df["return"].shift(-1) > 0).astype(int)

    df = df.dropna()

    X = df[["close","ema50","ema200"]]

    y = df["target"]

    rf_model.fit(X,y)

    gb_model.fit(X,y)

    xgb_model.fit(X,y)

    lgb_model.fit(X,y)


def predict_signal(df):

    X = df[["close","ema50","ema200"]].tail(1)

    p1 = rf_model.predict(X)[0]

    p2 = gb_model.predict(X)[0]

    p3 = xgb_model.predict(X)[0]

    p4 = lgb_model.predict(X)[0]

    votes = p1+p2+p3+p4

    if votes >= 3:
        return "buy"

    else:
        return "sell"


def probability_score(df):

    X = df[["close","ema50","ema200"]].tail(1)

    p1 = rf_model.predict_proba(X)[0][1]

    p2 = gb_model.predict_proba(X)[0][1]

    p3 = xgb_model.predict_proba(X)[0][1]

    p4 = lgb_model.predict_proba(X)[0][1]

    prob = (p1+p2+p3+p4)/4

    return prob
