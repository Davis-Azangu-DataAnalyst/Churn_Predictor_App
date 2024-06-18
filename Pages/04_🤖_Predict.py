import streamlit as st
import uuid
import os
import joblib
from sklearn.compose import ColumnTransformer
import pandas as pd
import datetime
import emoji



# function to set up page configuration
st.set_page_config(
        page_title="Churn Prediction",
        page_icon="🤖",
        layout="wide",
    )


st.title(" **Churn Prediction**")


@st.cache_resource(show_spinner= 'Models loading...')
def load_Logistic_Regression_pipeline():
    pipeline = joblib.load('./Models/Logistic_Regression_pipeline.joblib')
    return pipeline


@st.cache_resource(show_spinner= 'models loading...')
def load_KNN_pipeline():
    pipeline = joblib.load('./Models/KNN_pipeline.joblib')
    return pipeline


def select_model():
    col1, col2 = st.columns(2)
    
    with col1:
            st.selectbox('Select a model', options=[
            'Logistic_Regression', 'KNN'], key='selected_model')
    with col2:
        pass

    
    if st.session_state['selected_model'] == 'Logistic_Regression':
        pipeline = load_Logistic_Regression_pipeline()
    else:
        pipeline = load_KNN_pipeline()

    encoder = joblib.load('Models/encoder.joblib')

    return pipeline, encoder


if 'prediction' not in st.session_state:
            st.session_state['prediction'] = None
if 'probability' not in st.session_state:
            st.session_state['probability'] = None
            
st.cache_resource(show_spinner= 'models loading...')
def make_predictions(pipeline, encoder):
        gender = st.session_state['gender']
        partner = st.session_state['partner']
        dependents = st.session_state['dependents']
        phoneservice = st.session_state['phoneservice']
        multiplelines = st.session_state['multiplelines']
        internetservice = st.session_state['internetservice']
        onlinesecurity = st.session_state['onlinesecurity']
        onlinebackup = st.session_state['onlinebackup']
        deviceprotection = st.session_state['deviceprotection']
        techsupport = st.session_state['techsupport']
        streamingtv = st.session_state['streamingtv']
        streamingmovies = st.session_state['streamingmovies']
        contract = st.session_state['contract']
        paperlessbilling = st.session_state['paperlessbilling']
        paymentmethod = st.session_state['paymentmethod']
        seniorcitizen = st.session_state['seniorcitizen']
        tenure = st.session_state['tenure']
        monthlycharges = st.session_state['monthlycharges']
        totalcharges = st.session_state['totalcharges']


        # Convert tenure to integer
        tenure = int(tenure)

    # Create columns for the dataframe
        columns = ['gender', 'partner', 'dependents', 'phoneservice',
                'multiplelines', 'internetservice', 'onlinesecurity', 'onlinebackup',
                'deviceprotection', 'techsupport', 'streamingtv', 'streamingmovies',
                 'contract', 'paperlessbilling', 'paymentmethod', 'seniorcitizen', 
                 'tenure','monthlycharges','totalcharges', 'customerid']
    

    # Create rows for the dataframe
        data = [['gender', 'partner', 'dependents', 'phoneservice',
                'multiplelines', 'internetservice', 'onlinesecurity', 'onlinebackup',
                'deviceprotection', 'techsupport', 'streamingtv', 'streamingmovies',
                 'contract', 'paperlessbilling', 'paymentmethod', 'seniorcitizen',
                   'tenure', 'monthlycharges', 'totalcharges','customerid']]
    
        # Create a dataframe
        df= pd.DataFrame(data, columns=columns)
        

        # Change the data types to numerical 
        df['tenure'] = pd.to_numeric(df['tenure'], errors='coerce')
        df['monthlycharges'] = pd.to_numeric(df['monthlycharges'], errors='coerce')
        df['totalcharges'] = pd.to_numeric(df['totalcharges'], errors='coerce')

        # This makes prediction for History
        df['Predictions Time'] = datetime.date.today()
        df['Model Used'] = st.session_state['selected_model']

        df.to_csv('./Data/history.csv' ,mode='a',header=not os.path.exists('./Data/history.csv'), index=False)

        # Make a prediction and probability
        pred = pipeline.predict(df)
        pred_int = int(pred[0])
        prediction = encoder.inverse_transform([pred_int])


                # Get probabilities
        probability = pipeline.predict_proba(df)

                # Updating/Save in session state
        st.session_state['prediction'] = prediction
        st.session_state['probability'] = probability

        return prediction, probability

        
