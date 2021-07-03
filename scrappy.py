
import streamlit as st

import requests
import yfinance as yf
from bs4 import BeautifulSoup


def Scrappy(tickerinput):
    ticker = yf.Ticker(tickerinput)
    info = ticker.info
    url = 'https://stockanalysis.com/stocks/'+tickerinput
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    name = soup.find('h1', {'class': 'sa-h1'}).text
    price = soup.find('span', {'id': 'cpr'}).text
    currency = soup.find('span', {'id': 'cpr'}).find_next('span').text
    change = soup.find('span', {'id': 'spd'}).text
    rate = soup.find('span', {'id': 'spd'}).find_next('span').text
    meta = soup.find('div', {'id': 'sti'}).find('span').text
    meta = soup.find('div', {'id': 'sti'}).find('span').text
    after = soup.find('div', {'id': 'ext'}).find_next('span').text
    after2 = soup.find('span', {'id': 'extc'}).text
    aftert = soup.find('span', {'id': 'extcp'}).text
    aftertime = soup.find('span', {'id': 'exttime'}).text
    CR = change+" ("+rate+")"
    CT = after2+" ("+aftert+")"
    sub = change
    sub2 = after2
    aye = ": After-hours"


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

            st.markdown(f"<p style='vertical-align:bottom;font-weight: italic; color: #FFFFFF;font-size: 10px;'>{meta}</p>",
                        unsafe_allow_html=True)
            if float(sub2) > 0:

                st.markdown(after + " " + currency)
                st.markdown(
                    f"<p style='vertical-align:bottom;font-weight: bold; color: #00AC4A;font-size: 13px;'>{CT+aye}</p>",
                    unsafe_allow_html=True)


            else:
                st.markdown(after + " " + currency)
                st.markdown(
                    f"<p style='vertical-align:bottom;font-weight: bold; color: #D10000;;font-size: 13px;'>{CT+aye}</p>",
                    unsafe_allow_html=True)

            st.markdown(f"<p style='vertical-align:bottom;font-weight: italic; color: #FFFFFF;font-size: 10px;'>{aftertime}</p>",
                        unsafe_allow_html=True)
            submitted = st.form_submit_button("")
