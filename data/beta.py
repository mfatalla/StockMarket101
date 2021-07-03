import streamlit as st
import requests
import yfinance as yf
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np



st.set_page_config(
    page_title = 'SLAPSOIL',
    page_icon = '💜',
    layout= 'wide',
)
headerinput = st.beta_container()
with headerinput:
    st.sidebar.image('data//logo1.png')
    input = st.sidebar.text_input("Enter Ticker Symbol Here")

if input == "":
    input='NFLX'


ticker = yf.Ticker(input)
info = ticker.info

samplechart = ticker.history(period="max", interval="1wk")
samplechart2 = ticker.history(start="2020-06-02", end="2020-06-07", interval="1m")


first, second, thirdy = st.beta_columns([1, 3, 6])
with first:
    st.image(info['logo_url'])


with second:
    qq = (info['shortName'])
    st.markdown(f"<p style='vertical-align:bottom;font-weight: bold; color: #0E1117;font-size: 30px;'>{qq}</p>",
                unsafe_allow_html=True)
    st.markdown(f"<p style='vertical-align:bottom;font-weight: bold; color: #FFFFFF;font-size: 40px;'>{qq}</p>",
                unsafe_allow_html=True)

    url = 'https://stockanalysis.com/stocks/'+input
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    name = soup.find('h1', {'class': 'sa-h1'}).text
    price = soup.find('span', {'id': 'cpr'}).text
    currency = soup.find('span', {'id': 'cpr'}).find_next('span').text
    change = soup.find('span', {'id': 'spd'}).text
    rate = soup.find('span', {'id': 'spd'}).find_next('span').text
    meta = soup.find('div', {'id': 'sti'}).find('span').text
    after = soup.find('div', {'id': 'ext'}).find_next('span').text
    after2 = soup.find('span', {'id': 'extc'}).text
    aftert = soup.find('span', {'id': 'extcp'}).text
    aftertime = soup.find('span', {'id': 'exttime'}).text
    CR = change+" ("+rate+")"
    CT = after2+" ("+aftert+")"
    sub = change
    sub2 = after2
    aye = " PRE-MARKET: "

p1, p2,p3,p4 = st.beta_columns([2, 2,10,7])
with p1:
    st.markdown(
        f"<p style='vertical-align:bottom;font-weight: bold; color: #0E1117;font-size: 15px;'>{aye}</p>",
        unsafe_allow_html=True)
    st.markdown(
        f"<p style='vertical-align:bottom;font-weight: bold; color: #FAFAFA;font-size: 15px;'>{aye}</p>",
        unsafe_allow_html=True)
with p2:
    st.markdown(price + " " + currency)
    st.markdown(after+ " " + currency)
    st.markdown(meta)


with p3:

    if float(sub) > 0:
        aye2 = "+"
        st.markdown(
            f"<p style='vertical-align:bottom;font-weight: bold; color: #00AC4A;font-size: 15px;'>{aye2+CR}</p>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            f"<p style='vertical-align:bottom;font-weight: bold; color: #D10000;font-size: 15px;'>{CR}</p>",
            unsafe_allow_html=True)
    if float(sub2) > 0:
        st.markdown(
            f"<p style='vertical-align:bottom;font-weight: bold; color: #00AC4A;font-size: 15px;'>{CT}</p>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            f"<p style='vertical-align:bottom;font-weight: bold; color: #D10000;;font-size: 15px;'>{CT}</p>",
            unsafe_allow_html=True)
with p4:
    st.markdown(
        f"<p style='vertical-align:bottom;font-weight: bold; color: #0E1117;font-size: 15px;'>{aye}</p>",
        unsafe_allow_html=True)

with thirdy:
    st.markdown(
        f"<p style='vertical-align:bottom;font-weight: bold; color: #0E1117;font-size: 15px;'>{aye}</p>",
        unsafe_allow_html=True)

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)

st.line_chart(samplechart)

third, second = st.beta_columns([1, 6])

with second:
    st.markdown("")

with third:
    original_title = '<p style="font-family:Courier; color:#0E1117; font-size: 20px;">Original image</p>'
    st.markdown(original_title, unsafe_allow_html=True)


query_params = st.experimental_get_query_params()
tabs = ["Overview", "Technical Indicators", "Company Profile"]
if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Overview"

if active_tab not in tabs:
    st.experimental_set_query_params(tab="Stock Market")
    active_tab = "Overview"

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

