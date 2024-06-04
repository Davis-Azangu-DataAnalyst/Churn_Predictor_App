import streamlit as st
import pyodbc


st.set_page_config(
    page_title= 'Data Page',
    page_icon=":chart_with_upwards_trend:",
    layout= 'wide'
)


st.title('Churn Database')

# Create a connection 
@st.cache_resource(show_spinner='connecting to database...')
def init_connection():
    return pyodbc.connect(
        "DRIVER = {SQL Server}; SERVER="
          + st.secrets['server']
          + ";DATABASE ="
          + st.secrets['database']
          + ";UID ="
          + st.secrets['username']
          + ";PWD ="
          + st.secrets['password']
    )

connection = init_connection()

# Query the connection from the database
@st.cache_data(show_spinner='running_query...')
def running_query(query):
    with connection.cursor() as c:
        c.execute(query)
        rows = c.fetchall()
        
    return rows

sql_query = " SELECT * FROM LP2_Telco_churn_first_3000 "

rows = running_query(sql_query)

st.write(rows)
