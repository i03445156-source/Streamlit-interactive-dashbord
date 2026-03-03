import streamlit as st
import pandas as pd
import plotly.express as px
import pyupbit

st.set_page_config(page_title="업비트 시장 트리맵", layout="wide")
st.title(" 업비트 크립토 시장 거래대금 트리맵")

# 주요 티커 리스트
tickers = [
    "KRW-BTC", "KRW-ETH", "KRW-SOL", "KRW-XRP", "KRW-ADA",
    "KRW-DOGE", "KRW-AVAX", "KRW-DOT", "KRW-TRX", "KRW-LINK",
    "KRW-STX", "KRW-ETC", "KRW-APT", "KRW-ARB", "KRW-SUI", 
    "KRW-SEI", "KRW-SHIB", "KRW-NEAR", "KRW-FIL", "KRW-BCH"
]

@st.cache_data(ttl=60) # 코인은 변동성이 크므로 캐시 시간을 1분으로 단축
def fetch_snapshot(tickers):
    rows = []
    for tkr in tickers:
        try:
            # 1. 일봉 데이터 가져오기 (최근 2일)
            df_hist = pyupbit.get_ohlcv(tkr, interval="day", count=2)
            
            if df_hist is not None and len(df_hist) >= 2:
                prev_close = df_hist['close'].iloc[-2]
                last_close = df_hist['close'].iloc[-1]
                acc_value = df_hist['value'].iloc[-1] # 당일 거래대금 (시총 대용)
                
                chg_pct = (last_close - prev_close) / prev_close * 100
                
                # 섹터를 임의로 지정 (분석 시 직접 분류 추가 가능)
                sector = "Layer 1" if tkr in ["KRW-BTC", "KRW-ETH", "KRW-SOL", "KRW-ADA"] else "Altcoin"
                if "SHIB" in tkr or "DOGE" in tkr: sector = "Meme"

                rows.append({
                    "ticker": tkr.replace("KRW-", ""), # 이름 깔끔하게
                    "sector": sector,
                    "value": acc_value, # 트리맵 크기 기준
                    "price": last_close,
                    "change_pct": chg_pct
                })
        except Exception as e:
            continue
            
    return pd.DataFrame(rows)

df = fetch_snapshot(tickers)

if not df.empty:
    # 트리맵 그리기
    # path를 [sector, ticker]로 단순화 (업비트에는 industry 데이터가 없음)
    fig = px.treemap(
        df,
        path=['sector', 'ticker'],
        values="value",
        color='change_pct',
        color_continuous_scale='RdYlGn', # 하락:빨강, 상승:초록
        range_color=[-5, 5], # 색상 기준 범위 설정
        hover_data={"price": ":,.0f", "change_pct": ":.2f"}
    )

    fig.update_traces(
        # 여기서 :.2f를 사용해 소수점 둘째 자리까지 표시합니다.
        texttemplate="<b>%{label}</b><br>%{customdata[1]:.2f}%",
        textfont_size=18
    )

    fig.update_layout(margin=dict(t=30, l=10, r=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

    # 데이터프레임 표시
    st.subheader("상세 데이터")
    st.dataframe(df.style.format({'change_pct': '{:.2f}%', 'price': '{:,.0f}', 'value': '{:,.0f}'}), use_container_width=True)
else:
    st.error("데이터를 불러오지 못했습니다.")