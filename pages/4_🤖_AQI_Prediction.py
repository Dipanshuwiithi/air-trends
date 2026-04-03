import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from utils.load_data import load_data

st.title("🤖 AQI Prediction Model")

data = load_data()

features = [
    "PM2_5_ugm3",
    "PM10_ugm3",
    "NO2_ugm3",
    "CO_mg_m3",
    "O3_ugm3"
]

target = "US_AQI"

model_data = data.dropna(subset=features + [target])

X = model_data[features]
y = model_data[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor()

model.fit(X_train, y_train)

st.subheader("Enter Pollutant Values")

inputs = {}

for feature in features:
    inputs[feature] = st.number_input(feature, value=10.0)

if st.button("Predict AQI"):

    prediction = model.predict([list(inputs.values())])[0]

    st.success(f"Predicted AQI: {round(prediction, 2)}")