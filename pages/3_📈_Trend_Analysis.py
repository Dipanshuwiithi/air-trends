import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("📈 AQI Trend Analysis Dashboard")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_parquet("data/india_city_aqi.parquet")
    df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
    return df

data = load_data()

data = data.dropna(subset=["Datetime", "US_AQI"])

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.header("Trend Controls")

selected_cities = st.sidebar.multiselect(
    "Select Cities",
    sorted(data["City"].unique()),
    default=[data["City"].iloc[0]]
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [data["Datetime"].min(), data["Datetime"].max()]
)

rolling_window = st.sidebar.slider(
    "Smoothing Window (days)",
    1, 30, 7
)

pollutant_choice = st.sidebar.selectbox(
    "Select Metric",
    [
        "US_AQI",
        "PM2_5_ugm3",
        "PM10_ugm3",
        "NO2_ugm3",
        "SO2_ugm3",
        "CO_ugm3",
        "O3_ugm3"
    ]
)

# ---------------- FILTER DATA ----------------
filtered_data = data[
    (data["City"].isin(selected_cities)) &
    (data["Datetime"].dt.date >= date_range[0]) &
    (data["Datetime"].dt.date <= date_range[1])
]

# ---------------- SUMMARY METRICS ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Average AQI", round(filtered_data["US_AQI"].mean(), 2))
col2.metric("Maximum AQI", round(filtered_data["US_AQI"].max(), 2))
col3.metric("Minimum AQI", round(filtered_data["US_AQI"].min(), 2))

st.markdown("---")

# ---------------- INTERACTIVE TREND CHART ----------------
fig = go.Figure()

for city in selected_cities:

    city_data = filtered_data[filtered_data["City"] == city]
    city_data = city_data.sort_values("Datetime")

    smoothed = city_data[pollutant_choice].rolling(rolling_window).mean()

    fig.add_trace(
        go.Scatter(
            x=city_data["Datetime"],
            y=smoothed,
            mode="lines",
            name=city
        )
    )

# ---------------- AQI SEVERITY BANDS ----------------
if pollutant_choice == "US_AQI":

    fig.add_hrect(y0=0, y1=50, fillcolor="green", opacity=0.1)
    fig.add_hrect(y0=50, y1=100, fillcolor="yellow", opacity=0.1)
    fig.add_hrect(y0=100, y1=200, fillcolor="orange", opacity=0.1)
    fig.add_hrect(y0=200, y1=300, fillcolor="red", opacity=0.1)
    fig.add_hrect(y0=300, y1=500, fillcolor="purple", opacity=0.1)

# ---------------- LAYOUT SETTINGS ----------------
fig.update_layout(
    title=f"{pollutant_choice} Trend Over Time",
    xaxis_title="Date",
    yaxis_title=pollutant_choice,
    hovermode="x unified",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ---------------- POLLUTION ALERT ----------------
worst_city = filtered_data.sort_values("US_AQI", ascending=False).iloc[0]

st.warning(
    f"⚠ Highest AQI recorded: {worst_city['City']} "
    f"({round(worst_city['US_AQI'],2)}) on "
    f"{worst_city['Datetime'].date()}"
)