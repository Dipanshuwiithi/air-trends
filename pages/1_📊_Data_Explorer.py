import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Air Quality Dataset Explorer")

DATA_PATH = "data/india_city_aqi.parquet"

# ---------------- GET CITY LIST FAST ----------------
@st.cache_data
def get_city_list():
    # Read only City column (very fast)
    df = ppd.read_parquet(DATA_PATH, usecols=["City"])
    return sorted(df["City"].dropna().unique())

cities = get_city_list()

# ---------------- SIDEBAR FILTER ----------------
selected_city = st.sidebar.selectbox(
    "Select City",
    ["All Cities"] + cities
)


# ---------------- LOAD FILTERED DATA USING CHUNKS ----------------
@st.cache_data
def load_city_data(city):

    cols = [
        "City",
        "Datetime",
        "PM2_5_ugm3",
        "PM10_ugm3",
        "NO2_ugm3",
        "SO2_ugm3",
        "CO_ugm3",
        "O3_ugm3",
        "US_AQI"
    ]

    chunks = []

    for chunk in pd.read_parquet(
        DATA_PATH,
        usecols=cols,
        parse_dates=["Datetime"],
        chunksize=50000
    ):

        if city != "All Cities":
            chunk = chunk[chunk["City"] == city]

        chunks.append(chunk)

    df = pd.concat(chunks)

    return df


data = load_city_data(selected_city)

# ---------------- SUMMARY METRICS ----------------
st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Rows Loaded", f"{len(data):,}")
col2.metric("Cities Covered", data["City"].nunique())
col3.metric("Columns", len(data.columns))

st.markdown("---")


# ---------------- DAILY AGGREGATION ----------------
daily_avg = (
    data.set_index("Datetime")
        .resample("D")
        .mean(numeric_only=True)
        .reset_index()
)

st.subheader("Daily Aggregated Preview")

st.dataframe(daily_avg.head(500), use_container_width=True)


# ---------------- POLLUTANT DISTRIBUTION ----------------
st.markdown("---")

pollutant = st.selectbox(
    "Select Pollutant",
    [
        "PM2_5_ugm3",
        "PM10_ugm3",
        "NO2_ugm3",
        "SO2_ugm3",
        "CO_ugm3",
        "O3_ugm3",
        "US_AQI"
    ]
)

fig = px.histogram(
    daily_avg,
    x=pollutant,
    nbins=40,
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)


# ---------------- MISSING VALUES ----------------
st.markdown("---")
st.subheader("Missing Values Summary")

st.dataframe(daily_avg.isnull().sum())


# ---------------- DOWNLOAD BUTTON ----------------
st.download_button(
    "📥 Download Aggregated Dataset",
    daily_avg.to_csv(index=False),
    file_name="aggregated_air_quality.csv"
)