def display_form():
    pipeline, encoder = select_model()
    col1, col2, col3 = st.columns(3)
    
    with col1:
            st.write('###', emoji.emojize(':woman: Personal Information'))
            st.selectbox(' What is your gender?', ['Male', 'Female'], key= 'gender')
            st.selectbox('Do you have a partner?', ['Yes', 'No'], key= 'partner')
            st.selectbox('Do you have people that dependent on you?', ['Yes', 'No'], key= 'dependents')
            st.selectbox('Are you a senior citizen?', ['Yes', 'No'], key='seniorcitizen')
    with col2:
            st.write('###', emoji.emojize(':telephone_receiver: Service Information'))
            st.selectbox('Do you have access to phone services?', ['Yes', 'No'], key= 'phoneservice')
            st.selectbox('Do you have multiple lines?', ['Yes', 'No'], key='multiplelines')
            st.selectbox('What type of internet connection do you use?', ['DSL', 'Fiber Optic', 'No'], key= 'internetservice')
            st.selectbox('Do you have online security?', ['Yes', 'No'], key= 'onlinesecurity')
            st.selectbox('Do you have online backup storage?', ['Yes', 'No'], key= 'onlinebackup')
            st.selectbox('Are your devices protected?', ['Yes', 'No'], key= 'deviceprotection')
            st.selectbox('Do you have access to Tech Support', ['Yes', 'No'], key= 'techsupport')
            st.selectbox('Are you able to stream your TV channels smoothly?', ['Yes', 'No'], key='streamingtv')
            st.selectbox('Are you able to stream your movies perfectly?', ['Yes', 'No'], key='streamingmovies')

    with col3:
            st.write('###',emoji.emojize(':moneybag: Billing Information'))
            st.selectbox('What type of contract have you subscribed?', ['Month-to-Month', 'One Year', 'Two Year'], key= 'contract')
            st.selectbox('Do you use paperless billing?', ['Yes', 'No'], key= 'paperlessbilling')
            st.selectbox('What other types of payment do you use?', ['Electronic Check', 'Mailed Check', 'Bank Transfer', 'Credit Card'], key= 'paymentmethod')
            
            
            if 'tenure' not in st.session_state:
                  st.session_state.tenure = 12

            st.number_input('How long have you been our customer?', min_value=0, max_value=72, value=st.session_state.tenure)
            
            if'monthlycharges' not in st.session_state:
                  st.session_state.monthlycharges = 100
            st.number_input('How much is your monthly charges?', min_value=0, max_value=1000, value=st.session_state.monthlycharges)
            
            if 'totalcharges' not in st.session_state:
                  st.session_state.totalcharges = 1000
            st.number_input('How much is your total annual charges?', min_value=0, max_value=10000, value=st.session_state.totalcharges)
           
            

    # Prediction button
    with st.form(key='prediction_form'):
      st.form_submit_button('Make prediction', on_click=make_predictions, kwargs=dict(pipeline=pipeline, encoder=encoder))
    
if __name__ == "__main__":
         st.title("Make a Prediction")
         display_form()
    
         prediction = st.session_state['prediction']
         probability = st.session_state['probability']

         if not prediction:
               st.markdown("### Prediction shows here!")
               st.divider()
         elif prediction == "Yes":
               probability_of_yes = probability[0][1] * 100
               st.markdown(f"### The customer will leave the company services with a probability of {round(probability_of_yes,2)}%")
         else:
               probability_of_no = probability[0][0]*100
               st.markdown(f"### The customer not will leave the company services with a probability of {round(probability_of_no,2)}%")
st.write(st.session_state)




        



                 



    


        





