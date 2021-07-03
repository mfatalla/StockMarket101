
import pandas as pd
import streamlit as st
import yfinance
import csv
from collections import defaultdict


@st.cache
def load_data():
    components = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S" "%26P_500_companies"
    )[0]
    return components.drop("SEC filings", axis=1).set_index("Symbol")


@st.cache(allow_output_mutation=True)
def load_quotes(companyname):
    return yfinance.download(companyname)


def main():

    snp500 = pd.read_csv("data/updatated_ticker.csv")
    symbols = snp500['Symbol'].sort_values().tolist()
    snp500 = pd.read_csv("data/updatated_ticker.csv")
    wap = snp500[['Symbol','Name']]

    columns = defaultdict(list) # each value in each column is appended to a list

    with open('data/updatated_ticker.csv') as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value
                columns[k].append(v) # append the value into the appropriate list
    symbols1 = columns['Symbol']
    company = columns['Name']

    radio_list = symbols1
    query_params = st.experimental_get_query_params()

    # Query parameters are returned as a list to support multiselect.
    # Get the first item in the list if the query parameter exists.
    default = int(query_params["activity"][0]) if "activity" in query_params else 0
    companyname = st.sidebar.selectbox(
        "Choose a Company",
        radio_list,
        index=default
    )
    if companyname:
        st.experimental_set_query_params(activity=radio_list.index(companyname))

    components = load_data()
    title = st.empty()



    title.title(components.loc[companyname].Security)

    if st.sidebar.checkbox("View company info", True):
        st.table(components.loc[companyname])
    data0 = load_quotes(companyname)
    data = data0.copy().dropna()
    data.index.name = None

    section = st.sidebar.slider(
        "Number of quotes",
        min_value=30,
        max_value=min([2000, data.shape[0]]),
        value=500,
        step=10,
    )

    data2 = data[-section:]["Adj Close"].to_frame("Adj Close")

    sma = st.sidebar.checkbox("SMA")
    if sma:
        period = st.sidebar.slider(
            "SMA period", min_value=5, max_value=500, value=20, step=1
        )
        data[f"SMA {period}"] = data["Adj Close"].rolling(period).mean()
        data2[f"SMA {period}"] = data[f"SMA {period}"].reindex(data2.index)

    sma2 = st.sidebar.checkbox("SMA2")
    if sma2:
        period2 = st.sidebar.slider(
            "SMA2 period", min_value=5, max_value=500, value=100, step=1
        )
        data[f"SMA2 {period2}"] = data["Adj Close"].rolling(period2).mean()
        data2[f"SMA2 {period2}"] = data[f"SMA2 {period2}"].reindex(data2.index)

    st.subheader("Chart")
    st.line_chart(data2)

    if st.sidebar.checkbox("View stadistic"):
        st.subheader("Stadistic")
        st.table(data2.describe())

    if st.sidebar.checkbox("View quotes"):
        st.subheader(f"{companyname} historical data")
        st.write(data2)




main()