import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Dataset Explorer", page_icon="📊", layout="wide")

st.title("📊 Dataset Explorer")
st.markdown("Explore city-wise air quality data interactively.")

# ---------------- DATA PATH ----------------
DATA_PATH = "data/india_city_aqi.parquet"


# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_parquet(DATA_PATH)
    df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
    return df


# ---------------- LOAD CITY LIST ONLY ----------------
@st.cache_data
def get_city_list():
    df = pd.read_parquet(DATA_PATH, columns=["City"])
    return sorted(df["City"].dropna().unique())


# Load city list
cities = get_city_list()


# ---------------- SIDEBAR FILTER ----------------
st.sidebar.header("🔎 Filters")

selected_city = st.sidebar.selectbox(
    "Select City",
    cities
)


# ---------------- LOAD FILTERED DATA ----------------
data = load_data()

filtered_data = data[data["City"] == selected_city]


# ---------------- DATA OVERVIEW ----------------
st.subheader(f"📍 Air Quality Data for {selected_city}")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(filtered_data))
col2.metric("Start Date", str(filtered_data["Datetime"].min())[:10])
col3.metric("Latest Date", str(filtered_data["Datetime"].max())[:10])


# ---------------- SHOW DATA TABLE ----------------
st.subheader("📄 Dataset Preview")

st.dataframe(
    filtered_data.sort_values("Datetime", ascending=False),
    use_container_width=True
)


# ---------------- COLUMN SELECTOR ----------------
st.subheader("📊 Explore Specific Pollutants")

numeric_columns = filtered_data.select_dtypes(include="number").columns.tolist()

selected_column = st.selectbox(
    "Choose pollutant column",
    numeric_columns
)


# ---------------- STATISTICS ----------------
st.subheader("📈 Summary Statistics")

st.write(filtered_data[selected_column].describe())


# ---------------- HISTOGRAM ----------------
import plotly.express as px

fig = px.histogram(
    filtered_data,
    x=selected_column,
    nbins=50,
    title=f"Distribution of {selected_column} in {selected_city}"
)

st.plotly_chart(fig, use_container_width=True)


# ---------------- DOWNLOAD OPTION ----------------
st.subheader("⬇️ Download Filtered Data")

csv = filtered_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name=f"{selected_city}_aqi_data.csv",
    mime="text/csv"
)