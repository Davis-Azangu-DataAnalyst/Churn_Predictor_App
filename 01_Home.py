import streamlit as st
from pathlib import Path
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from Utils.info import column_1, column_2



# set home page
st.set_page_config(
    page_title='Home Page',
    page_icon='🏠',
    layout='wide'
)

with open("./config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


name, authentication_status, username = authenticator.login(location='sidebar')

if st.session_state['authentication_status']:
    authenticator.logout(location='sidebar')
    st.title('Churn Predictor Web App :robot_face:')
    st.write(f"Welcome {name}!")

    col1, col2 = st.columns(2)
    with col1:
        column_1
    with col2:
        column_2
        
        

elif st.session_state['authentication_status'] is False:
    st.error('Wrong username/password')
elif st.session_state['authentication_status'] is None:
    st.info('Login to get access to the app')
    st.code("""
    Test Account
    username: DataWhizz04
    password: max123
    """)

#st.write(st.session_state)




