import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("🗺️ AQI Geographic Visualization")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_parquet("data/india_city_aqi.parquet")

    # Convert datetime once
    df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")

    # Keep only latest reading per city (prevents huge map payload)
    df = (
        df.sort_values("Datetime")
          .groupby("City")
          .tail(1)
    )

    return df

data = load_data()

# Remove missing coordinates
data = data.dropna(subset=["Latitude", "Longitude", "US_AQI"])


# ---------------- AQI COLOR FUNCTION ----------------
def get_color(aqi):
    if aqi <= 50:
        return [0, 255, 0]
    elif aqi <= 100:
        return [255, 255, 0]
    elif aqi <= 200:
        return [255, 165, 0]
    elif aqi <= 300:
        return [255, 0, 0]
    else:
        return [128, 0, 128]


data["color"] = data["US_AQI"].apply(get_color)


# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.header("Map Controls")

selected_city = st.sidebar.selectbox(
    "Select City",
    ["All Cities"] + sorted(data["City"].unique())
)

show_heatmap = st.sidebar.checkbox("Enable Heatmap Layer (slower)")


# ---------------- FILTER DATA ----------------
if selected_city != "All Cities":
    filtered_data = data[data["City"] == selected_city]
else:
    filtered_data = data


# ---------------- MAP CENTER ----------------
view_state = pdk.ViewState(
    latitude=filtered_data["Latitude"].mean(),
    longitude=filtered_data["Longitude"].mean(),
    zoom=4,
    pitch=40,
)


# ---------------- SCATTER LAYER ----------------
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_data,
    get_position=["Longitude", "Latitude"],
    get_fill_color="color",
    get_radius="US_AQI * 20",
    pickable=True,
)


# ---------------- OPTIONAL HEATMAP ----------------
layers = [scatter_layer]

if show_heatmap and len(filtered_data) < 8000:

    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=filtered_data,
        get_position=["Longitude", "Latitude"],
        get_weight="US_AQI",
        radiusPixels=60,
    )

    layers.append(heatmap_layer)


# ---------------- RENDER MAP ----------------
st.pydeck_chart(
    pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={"text": "City: {City}\nAQI: {US_AQI}"}
    )
)


# ---------------- AQI LEGEND ----------------
st.markdown("""
### 📊 AQI Severity Legend

🟢 **Good (0–50)**  
🟡 **Moderate (51–100)**  
🟠 **Unhealthy (101–200)**  
🔴 **Very Unhealthy (201–300)**  
🟣 **Hazardous (300+)**
""")


# ---------------- LATEST AQI METRIC ----------------
latest_entry = filtered_data.sort_values("Datetime").iloc[-1]

st.metric(
    label=f"Latest AQI in {latest_entry['City']}",
    value=round(latest_entry["US_AQI"], 2)
)