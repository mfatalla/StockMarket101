import pandas as pd
import streamlit as st

df = pd.DataFrame({"x": [1, 2, 3, 4], "y": list("abcd")})

# set index to empty strings

df.index = [""] * len(df)
st.table(df)
