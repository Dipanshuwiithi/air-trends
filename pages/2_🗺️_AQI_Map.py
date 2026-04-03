import streamlit as st
import pydeck as pdk
from utils.load_data import load_data

st.title("🗺️ AQI Map")

data = load_data()

latest = (
    data.sort_values("Datetime")
        .groupby("City")
        .tail(1)
)

latest = latest.dropna(subset=["Latitude", "Longitude", "US_AQI"])

st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=22.9734,
            longitude=78.6569,
            zoom=4,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=latest,
                get_position="[Longitude, Latitude]",
                get_color="[200, 30, 0, 160]",
                get_radius=40000,
            )
        ],
    )
)