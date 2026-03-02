import streamlit as st
import pandas as pd
import pickle

# Load the model and encoder
model = pickle.load(open('factory_guard_model.pkl', 'rb'))
le = pickle.load(open('encoder.pkl', 'rb'))

st.title("🛡️ FactoryGuard AI: Predictive Maintenance")
st.write("Enter machine parameters to predict potential failure.")

# Create input fields for the user
col1, col2 = st.columns(2)

with col1:
    m_type = st.selectbox("Machine Type", ["L", "M", "H"])
    air_temp = st.number_input("Air Temperature [K]", value=300.0)
    proc_temp = st.number_input("Process Temperature [K]", value=310.0)

with col2:
    speed = st.number_input("Rotational Speed [rpm]", value=1500)
    torque = st.number_input("Torque [Nm]", value=40.0)
    wear = st.number_input("Tool Wear [min]", value=0)

# Prediction Logic
if st.button("Predict Status"):
    # Preprocess the input
    type_encoded = le.transform([m_type])[0]
    features = pd.DataFrame([[type_encoded, air_temp, proc_temp, speed, torque, wear]], 
                            columns=['Type', 'Air temperature_K', 'Process temperature_K', 'Rotational speed_rpm', 'Torque_Nm', 'Tool wear_min'])
    
    prediction = model.predict(features)
    
    if prediction[0] == 1:
        st.error("⚠️ WARNING: Machine Failure Predicted!")
    else:
        st.success("✅ Machine is operating normally.")
