import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="시장 트리맵", layout="wide")
st.title("유럽시장 시가총액 트리맵")


tickers = [
"ASML.AS", "MC.PA", "OR.PA", "SAP.DE", "TTE.PA", 
    "SIE.DE", "SAN.MC", "RMS.PA", "AIR.PA", "ALV.DE", 
    "SU.PA", "EL.PA", "IBE.MC", "BNP.PA", "ITX.MC", 
    "BMW.DE", "DTE.DE", "MBG.DE", "BBVA.MC", "DHL.DE", 
    "ENI.MI", "ISP.MI", "BAS.DE", "ENEL.MI", "AD.AS", 
    "KER.PA", "MUV2.DE", "CRH.L", "VIV.PA", "BN.PA", 
    "SAF.PA", "PRU.L", "ADS.DE", "STLAM.MI", "ASG.DE", 
    "CS.PA", "IFX.DE", "RWE.DE", "AH.AS", "ABI.BR", 
    "FLTR.L", "LIN.DE", "BEI.DE", "VOW3.DE", "HEI.DE", 
    "KER.PA", "EDP.LS", "KNEBV.HE", "NOKIA.HE", "VOLV-B.ST"
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