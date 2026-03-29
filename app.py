import streamlit as st
import joblib
import numpy as np

st.set_page_config(page_title="Fastag Fraud Detection", layout="wide")

st.title("🚧 Fastag Fraud Detection System")
st.write("Enter transaction details to check whether the FASTag transaction is valid or fraud.")

model = joblib.load("model.pkl")


# ======================
# Transaction Info
# ======================

st.header("Transaction Information")

col1, col2 = st.columns(2)

with col1:
    Transaction_Amount = st.number_input("Transaction Amount (₹)", min_value=0.0)
    Amount_paid = st.number_input("Amount Paid (₹)", min_value=0.0)
    

with col2:
    Hour = st.slider("Hour of Transaction", 0, 23)
    Month = st.slider("Month", 1, 12)
    DayOfWeek = st.selectbox(
        "Day of Week",
        ["Monday", "Tuesday", "Wednesday",
         "Thursday", "Friday", "Saturday", "Sunday"]
    )

    Vehicle_Type = st.selectbox(
        "Vehicle Type",
        ["Car", "Truck", "Bus", "Motercycle","SUV","Sedan","Van"]
    )

    Lane_Type = st.selectbox(
        "Lane Type",
        [ "Regular", "Express"]
    )


# ======================
# Extra Details
# ======================

st.header("Location & Extra Details")

col3, col4 = st.columns(2)

with col3:

    TollBoothID = st.text_input(
        "Toll Booth ID (Example: A-102, B-103)"
    )

    Vehicle_Speed = st.number_input(
        "Vehicle Speed",
        min_value=0
    )


    Vehicle_Dimensions = st.selectbox(
        "Vehicle Dimensions",
        ["Small", "Medium", "Large", "Extra Large"]
    )

with col4:

    state = st.selectbox(
        "State",
        ["KA", "MH", "DL", "TN", "UP"]
    )


# ======================
# Encoding
# ======================

state_dict = {
    "KA":0,
    "MH":1,
    "DL":2,
    "TN":3,
    "UP":4
}

vehicle_dict = {
    "Car":0,
    "Truck":1,
    "Bus":2,
    "Bike":3,
    "Motercycle": 4,
    "SUV":5,
    "Sedan":6,
    "Van":7

}

Lane_Type_dict = {
     "Regular":0,
    "Express":1,
    
}

dimension_dict = {
    "Small":0,
    "Medium":1,
    "Large":2,
    "Extra Large":3
}

DayOfWeek_dict = {
    "Monday":0,
    "Tuesday":0,
    "Wednesday":0,
    "Thursday":0,
    "Friday":0,
    "Saturday":1,
    "Sunday":1
}


State_Code = state_dict[state]
Vehicle_Type = vehicle_dict[Vehicle_Type]
Lane_Type = Lane_Type_dict[Lane_Type]
Vehicle_Dimensions = dimension_dict[Vehicle_Dimensions]
DayOfWeek = DayOfWeek_dict[DayOfWeek]

# toll text → number
TollBoothID = abs(hash(TollBoothID)) % 1000


# ======================
# Prediction
# ======================

st.markdown("---")

if st.button("Check Transaction"):

    data = np.array([[Transaction_Amount,
                      Amount_paid,
                      Hour,
                      Month,
                      DayOfWeek,
                      Vehicle_Type,
                      Lane_Type,
                      TollBoothID,
                      Vehicle_Speed,
                      Vehicle_Dimensions,
                      State_Code]])

    pred = model.predict(data)

    if pred[0] == 1:
        st.error("⚠ Fraud Transaction Detected")
    else:
        st.success("✅ Valid Transaction")

st.write(Transaction_Amount,
         Amount_paid,
         Vehicle_Type,
         Lane_Type,
         TollBoothID,
         Hour,
         Month,
         DayOfWeek,
         Vehicle_Speed,
         Vehicle_Dimensions,
         State_Code)