import pandas as pd
import streamlit as st
import requests
import yfinance as yf
from bs4 import BeautifulSoup
import profile
import overview
import lxml.html as lh
import technical
import line_chart
import candlestick

st.set_page_config(
    page_title = 'SLAPSOIL',
    page_icon = '💜',
    layout= 'wide',
    initial_sidebar_state="expanded",
)

def load_data():
    components = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S" "%26P_500_companies"
    )[0]
    return components.drop("SEC filings", axis=1).set_index("Symbol")


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

    inputtab = st.sidebar.beta_container()
    with inputtab:
        with st.form("my_form"):
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
            submitted = st.form_submit_button("")



    if menubar == 'Overview':
        left, right = st.beta_columns([1,1])
        with left:
            st.title("Line Chart")
            line_chart.line_chart(asset)
            st.title("Candlestick Chart")
            candlestick.candlestick(asset)


        with right:
            st.write("")
            st.write("")
            st.write("")

            urlfortable = 'https://stockanalysis.com/stocks/aapl/'

            page = requests.get(urlfortable)

            doc = lh.fromstring(page.content)

            tr_elements = doc.xpath('//tr')

            col = []
            i = 0
            x = 0

            mylist1 = []
            mylist2 = []
            for x in range(8):
                for t in tr_elements[x]:
                    i += 1
                    if (i % 2) == 0:
                        value = t.text_content()
                        mylist1.append(str(value))
                    else:
                        name = t.text_content()
                        mylist2.append(str(name))

            final_table = pd.DataFrame({"x": list(mylist2), "y": list(mylist1)})

            # set index to empty strings

            final_table.index = [""] * len(final_table)
            st.table(final_table)

        url = 'https://stockanalysis.com/stocks/' + asset
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
