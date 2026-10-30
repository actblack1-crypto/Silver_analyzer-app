#!/usr/bin/env python3
"""Silver Price Analyzer — SLV-focused technical dashboard."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import yfinance as yf
import ta

st.set_page_config(page_title="Silver Price Analyzer (SLV)", page_icon="🥈", layout="wide")
st.markdown("""
<style>
.main-header{font-size:2.35rem;font-weight:750;color:#c0c0c0;margin-bottom:.2rem}
[data-testid="stMetric"]{background:#1e1e2e;padding:12px;border-radius:9px}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300, show_spinner=False)
def load_data(symbol, period):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, auto_adjust=False)
    try: info = ticker.info or {}
    except Exception: info = {}
    return hist, info

def add_indicators(df):
    df = df.copy(); c = df.Close
    df["SMA_20"] = ta.trend.sma_indicator(c, window=20)
    df["SMA_50"] = ta.trend.sma_indicator(c, window=50)
    df["SMA_200"] = ta.trend.sma_indicator(c, window=200)
    df["EMA_12"] = ta.trend.ema_indicator(c, window=12)
    df["EMA_26"] = ta.trend.ema_indicator(c, window=26)
    df["RSI"] = ta.momentum.rsi(c, window=14)
    df["MACD"] = ta.trend.macd(c)
    df["MACD_signal"] = ta.trend.macd_signal(c)
    df["MACD_hist"] = ta.trend.macd_diff(c)
    bb = ta.volatility.BollingerBands(c, window=20, window_dev=2)
    df["BB_upper"], df["BB_middle"], df["BB_lower"] = bb.bollinger_hband(), bb.bollinger_mavg(), bb.bollinger_lband()
    df["ATR"] = ta.volatility.average_true_range(df.High, df.Low, c, window=14)
    df["Volatility_20"] = c.pct_change().rolling(20).std() * np.sqrt(252) * 100
    return df

def make_chart(df, symbol):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=.035,
        row_heights=[.62,.19,.19], subplot_titles=(f"{symbol} Price & Moving Averages","Volume","RSI (14)"))
    fig.add_trace(go.Candlestick(x=df.index, open=df.Open, high=df.High, low=df.Low, close=df.Close,
        name="Price", increasing_line_color="#26a69a", decreasing_line_color="#ef5350"), row=1,col=1)
    for col,color,label in [("SMA_20","#ffd700","SMA 20"),("SMA_50","#ff8c00","SMA 50"),("SMA_200","#ff1493","SMA 200")]:
        if df[col].notna().any(): fig.add_trace(go.Scatter(x=df.index,y=df[col],name=label,line=dict(color=color,width=1.4)),row=1,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df.BB_upper,name="Bollinger upper",line=dict(color="rgba(100,149,237,.5)",width=1),showlegend=False),row=1,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df.BB_lower,name="Bollinger lower",line=dict(color="rgba(100,149,237,.5)",width=1),fill="tonexty",fillcolor="rgba(100,149,237,.08)",showlegend=False),row=1,col=1)
    colors=["#26a69a" if c>=o else "#ef5350" for o,c in zip(df.Open,df.Close)]
    fig.add_trace(go.Bar(x=df.index,y=df.Volume,marker_color=colors,name="Volume"),row=2,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df.RSI,name="RSI",line=dict(color="#8ab4f8")),row=3,col=1)
    fig.add_hline(y=70,line_dash="dash",line_color="#ef5350",row=3,col=1)
    fig.add_hline(y=30,line_dash="dash",line_color="#26a69a",row=3,col=1)
    fig.update_layout(template="plotly_dark",height=790,margin=dict(l=10,r=10,t=55,b=10),xaxis_rangeslider_visible=False,
        legend=dict(orientation="h",y=1.02),paper_bgcolor="#0e1117",plot_bgcolor="#0e1117")
    fig.update_yaxes(title_text="Price ($)",row=1,col=1); fig.update_yaxes(title_text="Shares",row=2,col=1)
    fig.update_yaxes(title_text="RSI",range=[0,100],row=3,col=1)
    return fig

