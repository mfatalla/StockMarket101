import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import datetime as dt



st.set_page_config(
    page_title = 'SLAPSOIL',
    page_icon = '💜',
    layout= 'wide',
    initial_sidebar_state="expanded",
)

@st.cache(suppress_st_warning=True)
def load_data():
    components = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S" "%26P_500_companies"
    )[0]
    return components.drop("SEC filings", axis=1).set_index("Symbol")


@st.cache(suppress_st_warning=True)
def load_quotes(asset):
    return yf.download(asset)



menu = ['Overview', 'News', 'Technical Indicators', 'Company Profile', 'About']
query_params = st.experimental_get_query_params()

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
meta = soup.find('div', {'id': 'sti'}).find('span').text

after = soup.find('div', {'id': 'ext'}).find_next('span').text
after2 = soup.find('span', {'id': 'extc'}).text
aftert = soup.find('span', {'id': 'extcp'}).text
aftertime = soup.find('span', {'id': 'exttime'}).text
CR = change + " (" + rate + ")"
CT = after2 + " (" + aftert + ")"
sub = change
sub2 = after2
aye = ": After-hours"

formtab = st.sidebar.beta_container()
with formtab:
    st.image(info['logo_url'])
    qq = (info['shortName'])
    st.markdown(
        f"<p style='vertical-align:bottom;font-weight: bold; color: #FFFFFF;font-size: 40px;'>{qq}</p>",
        unsafe_allow_html=True)
    xx = price + " " + currency
    st.markdown(
        f"<p style='vertical-align:bottom;font-weight: bold; color: #FFFFFF;font-size: 20px;'>{xx}</p>",
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

    st.markdown(
        f"<p style='vertical-align:bottom;font-weight: italic; color: #FFFFFF;font-size: 10px;'>{meta}</p>",
        unsafe_allow_html=True)

    if float(sub2) > 0:

        st.markdown(after + " " + currency)
        st.markdown(
            f"<p style='vertical-align:bottom;font-weight: bold; color: #00AC4A;font-size: 13px;'>{CT + aye}</p>",
            unsafe_allow_html=True)


    else:
        st.markdown(after + " " + currency)
        st.markdown(
            f"<p style='vertical-align:bottom;font-weight: bold; color: #D10000;;font-size: 13px;'>{CT + aye}</p>",
            unsafe_allow_html=True)

    st.markdown(
        f"<p style='vertical-align:bottom;font-weight: italic; color: #FFFFFF;font-size: 10px;'>{aftertime}</p>",
        unsafe_allow_html=True)



if menubar == 'Overview':
    left, right = st.beta_columns([1,1])
    with left:
        st.title("Line Chart")
        linechart = st.beta_container()
        with linechart:
            linechart_expander = st.beta_expander(label='Line Chart Settings')
            with linechart_expander:
                ticker = yf.Ticker(asset)
                info = ticker.info

                attri = ['SMA', 'SMA2']
                attributes = st.multiselect(
                    'Choose Chart Attributes [SMA, SMA2]',
                    attri,
                    default='SMA'
                )

                data0 = load_quotes(asset)
                data = data0.copy().dropna()
                data.index.name = None

                section = st.slider(
                    "Number of quotes",
                    min_value=30,
                    max_value=min([2000, data.shape[0]]),
                    value=500,
                    step=10,
                )
                data2 = data[-section:]["Adj Close"].to_frame("Adj Close")

                if "SMA" in attributes:
                    period = st.slider(
                        "SMA period", min_value=5, max_value=500, value=20, step=1
                    )
                    data[f"SMA {period}"] = data["Adj Close"].rolling(period).mean()
                    data2[f"SMA {period}"] = data[f"SMA {period}"].reindex(data2.index)

                if "SMA2" in attributes:
                    period2 = st.slider(
                        "SMA2 period", min_value=5, max_value=500, value=100, step=1
                    )
                    data[f"SMA2 {period2}"] = data["Adj Close"].rolling(period2).mean()
                    data2[f"SMA2 {period2}"] = data[f"SMA2 {period2}"].reindex(data2.index)
                linebutton = st.button('Linechart Set')

            st.subheader("Chart")
            st.line_chart(data2, height=400)
            if st.checkbox("View quotes"):
                st.subheader(f"{asset} historical data")
                st.write(data2)

        #st.title("Candlestick Chart")
        #candlestick = st.beta_container()
        #with candlestick:

                candlechart_expander = st.beta_expander(label='Line Chart Settings')
                with candlechart_expander:
                    intervalList = ["1m", "5m", "15m", "30m"]
                    query_paramsa5 = st.experimental_get_query_params()
                    default5 = int(query_paramsa5["sort"][0]) if "sort" in query_paramsa5 else 2
                    interval = st.selectbox(
                        'Interval in minutes',
                        intervalList,
                        index=default5
                    )

                    if interval:
                        st.experimental_set_query_params(sort=intervalList.index(interval))

                    dayList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                               16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
                    query_paramsa6 = st.experimental_get_query_params()
                    default6 = int(query_paramsa6["chartdays"][0]) if "chartdays" in query_paramsa6 else 9
                    chartdays = st.selectbox(
                        'No. of Days',
                        dayList,
                        index=default6
                    )
                    if chartdays:
                        st.experimental_set_query_params(chartdays=dayList.index(chartdays))

                    candlebutton = st.button('Candlestick Set')

                stock = yf.Ticker(asset)
                history_data = stock.history(interval=interval, period=str(chartdays) + "d")
                prices = history_data['Close']
                volumes = history_data['Volume']

                lower = prices.min()
                upper = prices.max()

                prices_ax = np.linspace(lower, upper, num=20)

                vol_ax = np.zeros(20)

                for i in range(0, len(volumes)):
                    if (prices[i] >= prices_ax[0] and prices[i] < prices_ax[1]):
                        vol_ax[0] += volumes[i]

                    elif (prices[i] >= prices_ax[1] and prices[i] < prices_ax[2]):
                        vol_ax[1] += volumes[i]

                    elif (prices[i] >= prices_ax[2] and prices[i] < prices_ax[3]):
                        vol_ax[2] += volumes[i]

                    elif (prices[i] >= prices_ax[3] and prices[i] < prices_ax[4]):
                        vol_ax[3] += volumes[i]

                    elif (prices[i] >= prices_ax[4] and prices[i] < prices_ax[5]):
                        vol_ax[4] += volumes[i]

                    elif (prices[i] >= prices_ax[5] and prices[i] < prices_ax[6]):
                        vol_ax[5] += volumes[i]

                    elif (prices[i] >= prices_ax[6] and prices[i] < prices_ax[7]):
                        vol_ax[6] += volumes[i]

                    elif (prices[i] >= prices_ax[7] and prices[i] < prices_ax[8]):
                        vol_ax[7] += volumes[i]

                    elif (prices[i] >= prices_ax[8] and prices[i] < prices_ax[9]):
                        vol_ax[8] += volumes[i]

                    elif (prices[i] >= prices_ax[9] and prices[i] < prices_ax[10]):
                        vol_ax[9] += volumes[i]

                    elif (prices[i] >= prices_ax[10] and prices[i] < prices_ax[11]):
                        vol_ax[10] += volumes[i]

                    elif (prices[i] >= prices_ax[11] and prices[i] < prices_ax[12]):
                        vol_ax[11] += volumes[i]

                    elif (prices[i] >= prices_ax[12] and prices[i] < prices_ax[13]):
                        vol_ax[12] += volumes[i]

                    elif (prices[i] >= prices_ax[13] and prices[i] < prices_ax[14]):
                        vol_ax[13] += volumes[i]

                    elif (prices[i] >= prices_ax[14] and prices[i] < prices_ax[15]):
                        vol_ax[14] += volumes[i]

                    elif (prices[i] >= prices_ax[15] and prices[i] < prices_ax[16]):
                        vol_ax[15] += volumes[i]

                    elif (prices[i] >= prices_ax[16] and prices[i] < prices_ax[17]):
                        vol_ax[16] += volumes[i]

                    elif (prices[i] >= prices_ax[17] and prices[i] < prices_ax[18]):
                        vol_ax[17] += volumes[i]

                    elif (prices[i] >= prices_ax[18] and prices[i] < prices_ax[19]):
                        vol_ax[18] += volumes[i]

                    else:
                        vol_ax[19] += volumes[i]

                fig = make_subplots(
                    rows=1, cols=2,
                    column_widths=[0.2, 0.8],
                    specs=[[{}, {}]],
                    horizontal_spacing=0.01

                )

                fig.add_trace(
                    go.Bar(
                        x=vol_ax,
                        y=prices_ax,
                        text=np.around(prices_ax, 2),
                        textposition='auto',
                        orientation='h'
                    ),

                    row=1, col=1
                )

                dateStr = history_data.index.strftime("%d-%m-%Y %H:%M:%S")

                fig.add_trace(
                    go.Candlestick(x=dateStr,
                                   open=history_data['Open'],
                                   high=history_data['High'],
                                   low=history_data['Low'],
                                   close=history_data['Close'],
                                   yaxis="y2"

                                   ),

                    row=1, col=2
                )

                fig.update_layout(
                    title_text='Market Profile Chart (US S&P 500)',  # title of plot
                    bargap=0.01,  # gap between bars of adjacent location coordinates,
                    showlegend=False,

                    xaxis=dict(
                        showticklabels=False
                    ),
                    yaxis=dict(
                        showticklabels=False
                    ),

                    yaxis2=dict(
                        title="Price (USD)",
                        side="right"

                    )

                )

                fig.update_yaxes(nticks=20)
                fig.update_yaxes(side="right")
                fig.update_layout(height=800)

                config = {
                    'modeBarButtonsToAdd': ['drawline']
                }

                st.plotly_chart(fig, use_container_width=True, config=config)

    with right:

        summarytable = st.beta_container()
        with summarytable:
            urlfortable = 'https://stockanalysis.com/stocks/'+asset
            page = requests.get(urlfortable)
            doc = lh.fromstring(page.content)
            tr_elements = doc.xpath('//tr')
            i = 0
            i2 = 0
            tablecount = 0
            mylist1 = []
            mylist2 = []
            mylist3 = []
            mylist4 = []
            for tablecount in range(9):
                for t in tr_elements[tablecount]:
                    i += 1
                    if (i % 2) == 0:
                        value1 = t.text_content()
                        mylist1.append(str(value1))
                    else:
                        name1 = t.text_content()
                        mylist2.append(str(name1))

            for tablecount2 in range(9, 18):
                for t2 in tr_elements[tablecount2]:
                    i2 += 1
                    if (i2 % 2) == 0:
                        value2 = t2.text_content()
                        mylist3.append(str(value2))
                    else:
                        name2 = t2.text_content()
                        mylist4.append(str(name2))

            final_table = pd.DataFrame(
                {"": list(mylist2), "Value": list(mylist1), " ": list(mylist4), "Value ": list(mylist3)})
            final_table.index = [""] * len(final_table)
            st.title("Summary")
            st.table(final_table)


    urlq = 'https://stockanalysis.com/stocks/' + asset
    responseq = requests.get(urlq)
    soupq = BeautifulSoup(responseq.text, 'html.parser')

    samplenewscount = 0
    for samplenewscount in range(10):
        newsTitleq = soupq.find_all('div', {'class': 'news-side'})[samplenewscount].find('div').text
        newsThumbnailq = soupq.find_all('div', {'class': 'news-img'})[samplenewscount].find('img')
        newsBodyq = soupq.find_all('div', {'class': 'news-text'})[samplenewscount].find('p').text
        subMetaq = soupq.find_all('div', {'class': 'news-meta'})[samplenewscount].find_next('span').text
        hreflinkq = soupq.find_all('div', {'class': 'news-img'})[samplenewscount].find('a')
        linkq = hreflinkq.get('href')
        wapq = newsThumbnailq.get('data-src')


        chart1q, chart2q, chart3q = st.beta_columns([1, 2, 3])
        with chart1q:
            st.image(wapq)
        with chart2q:
            st.markdown(f"<h1 style='font-weight: bold; font-size: 17px;'>{newsTitleq}</h1>",
                        unsafe_allow_html=True)
            st.markdown(newsBodyq)
            linkq = "(" + linkq + ")"
            ayeq = '[[Link]]' + linkq
            st.markdown("Source: " + ayeq, unsafe_allow_html=True)
            st.text(" ")
            st.text(" ")

        with chart3q:
            st.markdown(subMetaq)

    st.text(" ")

elif menubar == 'News':
    with st.form(key='news_form'):
        col1, col2, col3, col4 = st.beta_columns([2, 2, 2, 1])
        with col1:
            attri = ['Company News', 'Stock Market News']
            query_paramsa1 = st.experimental_get_query_params()
            default1 = int(query_paramsa1["attributes"][0]) if "attributes" in query_paramsa1 else 0
            attributes = st.radio(
                'News',
                attri,
                index=default1
            )
            if attributes:
                st.experimental_set_query_params(attributes=attri.index(attributes))
        with col2:

            noList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                      16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
            query_paramsa2 = st.experimental_get_query_params()
            default2 = int(query_paramsa2["count"][0]) if "count" in query_paramsa2 else 9
            count = st.selectbox(
                'No. of News',
                noList,
                index=default2
            )
            if count:
                st.experimental_set_query_params(count=noList.index(count))

        with col3:
            sortList = ['Most Recent', 'Previous News']
            query_paramsa3 = st.experimental_get_query_params()
            default3 = int(query_paramsa3["sort"][0]) if "sort" in query_paramsa3 else 0
            sort = st.selectbox(
                'Sort',
                sortList,
                index=default3
            )

            if sort:
                st.experimental_set_query_params(sort=sortList.index(sort))

            if sort == 'Most Recent':
                DSort = (range(count))
            elif sort == 'Previous News':
                DSort = reversed((range(count)))

        with col4:
            st.markdown("")
            st.markdown("")
            submit_button = st.form_submit_button(label='Search')

    if attributes == "Company News":

        url = 'https://stockanalysis.com/stocks/' + asset
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        name = soup.find('h1', {'class': 'sa-h1'}).text

        x = 0
        for x in DSort:
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

            chart1, chart2, chart3 = st.beta_columns([1, 2, 1])
            with chart1:
                st.image(wap)
            with chart2:
                st.markdown(f"<h1 style='font-weight: bold; font-size: 17px;'>{newsTitle}</h1>",
                            unsafe_allow_html=True)
                st.markdown(newsBody)
                link = "(" + link + ")"
                aye = '[[Link]]' + link
                st.markdown("Source: " + aye, unsafe_allow_html=True)
                st.text(" ")
                st.text(" ")

            with chart3:
                st.markdown(subMeta)

        st.text(" ")

    elif attributes == "Stock Market News":

        url = 'https://stockanalysis.com/news'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1', {'class': 'entry-title'}).text

        x = 0
        for x in DSort:
            newsTitle1 = soup.find_all('div', {'class': 'news-side'})[x].find('div').text
            time1 = soup.find_all('div', {'class': 'news-meta'})[x].find('span').text
            newsThumbnail1 = soup.find_all('div', {'class': 'news-img'})[x].find('img')
            newsBody1 = soup.find_all('div', {'class': 'news-text'})[x].find('p').text
            hreflink1 = soup.find_all('div', {'class': 'news-img'})[x].find('a')
            link1 = hreflink1.get('href')
            newsimg1 = newsThumbnail1.get('data-src')

            chart1, chart2, chart3 = st.beta_columns([1, 2, 1])
            with chart1:
                st.image(newsimg1)
            with chart2:
                st.markdown(f"<h1 style='font-weight: bold; font-size: 17px;'>{newsTitle1}</h1>",
                            unsafe_allow_html=True)
                st.markdown(newsBody1)
                link1 = "(" + link1 + ")"
                concatclink = '[[Link]]' + link1
                st.markdown("Source: " + concatclink, unsafe_allow_html=True)
                st.text(" ")
                st.text(" ")

            with chart3:
                st.markdown(time1)

        st.text(" ")

elif menubar == 'Technical Indicators':
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
    dataMA = yf.download(asset, start, end)
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
    dataMACD = yf.download(asset, startMACD, endMACD)
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
    dataBoll = yf.download(asset, startBoll, endBoll)
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
elif menubar == 'Company Profile':
    ticker = yf.Ticker(asset)
    info = ticker.info

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
    df = yf.download(asset, start, end)
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

elif menubar == 'About':
    st.image('data//logo1.png')
else:
    st.error("Something has gone terribly wrong.")
