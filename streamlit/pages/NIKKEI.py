import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="시장 트리맵", layout="wide")
st.title("일본시장 시가총액 트리맵")


tickers = [
    "7203.T", "6758.T", "6857.T", "9984.T", "8035.T", "4502.T", "6098.T", "4063.T", "6501.T", "8058.T",
    "8306.T", "7267.T", "6954.T", "6367.T", "9432.T", "9433.T", "8001.T", "6981.T", "4519.T", "7741.T",
    "4901.T", "8031.T", "6503.T", "4568.T", "6273.T", "6146.T", "6920.T", "7733.T", "7974.T", "8801.T",
    "8316.T", "8002.T", "6301.T", "6723.T", "2502.T", "6702.T", "9022.T", "8766.T", "9101.T", "4503.T",
    "2802.T", "9613.T", "8802.T", "8411.T", "6594.T", "9201.T", "7269.T", "1925.T", "1605.T", "3407.T",
    "6762.T", "5108.T", "8053.T", "4661.T", "6861.T", "9020.T", "5401.T", "4452.T", "6902.T", "1801.T",
    "2914.T", "7201.T", "9503.T", "9104.T", "3382.T", "6326.T", "1802.T", "4324.T", "4911.T", "6701.T",
    "7270.T", "9501.T", "8267.T", "1803.T", "9107.T", "4523.T", "5802.T", "7011.T", "6473.T", "6752.T",
    "9021.T", "1928.T", "3402.T", "5233.T", "4507.T", "9735.T", "7013.T", "6506.T", "4151.T", "2432.T",
    "3861.T", "4021.T", "4543.T", "5713.T", "6305.T", "7751.T", "8604.T", "9531.T", "9766.T", "2267.T"
]
@st.cache_data(ttl=300)
def fetch_snapshot(tickers):
    rows = []
    for tkr in tickers:
        t = yf.Ticker(tkr)
        info = t.info
        hist = t.history(period = "2d",interval = "1d")

        if hist is None or hist.empty or len(hist) <2:
            prev_close = None
            last_close = None
            chg_pct = None 
        else:
            prev_close = float(hist["Close"].iloc[-2])
            last_close = float(hist['Close'].iloc[-1])
            chg_pct = (last_close - prev_close)/ prev_close * 100 if prev_close !=0 else None

        rows.append({
                "ticker":tkr,
                "name":info.get("shortName") or info.get("longName") or tkr,
                "sector": info.get("sector") or "Unknown",
                "marketCap": info.get("marketCap") or 0,
                "price": last_close,
                "change_pct" : chg_pct,
                "industry": info.get("industry") or "Unknown",
                
            })
    return pd.DataFrame(rows)
       

df = fetch_snapshot(tickers)


fig = px.treemap(
    df,
    path = ['sector','industry','ticker'],
    values = "marketCap",
    color = 'change_pct',
    color_continuous_scale = 'RdYlGn',
    hover_data = {"name": True, "price": True, "marketCap": True, "change_pct": True},
    custom_data=["change_pct"]
)

fig.update_traces(
    texttemplate ="<b>%{label}</b><br>%{customdata[0]:.2f}%",
    textfont_size = 18
)

fig.update_layout(margin = dict(t=10, l=10, r=10, b=10))
st.plotly_chart(fig, use_container_width = True)

st.dataframe(df[["ticker","name","sector","industry","marketCap","price","change_pct"]],use_container_width = True)

st.write("행 개수:", len(df))
st.write(df[["ticker","change_pct"]].head())