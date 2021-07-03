import yfinance as yf
import streamlit as st

@st.cache(allow_output_mutation=True)
def load_quotes(asset):
    return yf.download(asset)


def line_chart(asset):


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
    st.line_chart(data2, height= 400)
    if st.checkbox("View quotes"):
        st.subheader(f"{asset} historical data")
        st.write(data2)
