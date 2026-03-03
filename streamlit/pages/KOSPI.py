import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="시장 트리맵", layout="wide")
st.title("한국 시가총액 변동 트리맵")


tickers = [
    "005930.KS", "000660.KS", "005380.KS", "005935.KS", "373220.KS",
    "402340.KS", "207940.KS", "000270.KS", "034020.KS", "329180.KS",
    "012450.KS", "028260.KS", "105560.KS", "068270.KS", "012330.KS",
    "032830.KS", "055550.KS", "042660.KS", "010130.KS", "006800.KS",
    "005490.KS", "035420.KS", "051910.KS", "000810.KS", "035720.KS",
    "003550.KS", "017670.KS", "011200.KS", "009150.KS", "033780.KS",
    "018260.KS", "000660.KS", "010950.KS", "138040.KS", "316140.KS",
    "066570.KS", "003670.KS", "086790.KS", "000100.KS", "034730.KS",
    "015760.KS", "032640.KS", "011780.KS", "009830.KS", "004020.KS",
    "009540.KS", "010140.KS", "024110.KS", "034220.KS", "047050.KS",
    "001040.KS", "086280.KS", "259960.KS", "071050.KS", "036570.KS",
    "003470.KS", "011170.KS", "012750.KS", "005830.KS", "051900.KS",
    "000080.KS", "014680.KS", "008770.KS", "021240.KS", "097950.KS",
    "004170.KS", "010620.KS", "023530.KS", "078930.KS", "002380.KS",
    "000720.KS", "005940.KS", "028050.KS", "052690.KS", "011070.KS",
    "064350.KS", "006400.KS", "001450.KS", "001740.KS", "267250.KS",
    "000210.KS", "000060.KS", "161390.KS", "020150.KS", "282330.KS",
    "008930.KS", "030200.KS", "000120.KS", "006360.KS", "005385.KS",
    "004990.KS", "005387.KS", "180640.KS", "000990.KS", "003230.KS",
    "001570.KS", "011210.KS", "016360.KS", "005440.KS", "001800.KS"
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