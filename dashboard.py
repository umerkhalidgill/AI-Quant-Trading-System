import streamlit as st
import pandas as pd

st.title("Quant AI Trading Control Panel")

run_bot = st.button("Start Bot")

stop_bot = st.button("Stop Bot")

try:

    df = pd.read_csv("trade_log.csv")

    st.subheader("Recent Trades")

    st.dataframe(df.tail(20))

    st.metric("Total Trades",len(df))

except:

    st.write("No trades yet")