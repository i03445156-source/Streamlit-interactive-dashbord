import streamlit as st
import yfinance as yf
import pandas as pd
st.write('시가총액 200을 조회할 수 있습니다. 조회 가능 리스트는 다음과같습니다.')
st.write("전 세계 시가총액 상위 약 200개 종목"
    # --- 미국 (US: NASDAQ & NYSE) ---
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "BRK-B", "TSLA", "AVGO", "LLY",
    "V", "UNH", "JPM", "XOM", "MA", "WMT", "JNJ", "PG", "ORCL", "HD",
    "COST", "ABBV", "NFLX", "AMD", "MRK", "CVX", "CRM", "ADBE", "BAC", "PEP",
    "LIN", "KO", "TMO", "WFC", "ACN", "CSCO", "MCD", "DIS", "ABT", "INTU",
    "QCOM", "GE", "VZ", "CAT", "AMAT", "DHR", "TXN", "AXP", "AMGN", "IBM",
    "PFE", "PM", "MS", "UNP", "ISRG", "LOW", "SPGI", "RTX", "HON", "INTC",
    "GS", "SYK", "BKNG", "PLD", "ELV", "TJX", "VRTX", "LRCX", "BLK", "MDLZ",
    "REGN", "ADP", "PGR", "BA", "CI", "MMC", "BSX", "ADI", "NOW", "C",
    "GILD", "AMT", "LMT", "CB", "T", "SNPS", "MU", "PANW", "CDNS", "SCHW",
    
    # --- 한국 (South Korea: KOSPI) ---
    "005930.KS", "000660.KS", "005380.KS", "373220.KS", "207940.KS", "000270.KS", 
    "005935.KS", "068270.KS", "105560.KS", "055550.KS", "035420.KS", "000810.KS",
    "028260.KS", "012330.KS", "032830.KS", "051910.KS", "035720.KS", "017670.KS",
    
    # --- 일본 (Japan: Tokyo) ---
    "7203.T", "6758.T", "8035.T", "9984.T", "6857.T", "4063.T", "8306.T", "8001.T",
    "9432.T", "6501.T", "8058.T", "9433.T", "6367.T", "4519.T", "6098.T", "7741.T",
    "8316.T", "2914.T", "4568.T", "6954.T", "6273.T", "8031.T", "6146.T", "6920.T",

    # --- 대만 (Taiwan: TWSE) ---
    "2330.TW", "2454.TW", "2317.TW", "2308.TW", "2382.TW", "2881.TW", "2882.TW",

    # --- 유럽 (Europe: Germany, France, Netherlands, Spain, etc.) ---
    "ASML.AS", "MC.PA", "OR.PA", "SAP.DE", "TTE.PA", "RMS.PA", "SIE.DE", "AIR.PA",
    "NSRGY", "ALV.DE", "SAN.MC", "SU.PA", "EL.PA", "IBE.MC", "BNP.PA", "ITX.MC",
    "BMW.DE", "DTE.DE", "MBG.DE", "BAS.DE", "ENEL.MI", "ISP.MI", "DHL.DE", "AD.AS",

    # --- 중국/홍콩 (China/Hong Kong: HKEX, SSE, SZSE) ---
    "0700.HK", "9988.HK", "1810.HK", "3690.HK", "601857.SS", "600519.SS", "601318.SS",
    "601398.SS", "1211.HK", "9618.HK", "2318.HK", "0388.HK", "1299.HK", "0941.HK",
    # --- 기타 주요 글로벌 기업 (UK, Switzerland, etc.) ---
    "AZN.L", "SHEL.L", "HSBA.L", "ULVR.L", "BP.L", "RIO.L", "GSK.L", "DIAGEO.L",
    "ROG.SW", "NESN.SW", "NOVN.SW", "CFR.SW", "ZURN.SW")
