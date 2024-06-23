import streamlit as st
from authentication import authenticated_page



# function to set up page configuration
st.set_page_config(
        page_title="History",
        page_icon="🕰️",
        layout="wide",
    )

if authenticated_page():
    st.title('Prediction History 📚')






