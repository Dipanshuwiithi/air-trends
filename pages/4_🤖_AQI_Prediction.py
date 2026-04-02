import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

st.title("🤖 AI-Based AQI Prediction System")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/india_city_aqi.csv")
    return df

data = load_data()

features = [
    "PM2_5_ugm3",
    "PM10_ugm3",
    "NO2_ugm3",
    "SO2_ugm3",
    "CO_ugm3",
    "O3_ugm3"
]

target = "US_AQI"

model_data = data[features + [target]].dropna()


# ---------------- TRAIN MODEL ----------------
@st.cache_resource
def train_model():

    X = model_data[features]
    y = model_data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=80,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    return model, rmse, r2


model, rmse, r2 = train_model()

# ---------------- MODEL PERFORMANCE ----------------
col1, col2 = st.columns(2)

col1.metric("Model RMSE", round(rmse, 2))
col2.metric("Model R² Score", round(r2, 3))

st.markdown("---")


# ---------------- USER INPUT PANEL ----------------
st.subheader("Enter Pollutant Values")

col1, col2, col3 = st.columns(3)

pm25 = col1.number_input("PM2.5 (µg/m³)", 0.0)
pm10 = col2.number_input("PM10 (µg/m³)", 0.0)
no2 = col3.number_input("NO2 (µg/m³)", 0.0)

col4, col5, col6 = st.columns(3)

so2 = col4.number_input("SO2 (µg/m³)", 0.0)
co = col5.number_input("CO (µg/m³)", 0.0)
o3 = col6.number_input("O3 (µg/m³)", 0.0)


# ---------------- AQI CATEGORY FUNCTION ----------------
def aqi_category(aqi):

    if aqi <= 50:
        return "🟢 Good"
    elif aqi <= 100:
        return "🟡 Moderate"
    elif aqi <= 200:
        return "🟠 Unhealthy"
    elif aqi <= 300:
        return "🔴 Very Unhealthy"
    else:
        return "🟣 Hazardous"


# ---------------- PREDICTION ----------------
if st.button("Predict AQI"):

    prediction = model.predict([[pm25, pm10, no2, so2, co, o3]])[0]

    category = aqi_category(prediction)

    st.success(f"Predicted AQI: {round(prediction,2)}")
    st.info(f"AQI Category: {category}")


# ---------------- FEATURE IMPORTANCE ----------------
st.markdown("---")
st.subheader("Feature Importance Analysis")

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

fig = px.bar(
    importance_df,
    x="Feature",
    y="Importance",
    color="Importance",
    template="plotly_dark",
    title="Pollutant Contribution to AQI"
)

st.plotly_chart(fig, use_container_width=True)