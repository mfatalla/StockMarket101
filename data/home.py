
import pandas as pd
import csv
import streamlit as st
from collections import defaultdict


st.set_page_config(
    page_title = 'SLAPSOIL',
    page_icon = '💜',
    layout= 'wide',
)

st.sidebar.image('data//logo1.png')



st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)


tabs = ["Home", "About", "Contact"]
query_params = st.experimental_get_query_params()

snp500 = pd.read_csv("updatated_ticker.csv")
symbols = snp500['Symbol'].sort_values().tolist()
snp500 = pd.read_csv("updatated_ticker.csv")
wap = snp500[['Symbol', 'Name']]


columns = defaultdict(list)  # each value in each column is appended to a list

with open('updatated_ticker.csv') as f:
    reader = csv.DictReader(f)  # read rows into a dictionary format
    for row in reader:  # read a row as {column1: value1, column2: value2,...}
        for (k, v) in row.items():  # go over each column name and value
            columns[k].append(v)  # append the value into the appropriate list
symbols = columns['Symbol']
company = columns['Name']

radio_list = company

default = int(query_params["companyname"][0]) if "companyname" in query_params else 0
companyname = st.sidebar.selectbox(
    "Choose a Company",
    radio_list,
    index=default
)
if companyname:
    st.experimental_set_query_params(companyname=radio_list.index(companyname))

active_tab = "Home"

st.sidebar.markdown((companyname))

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


if active_tab == "Home":
   st.markdown(companyname)
elif active_tab == "About":
    st.markdown(companyname)

    st.write("This page was created as a hacky demo of tabs")
elif active_tab == "Contact":
    st.markdown(companyname)

    st.write("If you'd like to contact me, then please don't.")
else:
    st.error("Something has gone terribly wrong.")




