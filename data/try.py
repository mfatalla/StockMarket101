
import technical
import overview
import requests
import yfinance as yf
from bs4 import BeautifulSoup
import profile
import scrappy
import pandas as pd
import csv
import streamlit as st
from collections import defaultdict

st.set_page_config(
    page_title = 'SLAPSOIL',
    page_icon = '💜',
    layout= 'wide',
    initial_sidebar_state="expanded",
)

st.sidebar.image('data//logo1.png')

inputbox = st.sidebar.beta_container()

with inputbox:

    st.write("")
    st.write("")
    snp500 = pd.read_csv("updatated_ticker.csv")
    symbols = snp500['Symbol'].sort_values().tolist()
    snp500 = pd.read_csv("updatated_ticker.csv")
    wap = snp500[['Symbol','Name']]

    columns = defaultdict(list) # each value in each column is appended to a list

    with open('updatated_ticker.csv') as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value
                columns[k].append(v) # append the value into the appropriate list
    symbols = columns['Symbol']
    company = columns['Name']

    radio_list = company
    query_params = st.experimental_get_query_params()

    # Query parameters are returned as a list to support multiselect.
    # Get the first item in the list if the query parameter exists.
    default = int(query_params["activity"][0]) if "activity" in query_params else 0
    companyname = st.selectbox(
        "Choose a Company",
        radio_list,
        index=default
    )
    if companyname:
        st.experimental_set_query_params(activity=radio_list.index(companyname))


menubar = st.selectbox(
    'Menu',
    ('Overview', 'Technical Indicators', 'Company Profile', 'About'))



tickerinput = snp500.loc[snp500['Name'] == companyname, 'Symbol'].iloc[0]
ww = tickerinput
tickerbox = st.sidebar.beta_container()
with tickerbox:
    chart1, chart2= st.beta_columns([1, 1])
    with chart1:
        st.write("Ticker Symbol:")
    with chart2:
        st.markdown(f"<p style='vertical-align:bottom;font-weight: bold; color: #FFFFFF;font-size: 20px;'>{ww}</p>",
                    unsafe_allow_html=True)



scrappy.Scrappy(tickerinput)

if menubar == 'Overview':
    ticker = yf.Ticker(tickerinput)
    info = ticker.info
    samplechart = ticker.history(period="max", interval="1wk")
    st.line_chart(samplechart, height=600)
    overview.News(tickerinput)
elif menubar == 'News':
    st.write("WAP")

elif menubar == 'Technical Indicators':
    technical.Scrappy(tickerinput)
elif menubar == 'Company Profile':
    profile.Profile(tickerinput)

elif menubar == 'About':
    overview.News(tickerinput)
else:
    st.error("Something has gone terribly wrong.")