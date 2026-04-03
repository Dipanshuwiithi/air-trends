import streamlit as st
from utils.load_data import load_data

st.set_page_config(
    page_title="AirSense Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 AirSense Dashboard")
st.markdown("Interactive Air Quality Monitoring & Prediction System")

data = load_data()

st.subheader("📊 Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(data))
col2.metric("Cities Covered", data["City"].nunique())
col3.metric("Latest AQI", int(data["US_AQI"].dropna().iloc[-1]))

st.markdown("Use sidebar to explore pages ➡️")