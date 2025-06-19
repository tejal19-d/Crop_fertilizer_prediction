import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load models and label encoder
crop_model = pickle.load(open('crop_model.pkl', 'rb'))
fert_model = pickle.load(open('fertilizer_model.pkl', 'rb'))  # Optional

try:
    le = pickle.load(open('label_encoder.pkl', 'rb'))
except:
    le = None

# Set up Streamlit
st.set_page_config(page_title="Agri Advisor", layout="wide")
st.title("🌾 Smart Agriculture Advisor")
st.sidebar.title("🔍 Navigation")

option = st.sidebar.radio("Go to:", ["Home", "Crop Recommendation", "Fertilizer Recommendation"])

if option == "Home":
    st.header("Welcome to the Smart Agriculture Advisor 🌿")
    st.write("""
        This tool helps farmers and agricultural experts:
        - 📈 Choose the best crop to cultivate based on soil & climate
        - 💊 Recommend the right fertilizer based on deficiencies

        Built using machine learning models trained on agricultural data.
    """)

elif option == "Crop Recommendation":
    st.header("🌱 Crop Recommendation System")

    col1, col2 = st.columns(2)

    with col1:
        N = st.number_input("Nitrogen (N)", 0, 200)
        P = st.number_input("Phosphorus (P)", 0, 200)
        K = st.number_input("Potassium (K)", 0, 200)
        temp = st.number_input("Temperature (°C)", 0.0, 60.0)
    with col2:
        humidity = st.number_input("Humidity (%)", 0.0, 100.0)
        ph = st.number_input("pH Level", 0.0, 14.0)
        rainfall = st.number_input("Rainfall (mm)", 0.0, 300.0)

    if st.button("Recommend Crop"):
        data = np.array([[N, P, K, temp, humidity, ph, rainfall]])
        prediction = crop_model.predict(data)[0]

        if le:
            crop_name = le.inverse_transform([prediction])[0]
        else:
            crop_name = str(prediction)

        st.success(f"✅ Recommended Crop: **{crop_name.upper()}**")

elif option == "Fertilizer Recommendation":
    st.header("💊 Fertilizer Recommendation System")

    crops = ['rice', 'wheat', 'maize', 'cotton', 'millets', 'barley', 'oil seeds', 'pulses']
    crop_name = st.selectbox("Select Crop", crops)

    N = st.number_input("Nitrogen (N)", 0, 200)
    P = st.number_input("Phosphorus (P)", 0, 200)
    K = st.number_input("Potassium (K)", 0, 200)

    if st.button("Recommend Fertilizer"):
        # You can improve this by replacing with fert_model.predict()
        if N < 50:
            st.info("🧪 Add Urea-based fertilizers (N-deficiency)")
        elif P < 50:
            st.info("🧪 Add Superphosphate (P-deficiency)")
        elif K < 50:
            st.info("🧪 Add Potash-based fertilizers (K-deficiency)")
        else:
            st.success("✅ Soil nutrient levels are sufficient.")
