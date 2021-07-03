import requests
import yfinance as yf
from bs4 import BeautifulSoup
import streamlit as st




url = 'https://stockanalysis.com/stocks/TSLA'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

name = soup.find('h1', {'class': 'sa-h1'}).text

x = 0
for x in range(5):
    # altwrap > div > div:nth-child(7) >
    vidTitle = soup.find_all('div', {'class': 'news-video'})[x].find('h3')
    #vidBody = soup.find_all('div', {'class': 'news-text'})[x].find('p').text
    #vidTime = soup.find_all('span', {'class': 'news-time'})[x].find('span')
    #vidTN = soup.find_all('div', {'class': 'news-video'})[x].find_next('iframe')
    #vidLink = vidTN.get('src')


    #print(vidLink)
    print(vidTitle)
    #print(vidBody)
    #print(vidTime)
    print("")

    #st.video(vidLink)

vid = soup.find_all('div', {'class': 'news-video'})[5].find('div').text
print(vid)






