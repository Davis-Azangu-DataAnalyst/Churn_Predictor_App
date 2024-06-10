import streamlit as st
import uuid
import os
import joblib

# function to set up page configuration
st.set_page_config(
        page_title="Churn Prediction",
        page_icon="🤖",
        layout="wide",
    )

st.markdown("## **Churn Prediction**")
st.write("Enter the customer details below to predict churn:")

customer_features = {
    "Age": st.number_input("Age", min_value=18, max_value=100, value=30),
    "Gender": st.selectbox("Gender", ["Male", "Female"]),
    "Total_Purchase": st.number_input("Total Purchase", min_value=0, value=1000),
        # Add more features as needed
    }

    


        





