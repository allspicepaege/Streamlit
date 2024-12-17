import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

st.write('''
        # Котировки компании Apple
        ### Котировка акций при закрытии биржи
         ''')

tickerSymbol = 'AAPL'
tickerData = yf.Ticker(tickerSymbol)
tickerDF = tickerData.history(period='1d', start='2015-1-1', end='2024-1-1')

st.line_chart(tickerDF.Close)
st.write('### Общее количество акций, участвующих в торгах')
st.line_chart(tickerDF.Volume)