st.markdown('<div class="main-header">🥈 Silver Price Analyzer</div>',unsafe_allow_html=True)
st.caption("SLV-focused technical dashboard • Market data via Yahoo Finance")
with st.sidebar:
    st.header("Analyzer settings")
    symbol=st.text_input("Ticker symbol",value="SLV").strip().upper() or "SLV"
    period=st.selectbox("Historical period",["1mo","3mo","6mo","1y","2y","5y","10y","max"],index=5)
    if st.button("Refresh data",use_container_width=True): st.cache_data.clear(); st.rerun()
try:
    with st.spinner(f"Loading {symbol} market data..."):
        raw,info=load_data(symbol,period)
except Exception as e:
    st.error(f"Could not retrieve market data: {e}"); st.stop()
if raw is None or raw.empty:
    st.error("No price history returned. Check the ticker symbol and try again."); st.stop()
required={"Open","High","Low","Close","Volume"}
if not required.issubset(raw.columns): st.error("Unexpected data format from provider."); st.stop()
data=add_indicators(raw.dropna(subset=["Open","High","Low","Close"]))
if len(data)<2: st.warning("Not enough historical data to calculate indicators."); st.stop()
last,prev=data.iloc[-1],data.iloc[-2]
price=float(last.Close); change=price-float(prev.Close); pct=change/float(prev.Close)*100 if prev.Close else 0
rsi=float(last.RSI) if pd.notna(last.RSI) else float("nan")
if np.isnan(rsi): momentum="Not enough history"
elif rsi>=70: momentum="Potentially overbought"
elif rsi<=30: momentum="Potentially oversold"
else: momentum="Neutral RSI range"
if pd.notna(last.SMA_200) and price>last.SMA_50>last.SMA_200: trend="Bullish moving-average alignment"
elif pd.notna(last.SMA_200) and price<last.SMA_50<last.SMA_200: trend="Bearish moving-average alignment"
else: trend="Mixed / transitional trend"
st.subheader(info.get("longName") or info.get("shortName") or symbol)
c1,c2,c3,c4=st.columns(4)
c1.metric("Latest close",f"{info.get('currency','USD')} {price:,.2f}",f"{change:+.2f} ({pct:+.2f}%)")
c2.metric("RSI (14)","—" if np.isnan(rsi) else f"{rsi:.1f}",momentum)
c3.metric("20-day volatility","—" if pd.isna(last.Volatility_20) else f"{last.Volatility_20:.1f}%")
c4.metric("Average true range",f"{last.ATR:.2f}")
st.info(f"**Trend reading:** {trend}. Indicator descriptions are not buy or sell instructions.")
st.plotly_chart(make_chart(data,symbol),use_container_width=True)
left,right=st.columns(2)
with left:
    st.subheader("Technical snapshot")
    keys=[("SMA 20","SMA_20"),("SMA 50","SMA_50"),("SMA 200","SMA_200"),("EMA 12","EMA_12"),("EMA 26","EMA_26"),("MACD","MACD"),("MACD signal","MACD_signal"),("Bollinger upper","BB_upper"),("Bollinger lower","BB_lower")]
    st.dataframe(pd.DataFrame({"Indicator":[x[0] for x in keys],"Latest value":[last[x[1]] for x in keys]}),hide_index=True,use_container_width=True)
with right:
    st.subheader("Recent price history")
    st.dataframe(data[["Open","High","Low","Close","Volume"]].tail(10).sort_index(ascending=False),use_container_width=True)
st.download_button("Download historical data (CSV)",data=data.to_csv().encode("utf-8"),file_name=f"{symbol.lower()}_analysis.csv",mime="text/csv")
st.caption(f"Last data timestamp: {data.index[-1]} • Yahoo Finance • Five-minute cache")
st.warning("Educational information only. SLV is an exchange-traded product and may not track spot silver exactly. Data may be delayed or unavailable. This app does not provide personalized financial, tax, or investment advice and does not place trades.")
