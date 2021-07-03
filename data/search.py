import requests
import lxml.html as lh
import pandas as pd
import streamlit as st
import yfinance as yf


urlfortable='https://stockanalysis.com/stocks/aapl/'

page = requests.get(urlfortable)

doc = lh.fromstring(page.content)

tr_elements = doc.xpath('//tr')


col=[]
i=0
x =5
mylist1 = []
mylist2 = []
for x in range(10):
    for t in tr_elements[x]:
        i+=1
        if (i%2)==0:
            value = t.text_content()
            mylist1.append(str(value))
        else:
            name = t.text_content()
            mylist2.append(str(name))


final_table = pd.DataFrame({"x": list(mylist2), "y": list(mylist1)})

# set index to empty strings

final_table.index = [""] * len(final_table)
st.table(final_table)

st.write(mylist2[9])
st.write(mylist1[9])