if active_tab == "Overview":


    news = st.beta_container()
    with news:
        url = 'https://stockanalysis.com/stocks/' + input
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        name = soup.find('h1', {'class': 'sa-h1'}).text

        x = 0
        for x in range(10):
            newsTitle = soup.find_all('div', {'class': 'news-side'})[x].find('div').text
            newsThumbnail = soup.find_all('div', {'class': 'news-img'})[x].find('img')
            newsBody = soup.find_all('div', {'class': 'news-text'})[x].find('p').text
            subMeta = soup.find_all('div', {'class': 'news-meta'})[x].find_next('span').text
            hreflink = soup.find_all('div', {'class': 'news-img'})[x].find('a')
            link = hreflink.get('href')
            # print(link)
            # linkthumbnail = newsThumbnail.get('src')
            # print(linkthumbnail)
            wap = newsThumbnail.get('data-src')
            # print(wap)
            # print("News#"+str(x+1))
            # print(newsTitle)
            # print(newsBody)
            # print(subMeta)
            # print("")

            chart1, chart2, chart3 = st.beta_columns([1, 2, 3])
            with chart1:
                st.image(wap)
            with chart2:
                st.markdown(f"<h1 style='font-weight: bold; font-size: 17px;'>{newsTitle}</h1>", unsafe_allow_html=True)
                st.markdown(newsBody)
                link = "(" + link + ")"
                aye = '[[Link]]' + link
                st.markdown("Source: " + aye, unsafe_allow_html=True)
                st.text(" ")
                st.text(" ")

            with chart3:
                st.markdown(subMeta)

        st.text(" ")

elif active_tab == "Technical Indicators":

    def calcMovingAverage(data, size):
        df = data.copy()
        df['sma'] = df['Adj Close'].rolling(size).mean()
        df['ema'] = df['Adj Close'].ewm(span=size, min_periods=size).mean()
        df.dropna(inplace=True)
        return df


    def calc_macd(data):
        df = data.copy()
        df['ema12'] = df['Adj Close'].ewm(span=12, min_periods=12).mean()
        df['ema26'] = df['Adj Close'].ewm(span=26, min_periods=26).mean()
        df['macd'] = df['ema12'] - df['ema26']
        df['signal'] = df['macd'].ewm(span=9, min_periods=9).mean()
        df.dropna(inplace=True)
        return df


    def calcBollinger(data, size):
        df = data.copy()
        df["sma"] = df['Adj Close'].rolling(size).mean()
        df["bolu"] = df["sma"] + 2 * df['Adj Close'].rolling(size).std(ddof=0)
        df["bold"] = df["sma"] - 2 * df['Adj Close'].rolling(size).std(ddof=0)
        df["width"] = df["bolu"] - df["bold"]
        df.dropna(inplace=True)
        return df


    st.title('Technical Indicators')
    st.subheader('Moving Average')

    coMA1, coMA2 = st.beta_columns(2)

    with coMA1:
        numYearMA = st.number_input('Insert period (Year): ', min_value=1, max_value=10, value=2, key=0)

    with coMA2:
        windowSizeMA = st.number_input('Window Size (Day): ', min_value=5, max_value=500, value=20, key=1)

    start = dt.datetime.today() - dt.timedelta(numYearMA * 365)
    end = dt.datetime.today()
    dataMA = yf.download(input, start, end)
    df_ma = calcMovingAverage(dataMA, windowSizeMA)
    df_ma = df_ma.reset_index()

    figMA = go.Figure()

    figMA.add_trace(
        go.Scatter(
            x=df_ma['Date'],
            y=df_ma['Adj Close'],
            name="Prices Over Last " + str(numYearMA) + " Year(s)"
        )
    )

    figMA.add_trace(
        go.Scatter(
            x=df_ma['Date'],
            y=df_ma['sma'],
            name="SMA" + str(windowSizeMA) + " Over Last " + str(numYearMA) + " Year(s)"
        )
    )

    figMA.add_trace(
        go.Scatter(
            x=df_ma['Date'],
            y=df_ma['ema'],
            name="EMA" + str(windowSizeMA) + " Over Last " + str(numYearMA) + " Year(s)"
        )
    )

    figMA.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    figMA.update_layout(legend_title_text='Trend')
    figMA.update_yaxes(tickprefix="$")

    st.plotly_chart(figMA, use_container_width=True)

    st.subheader('Moving Average Convergence Divergence (MACD)')
    numYearMACD = st.number_input('Insert period (Year): ', min_value=1, max_value=10, value=2, key=2)

    startMACD = dt.datetime.today() - dt.timedelta(numYearMACD * 365)
    endMACD = dt.datetime.today()
    dataMACD = yf.download(input, startMACD, endMACD)
    df_macd = calc_macd(dataMACD)
    df_macd = df_macd.reset_index()

    figMACD = make_subplots(rows=2, cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.01)

    figMACD.add_trace(
        go.Scatter(
            x=df_macd['Date'],
            y=df_macd['Adj Close'],
            name="Prices Over Last " + str(numYearMACD) + " Year(s)"
        ),
        row=1, col=1
    )

    figMACD.add_trace(
        go.Scatter(
            x=df_macd['Date'],
            y=df_macd['ema12'],
            name="EMA 12 Over Last " + str(numYearMACD) + " Year(s)"
        ),
        row=1, col=1
    )

    figMACD.add_trace(
        go.Scatter(
            x=df_macd['Date'],
            y=df_macd['ema26'],
            name="EMA 26 Over Last " + str(numYearMACD) + " Year(s)"
        ),
        row=1, col=1
    )

    figMACD.add_trace(
        go.Scatter(
            x=df_macd['Date'],
            y=df_macd['macd'],
            name="MACD Line"
        ),
        row=2, col=1
    )

    figMACD.add_trace(
        go.Scatter(
            x=df_macd['Date'],
            y=df_macd['signal'],
            name="Signal Line"
        ),
        row=2, col=1
    )

    figMACD.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="left",
        x=0
    ))

    figMACD.update_yaxes(tickprefix="$")
    st.plotly_chart(figMACD, use_container_width=True)

    st.subheader('Bollinger Band')
    coBoll1, coBoll2 = st.beta_columns(2)
    with coBoll1:
        numYearBoll = st.number_input('Insert period (Year): ', min_value=1, max_value=10, value=2, key=6)

    with coBoll2:
        windowSizeBoll = st.number_input('Window Size (Day): ', min_value=5, max_value=500, value=20, key=7)

    startBoll = dt.datetime.today() - dt.timedelta(numYearBoll * 365)
    endBoll = dt.datetime.today()
    dataBoll = yf.download(input, startBoll, endBoll)
    df_boll = calcBollinger(dataBoll, windowSizeBoll)
    df_boll = df_boll.reset_index()
    figBoll = go.Figure()
    figBoll.add_trace(
        go.Scatter(
            x=df_boll['Date'],
            y=df_boll['bolu'],
            name="Upper Band"
        )
    )

    figBoll.add_trace(
        go.Scatter(
            x=df_boll['Date'],
            y=df_boll['sma'],
            name="SMA" + str(windowSizeBoll) + " Over Last " + str(numYearBoll) + " Year(s)"
        )
    )

    figBoll.add_trace(
        go.Scatter(
            x=df_boll['Date'],
            y=df_boll['bold'],
            name="Lower Band"
        )
    )

    figBoll.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="left",
        x=0
    ))

    figBoll.update_yaxes(tickprefix="$")
    st.plotly_chart(figBoll, use_container_width=True)


