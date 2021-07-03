"""
Yahoo Finance Data app

Author: Paduel https://github.com/paduel
Original Source: https://github.com/paduel/streamlit_finance_chart
"""

import pandas as pd
import streamlit as st
import requests
import yfinance as yf
from bs4 import BeautifulSoup
import profile
import overview
import scrappy
import technical
import line_chart
import candlestick

st.set_page_config(
    page_title = 'SLAPSOIL',
    page_icon = '💜',
    layout= 'wide',
    initial_sidebar_state="expanded",
)

@st.cache
def load_data():
    components = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S" "%26P_500_companies"
    )[0]
    return components.drop("SEC filings", axis=1).set_index("Symbol")


@st.cache(allow_output_mutation=True)
def load_quotes(asset):
    return yf.download(asset)


def main():

    menu = ['Overview', 'News', 'Technical Indicators', 'Company Profile', 'About']
    query_params = st.experimental_get_query_params()

    # Query parameters are returned as a list to support multiselect.
    # Get the first item in the list if the query parameter exists.
    default = int(query_params["menubar"][0]) if "menubar" in query_params else 0
    menubar = st.selectbox(
        "Menu",
        menu,
        index=default
    )
    if menubar:
        st.experimental_set_query_params(menubar=menu.index(menubar))

    components = load_data()
    title = st.empty()

    st.sidebar.image('data//logo1.png')

    def label(symbol):
        a = components.loc[symbol]
        return symbol + " - " + a.Security

    st.sidebar.subheader("Select asset")
    asset = st.sidebar.selectbox(
        "Click below to select a new asset",
        components.index.sort_values(),
        index=3,
        format_func=label,
    )



    ticker = yf.Ticker(asset)
    info = ticker.info
    url = 'https://stockanalysis.com/stocks/' + asset
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    name = soup.find('h1', {'class': 'sa-h1'}).text
    price = soup.find('span', {'id': 'cpr'}).text
    currency = soup.find('span', {'id': 'cpr'}).find_next('span').text
    change = soup.find('span', {'id': 'spd'}).text
    rate = soup.find('span', {'id': 'spd'}).find_next('span').text
    CR = change + " (" + rate + ")"
    sub = change

    inputtab = st.sidebar.beta_container()
    with inputtab:
        with st.form("my_form"):
            st.image(info['logo_url'])
            qq = (info['shortName'])
            st.markdown(f"<p style='vertical-align:bottom;font-weight: bold; color: #FFFFFF;font-size: 40px;'>{qq}</p>",
                        unsafe_allow_html=True)
            xx = price + " " + currency
            st.markdown(f"<p style='vertical-align:bottom;font-weight: bold; color: #FFFFFF;font-size: 20px;'>{xx}</p>",
                        unsafe_allow_html=True)
            if float(sub) > 0:
                aye2 = "+"

                st.markdown(
                    f"<p style='vertical-align:bottom;font-weight: bold; color: #00AC4A;font-size: 13px;'>{aye2 + CR}</p>",
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<p style='vertical-align:bottom;font-weight: bold; color: #D10000;font-size: 13px;'>{CR}</p>",
                    unsafe_allow_html=True)


            submitted = st.form_submit_button("")

    if menubar == 'Overview':
        st.title("Line Chart")
        line_chart.line_chart(asset)
        st.title("Candlestick Chart")
        candlestick.candlestick(asset)

    elif menubar == 'News':
        overview.news(asset)

    elif menubar == 'Technical Indicators':
        technical.Scrappy(asset)
    elif menubar == 'Company Profile':
        profile.Profile(asset)

    elif menubar == 'About':
        overview.news(asset)
    else:
        st.error("Something has gone terribly wrong.")




main()