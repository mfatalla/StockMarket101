import requests
import yfinance as yf
from bs4 import BeautifulSoup
import streamlit as st

wapx = st.text_input('Enter here: ')
def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']





company = get_symbol(wapx)

ticker= yf.Ticker(wapx)
aapl_historical = ticker.history(period="max", interval="1wk")
info = ticker.info
x = st.text(company).text
if x == 'None':
    st.markdown("WAP")

st.line_chart(aapl_historical)