import streamlit as st
import requests
from bs4 import BeautifulSoup

def news(tickerinput):
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

        url = 'https://stockanalysis.com/stocks/' + tickerinput
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
                st.markdown(f"<h1 style='font-weight: bold; font-size: 17px;'>{newsTitle1}</h1>", unsafe_allow_html=True)
                st.markdown(newsBody1)
                link1 = "(" + link1 + ")"
                concatclink = '[[Link]]' + link1
                st.markdown("Source: " + concatclink, unsafe_allow_html=True)
                st.text(" ")
                st.text(" ")

            with chart3:
                st.markdown(time1)

        st.text(" ")


