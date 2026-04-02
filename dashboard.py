import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AirSense",
    layout="wide",
    page_icon=""
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#020617,#0f172a);
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* Sidebar title */
.sidebar-title {
    font-size: 26px;
    font-weight: 700;
    background: linear-gradient(90deg,#38bdf8,#22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Section labels */
.section-label {
    font-size: 13px;
    color: #94a3b8;
    margin-top: 14px;
}

/* Header title */
.app-header {
    font-size: 36px;
    font-weight: 700;
    background: linear-gradient(90deg,#38bdf8,#22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Glass cards */
.metric-card {
    background: rgba(255,255,255,0.04);
    padding: 25px;
    border-radius: 16px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#22c55e,#06b6d4);
    color: white;
    border-radius: 10px;
    border: none;
}

/* Footer nav buttons */
.footer-btn button {
    width: 100%;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">AirSense</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-label">DATA</div>',
        unsafe_allow_html=True
    )

    st.page_link("pages/1_📊_Data_Explorer.py", label="Data Explorer")
    st.page_link("pages/2_🗺️_AQI_Map.py", label="AQI Map")

    st.markdown(
        '<div class="section-label">ANALYTICS</div>',
        unsafe_allow_html=True
    )

    st.page_link("pages/3_📈_Trend_Analysis.py", label="Trend Analysis")

    st.markdown(
        '<div class="section-label">AI MODULE</div>',
        unsafe_allow_html=True
    )

    st.page_link("pages/4_🤖_AQI_Prediction.py", label="AQI Prediction")

# ---------------- HEADER ----------------
col1, col2 = st.columns([8, 1])

with col1:
    st.markdown(
        '<div class="app-header">AirSense – AI Air Quality Forecasting</div>',
        unsafe_allow_html=True
    )

with col2:
    st.success("API Status: OK")

st.markdown("---")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/india_city_aqi.csv")
    df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
    return df

data = load_data()

# ---------------- AI FORECAST PANEL ----------------
st.subheader("🔮 AI-Powered Forecasting")

col1, col2, col3, col4 = st.columns([4,1,1,2])

with col1:
    selected_city = st.selectbox(
        "Cities to Forecast",
        sorted(data["City"].unique())
    )

with col2:
    forecast_days = st.number_input("Forecast Horizon", value=5)

with col3:
    training_window = st.number_input("Training Window", value=30)

with col4:
    generate_forecast = st.button("Generate Forecast")

# ---------------- METRIC CARDS ----------------
city_data = data[data["City"] == selected_city]

latest_aqi = city_data["US_AQI"].dropna().iloc[-1]
avg_pm25 = city_data["PM2_5_ugm3"].mean()

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h4>{selected_city}</h4>
        <h2>{round(latest_aqi,2)} AQI</h2>
        <p>Forecast horizon: {forecast_days} days</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h4>Average PM2.5</h4>
        <h2>{round(avg_pm25,2)} µg/m³</h2>
        <p>Training window: {training_window} days</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------- FOOTER NAV BAR ----------------
st.markdown("### Quick Navigation")

col1, col2, col3, col4 = st.columns(4)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.page_link(
        "pages/1_📊_Data_Explorer.py",
        label="📊 Data Explorer"
    )

with col2:
    st.page_link(
        "pages/2_🗺️_AQI_Map.py",
        label="🗺️ City Analysis"
    )

with col3:
    st.page_link(
        "pages/3_📈_Trend_Analysis.py",
        label="📈 Trend Analysis"
    )

with col4:
    st.page_link(
        "pages/4_🤖_AQI_Prediction.py",
        label="🤖 AQI Forecast"
    )