elif active_tab == "Company Profile":

    st.title('Company Profile')
    st.subheader(info['longName'])
    st.markdown('** Sector **: ' + info['sector'])
    st.markdown('** Industry **: ' + info['industry'])
    st.markdown('** Phone **: ' + info['phone'])
    st.markdown(
        '** Address **: ' + info['address1'] + ', ' + info['city'] + ', ' + info['zip'] + ', ' + info['country'])
    st.markdown('** Website **: ' + info['website'])
    st.markdown('** Business Summary **')
    st.info(info['longBusinessSummary'])

    fundInfo = {
        'Enterprise Value (USD)': info['enterpriseValue'],
        'Enterprise To Revenue Ratio': info['enterpriseToRevenue'],
        'Enterprise To Ebitda Ratio': info['enterpriseToEbitda'],
        'Net Income (USD)': info['netIncomeToCommon'],
        'Profit Margin Ratio': info['profitMargins'],
        'Forward PE Ratio': info['forwardPE'],
        'PEG Ratio': info['pegRatio'],
        'Price to Book Ratio': info['priceToBook'],
        'Forward EPS (USD)': info['forwardEps'],
        'Beta ': info['beta'],
        'Book Value (USD)': info['bookValue'],
        'Dividend Rate (%)': info['dividendRate'],
        'Dividend Yield (%)': info['dividendYield'],
        'Five year Avg Dividend Yield (%)': info['fiveYearAvgDividendYield'],
        'Payout Ratio': info['payoutRatio']
    }

    fundDF = pd.DataFrame.from_dict(fundInfo, orient='index')
    fundDF = fundDF.rename(columns={0: 'Value'})
    st.subheader('Fundamental Info')
    st.table(fundDF)

    st.subheader('General Stock Info')
    st.markdown('** Market **: ' + info['market'])
    st.markdown('** Exchange **: ' + info['exchange'])
    st.markdown('** Quote Type **: ' + info['quoteType'])

    start = dt.datetime.today() - dt.timedelta(2 * 365)
    end = dt.datetime.today()
    df = yf.download(input, start, end)
    df = df.reset_index()
    fig = go.Figure(
        data=go.Scatter(x=df['Date'], y=df['Adj Close'])
    )
    fig.update_layout(
        title={
            'text': "Stock Prices Over Past Two Years",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    st.plotly_chart(fig, use_container_width=True)

    marketInfo = {
        "Volume": info['volume'],
        "Average Volume": info['averageVolume'],
        "Market Cap": info["marketCap"],
        "Float Shares": info['floatShares'],
        "Regular Market Price (USD)": info['regularMarketPrice'],
        'Bid Size': info['bidSize'],
        'Ask Size': info['askSize'],
        "Share Short": info['sharesShort'],
        'Short Ratio': info['shortRatio'],
        'Share Outstanding': info['sharesOutstanding']

    }

    marketDF = pd.DataFrame(data=marketInfo, index=[0])
    st.table(marketDF)

else:
    st.error("Something has gone terribly wrong.")




