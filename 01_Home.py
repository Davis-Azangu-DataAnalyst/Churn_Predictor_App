import streamlit as st
import os
import joblib
from pathlib import Path
import streamlit_authenticator as stauth
import bcrypt

st.set_page_config(
    page_title='Home Page',
    page_icon='🏠',
    layout='wide'
)

# Define the file path correctly
file_path = Path(__file__).parent / "Assets" / "hashed_pw.joblib"

# Load hashed passwords from the file
with file_path.open("rb") as file:
    hashed_passwords = joblib.load(file)

# Dummy data for usernames and names to correspond with the hashed passwords
usernames = ["Max33", "Danna"]
names = ["Davis Azangu", "Donna Moguche"]

# Streamlit app
st.title("Welcome to Churn Predictor App")

# Sidebar for login
st.sidebar.title("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

authentication_status = None

if st.sidebar.button("Login"):
    if username in usernames:
        user_index = usernames.index(username)
        hashed_password = hashed_passwords[user_index]

        # Check if the provided password matches the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            authentication_status = True
            name = names[user_index]
            st.sidebar.success("Login successful!")
            st.write(f"Welcome {name}!")
        else:
            authentication_status = False
            st.sidebar.error("Invalid username or password")
    else:
        authentication_status = False
        st.sidebar.error("Invalid username or password")

# Logout button
if authentication_status:
    if st.sidebar.button("Logout"):
        st.sidebar.success("Logged out successfully!")
        authentication_status = None
        st.experimental_rerun()

# Display message if not logged in
if authentication_status is None:
    st.write("Please log in from the sidebar to access the content.")
    
    def home_page():
        image_filename = 'home.png'
        home_image_path = os.path.join('Assets', 'home.png')
        st.image(home_image_path, use_column_width=False)


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
    

