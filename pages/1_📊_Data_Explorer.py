import streamlit as st
import plotly.express as px
from utils.load_data import load_data

st.title("📊 Dataset Explorer")

data = load_data()

cities = sorted(data["City"].dropna().unique())

selected_city = st.sidebar.selectbox("Select City", cities)

filtered = data[data["City"] == selected_city]

st.subheader(f"Air Quality Data for {selected_city}")

col1, col2, col3 = st.columns(3)

col1.metric("Records", len(filtered))
col2.metric("Start Date", str(filtered["Datetime"].min())[:10])
col3.metric("End Date", str(filtered["Datetime"].max())[:10])

st.dataframe(filtered, width="stretch")

numeric_cols = filtered.select_dtypes("number").columns

selected_col = st.selectbox("Select Pollutant", numeric_cols)

fig = px.histogram(filtered, x=selected_col)

st.plotly_chart(fig, width="stretch")