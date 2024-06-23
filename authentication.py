# authentication.py

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def setup_authentication():
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
    st.session_state['authentication_status'] = authentication_status
    return name

def authenticated_page():
    name = setup_authentication()
    if st.session_state['authentication_status']:
        st.write(f"Welcome {name}!")
        return True
    elif st.session_state['authentication_status'] is False:
        st.error('Wrong username/password')
        return False
    elif st.session_state['authentication_status'] is None:
        st.info('Login to get access to the app')
        st.code("""
        Test Account
        username: DataWhizz04
        password: max123
        """)
        return False