import streamlit as st
import os
import joblib
from pathlib import Path
import streamlit_authenticator as stauth

st.set_page_config(
    page_title='Home Page',
    page_icon='🏠',
    layout='wide'
)

# Try to load the hashed passwords
file_path = os.path.join("Assets", "hashed_pw.joblib")
try:
    with open(file_path, "rb") as file:
        hashed_passwords = joblib.load(file)
except FileNotFoundError:
    st.error("Hashed password file not found! Please ensure the file 'hashed_pw.pkl' exists in the correct directory.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the hashed passwords: {e}")
    st.stop()

# Verify the loaded hashed_passwords
if not isinstance(hashed_passwords, list):
    st.error("The loaded hashed passwords should be a list.")
    st.stop()

# Dummy data for names and usernames, replace these with actual data
names = ["Davis Azangu", "Donna Moguche"]
usernames = ["Max33", "Danna"]

# Convert usernames and hashed_passwords to a dictionary
credentials = dict(zip(usernames, hashed_passwords))

# Instantiate the authenticator
authenticator = stauth.Authenticate(names, credentials, "1234", cookie_expiry_days=10)

# Your Streamlit app code goes here
st.title("Churn Predictor Web App")
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.write(f"Welcome {name}!")
    def home_page():
        image_filename = 'home.png'
        home_image_path = os.path.join('Assets', 'home.png')
        st.image(home_image_path, use_column_width=False)

    # Sidebar Navigation and logout
    # authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")

    # Example function call to display home page
    home_page()

    st.markdown("## **This is a Streamlit app for predicting churn.**")
    st.write("**Features:**")
    st.write("- Predict customer churn based on various features.")
    st.write("- Allow users to log in and create accounts.")
    st.write("- Provide interactive visualizations of churn prediction results.")
    st.write("**Benefits:**")
    st.write("- Helps businesses identify customers at risk of churning.")
    st.write("- Enables proactive retention strategies to reduce churn.")
    st.write("- Streamlines the churn prediction process with a user-friendly interface.")
    st.write("**Machine Learning Integrations:**")
    st.write("- Utilizes machine learning models for churn prediction.")
    st.write("- Supports algorithms like Linear Regression and K-Nearest Neighbors (KNN) models.")

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")

