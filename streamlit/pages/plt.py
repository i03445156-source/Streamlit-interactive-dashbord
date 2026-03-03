
import pandas as pd 
import streamlit as st
import seaborn 
import yfinance as yf


st.title("실시간 전광판")

tickers = ["005930.KS",'000660.KS','005380.KS','005935.KS','373220.KS',
           '402340.KS','207940.KS','000270.KS','034020.KS','329180.KS',
           '012450.KS','028260.KS','105560.KS','068270.KS','012330.KS',
           '032830.KS','055550.KS','042660.KS','010130.KS','006800.KS']

data = yf.download(tickers, period='1d',interval='1m')
latest = data['Close'].iloc[-1]
previous = data['Close'].iloc[-2]



cols = st.columns(len(tickers))

per_row = 5

for start in range(0,len(tickers),per_row):
    row = tickers[start:start + per_row]
    cols = st.columns(len(row))

    for i, tkr in enumerate(row):
        price = latest.get(tkr,None)
        prev = previous.get(tkr,None)

        if price is None or prev is None or prev ==0:
            cols[i].metric(label = tkr, value="N/A",delta = "N/A")
        else:
            change = (price - prev)/prev*100
            cols[i].metric(
                label=tkr,
                value = f"{float(price):,.2f}",
                delta=f"{float(change):.2f}%"
            )


df = pd.DataFrame({
        "ticker": tickers,
        "price":[latest.get(t,None) for t in tickers],
        "prev": [ previous.get(t,None) for t in tickers],
})

df['change_pct'] = (df["price"]- df['prev'])/ df['prev']*100

st.dataframe(df[["ticker","price","change_pct"]], use_container_width = True)

st.divider()
