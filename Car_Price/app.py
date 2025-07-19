import streamlit as st
import pandas as pd
import pickle
import datetime
import os

# === Load model ===
model_path = os.path.join(os.path.dirname(__file__), 'car2.sav')
model = pickle.load(open(model_path, 'rb'))

# === Load local CSS if available ===
def load_local_css(file_name):
    try:
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ style.css not found. Default styling applied.")

load_local_css("style.css")

# === Brand encoding map ===
brand_map = {
    'Maruti': 1, 'Skoda': 2, 'Honda': 3, 'Hyundai': 4, 'Toyota': 5,
    'Ford': 6, 'Renault': 7, 'Mahindra': 8, 'Tata': 9, 'Chevrolet': 10,
    'Fiat': 11, 'Datsun': 12, 'Jeep': 13, 'Mercedes-Benz': 14, 'Mitsubishi': 15,
    'Audi': 16, 'Volkswagen': 17, 'BMW': 18, 'Nissan': 19, 'Lexus': 20,
    'Jaguar': 21, 'Land': 22, 'MG': 23, 'Volvo': 24, 'Daewoo': 25,
    'Kia': 26, 'Force': 27, 'Ambassador': 28, 'Ashok': 29, 'Isuzu': 30,
    'Opel': 31, 'Peugeot': 32
}

# === UI Title ===
st.markdown("<h1 style='text-align: center; color: navy;'>🚗 Car Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("---")

# === Input Fields ===
st.markdown("### 🧾 Enter Car Details:")
col1, col2 = st.columns(2)

with col1:
    brand = st.selectbox("Car Brand", sorted(brand_map.keys()))
    seats = st.number_input("Number of Seats", min_value=2, max_value=10, step=1)
    fuel = st.selectbox("Fuel Type", ['Petrol', 'Diesel', 'Electric', 'Hybrid'])
    transmission = st.radio("Transmission", ['Manual', 'Automatic'])

with col2:
    km_driven = st.slider("KM Driven", 0, 300000, 30000, step=1000)
    engine = st.slider("Engine Size (cc)", 500, 5000, 1200, step=100)
    max_power = st.slider("Max Power (bhp)", 20, 500, 100, step=5)
    mileage = st.slider("Mileage (km/l)", 0.0, 40.0, 15.0, step=0.1)
    year = st.slider("Manufacturing Year", 2000, datetime.datetime.now().year, 2018)

# === Predict Button ===
if st.button("🔍 Predict Price"):
    try:
        brand_code = brand_map[brand]
        fuel_code = {'Petrol': 0, 'Diesel': 1, 'Electric': 2, 'Hybrid': 3}[fuel]
        transmission_code = {'Manual': 0, 'Automatic': 1}[transmission]

        input_df = pd.DataFrame([[
            year,
            km_driven,
            fuel_code,
            transmission_code,
            mileage,
            engine,
            max_power,
            seats,
            brand_code
        ]], columns=[
            'year', 'km_driven', 'fuel', 'transmission', 'mileage',
            'engine', 'max_power', 'seats', 'Brand_Code'
        ])

        predicted_price = model.predict(input_df)[0]
        st.success(f"💰 **Predicted Selling Price**: ₹ {predicted_price:,.2f}")
        st.balloons()
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
