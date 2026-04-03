import streamlit as st
import plotly.express as px
from utils.load_data import load_data

st.title("📈 AQI Trend Analysis")

data = load_data()

cities = sorted(data["City"].unique())

city = st.sidebar.selectbox("Select City", cities)

city_data = data[data["City"] == city]

city_data = city_data.dropna(subset=["Datetime", "US_AQI"])

fig = px.line(
    city_data,
    x="Datetime",
    y="US_AQI",
    title=f"AQI Trend for {city}"
)

st.plotly_chart(fig, width="stretch")