# 1. 아까 뽑은 글로벌 200개 티커 중 일부를 예시로 넣거나 리스트 전체를 활용
top_tickers = [
    # --- 미국 (US: NASDAQ & NYSE) ---
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "BRK-B", "TSLA", "AVGO", "LLY",
    "V", "UNH", "JPM", "XOM", "MA", "WMT", "JNJ", "PG", "ORCL", "HD",
    "COST", "ABBV", "NFLX", "AMD", "MRK", "CVX", "CRM", "ADBE", "BAC", "PEP",
    "LIN", "KO", "TMO", "WFC", "ACN", "CSCO", "MCD", "DIS", "ABT", "INTU",
    "QCOM", "GE", "VZ", "CAT", "AMAT", "DHR", "TXN", "AXP", "AMGN", "IBM",
    "PFE", "PM", "MS", "UNP", "ISRG", "LOW", "SPGI", "RTX", "HON", "INTC",
    "GS", "SYK", "BKNG", "PLD", "ELV", "TJX", "VRTX", "LRCX", "BLK", "MDLZ",
    "REGN", "ADP", "PGR", "BA", "CI", "MMC", "BSX", "ADI", "NOW", "C",
    "GILD", "AMT", "LMT", "CB", "T", "SNPS", "MU", "PANW", "CDNS", "SCHW",
    
    # --- 한국 (South Korea: KOSPI) ---
    "005930.KS", "000660.KS", "005380.KS", "373220.KS", "207940.KS", "000270.KS", 
    "005935.KS", "068270.KS", "105560.KS", "055550.KS", "035420.KS", "000810.KS",
    "028260.KS", "012330.KS", "032830.KS", "051910.KS", "035720.KS", "017670.KS",
    
    # --- 일본 (Japan: Tokyo) ---
    "7203.T", "6758.T", "8035.T", "9984.T", "6857.T", "4063.T", "8306.T", "8001.T",
    "9432.T", "6501.T", "8058.T", "9433.T", "6367.T", "4519.T", "6098.T", "7741.T",
    "8316.T", "2914.T", "4568.T", "6954.T", "6273.T", "8031.T", "6146.T", "6920.T",

    # --- 대만 (Taiwan: TWSE) ---
    "2330.TW", "2454.TW", "2317.TW", "2308.TW", "2382.TW", "2881.TW", "2882.TW",

    # --- 유럽 (Europe: Germany, France, Netherlands, Spain, etc.) ---
    "ASML.AS", "MC.PA", "OR.PA", "SAP.DE", "TTE.PA", "RMS.PA", "SIE.DE", "AIR.PA",
    "NSRGY", "ALV.DE", "SAN.MC", "SU.PA", "EL.PA", "IBE.MC", "BNP.PA", "ITX.MC",
    "BMW.DE", "DTE.DE", "MBG.DE", "BAS.DE", "ENEL.MI", "ISP.MI", "DHL.DE", "AD.AS",

    # --- 중국/홍콩 (China/Hong Kong: HKEX, SSE, SZSE) ---
    "0700.HK", "9988.HK", "1810.HK", "3690.HK", "601857.SS", "600519.SS", "601318.SS",
    "601398.SS", "1211.HK", "9618.HK", "2318.HK", "0388.HK", "1299.HK", "0941.HK",

    # --- 기타 주요 글로벌 기업 (UK, Switzerland, etc.) ---
    "AZN.L", "SHEL.L", "HSBA.L", "ULVR.L", "BP.L", "RIO.L", "GSK.L", "DIAGEO.L",
    "ROG.SW", "NESN.SW", "NOVN.SW", "CFR.SW", "ZURN.SW"
]

st.set_page_config(page_title="글로벌 주식 분석기", layout="wide")
st.title(" 종목 재무 및 주가 조회기")

# 2. 사이드바에서 선택하거나 직접 입력
with st.sidebar:
    st.header("종목 선택")
    selected_ticker = st.selectbox("주요 종목 선택", top_tickers)
    manual_ticker = st.text_input("직접 티커 입력(예: TSLA)", "")

# 최종 조회할 티커 결정 (직접 입력 우선)
target = manual_ticker if manual_ticker else selected_ticker

if target:
    try:
        stock = yf.Ticker(target)
        
        # 데이터 미리 불러오기
        info = stock.info
        hist = stock.history(period='1y')
        
        # 상단 요약 정보 (Metric 활용)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("현재가", f"{info.get('currentPrice', 0):,.2f} {info.get('currency', '')}")
        with col2:
            # 아까 배운 .2f로 수익률 표시
            change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
            st.metric("전일대비", f"{change:.2f}%")
        with col3:
            st.write(f"**기업명:** {info.get('longName', 'N/A')}")

        # 3. 탭으로 정보 분리 (UI 깔끔하게)
        tab1, tab2, tab3 = st.tabs(["주가 차트", "재무제표", "기업 정보"])

        with tab1:
            st.subheader(f"{target} 1년 주가 흐름")
            st.line_chart(hist['Close'])

        with tab2:
            st.subheader("연간 재무제표")
            # yfinance의 financials는 데이터프레임이므로 바로 출력 가능
            st.dataframe(stock.financials, use_container_width=True)
            
            st.subheader("현금 흐름표")
            st.dataframe(stock.cashflow, use_container_width=True)

        with tab3:
            st.subheader("기업 개요")
            st.write(info.get('longBusinessSummary', '정보가 없습니다.'))
            
    except Exception as e:
        st.error(f"티커 '{target}'를 찾을 수 없습니다. 접미사(.KS, .T 등)를 확인해주세요!")