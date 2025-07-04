# app.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model and columns
model = joblib.load('pollution_model.pkl')
columns = joblib.load('model_columns.pkl')

# Pollutants and safety limits (from your PDF)
safety_limits = {
    'O2': (5, 'min'),        # Dissolved Oxygen > 5 mg/L
    'NO3': (10, 'max'),
    'NO2': (0.1, 'max'),
    'SO4': (250, 'max'),
    'PO4': (0.1, 'max'),
    'CL': (250, 'max')
}

pollutants = list(safety_limits.keys())

# Streamlit App
st.title("💧 Water Pollution Prediction")
st.markdown("Predicts future pollutant levels at water stations.")

# Inputs
station_id = st.selectbox("Select Station ID", [str(i) for i in range(1, 23)])
year_input = st.number_input("Enter Year (future/present)", min_value=2022, max_value=2100, value=2025)

if st.button("Predict"):
    # Prepare input
    input_df = pd.DataFrame({'year': [year_input], 'id': [station_id]})
    input_encoded = pd.get_dummies(input_df, columns=['id'])
    
    # Add missing dummy columns
    missing_cols = set(columns) - set(input_encoded.columns)
    for col in missing_cols:
        input_encoded[col] = 0
    input_encoded = input_encoded[columns]  # Align column order

    # Predict
    predicted = model.predict(input_encoded)[0]

    st.subheader(f"Predicted Pollutants for Station {station_id} in {year_input}")
    for i, pollutant in enumerate(pollutants):
        value = predicted[i]
        limit, condition = safety_limits[pollutant]

        # Determine status
        if (condition == 'max' and value <= limit) or (condition == 'min' and value >= limit):
            status = f"✅ Safe"
            color = "green"
        else:
            status = f"❌ Unsafe"
            color = "red"

        st.markdown(f"**{pollutant}**: {value:.2f} mg/L — :{color}[{status}]")

