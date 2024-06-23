import streamlit as st
import pandas as pd
from authentication import authenticated_page

st.set_page_config(
    page_title= 'Data Page',
      page_icon = "🗃",
      layout= 'wide'
)



if authenticated_page():
    
    st.title('Churn Database \U0001F4C8')
 
    def show_dataframe(data):
        df = st.dataframe(data)
        return df

    data = pd.read_csv('./Data/data1.csv')

    column_type = st.selectbox('Select column type', ['All columns', 'Numerical columns', 'Categorical columns'])

    if column_type == 'All columns':
        show_dataframe(data)
    elif column_type == 'Numerical columns':
        numerical_columns = data.select_dtypes(include=['float', 'int']).columns
        show_dataframe(data[numerical_columns])
    elif column_type == 'Categorical columns':
        categorical_columns = data.select_dtypes(include=['object']).columns
    show_dataframe(data[categorical_columns])
    
    
    
    


    