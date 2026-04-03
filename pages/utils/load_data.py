import streamlit as st
import pandas as pd

DATA_PATH = "data/india_city_aqi.parquet"

@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_parquet(DATA_PATH)
    df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
    return df