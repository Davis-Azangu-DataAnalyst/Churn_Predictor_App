import streamlit as st
import uuid
import os
import joblib
from sklearn.compose import ColumnTransformer
import pandas as pd
import datetime


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
    print(pipeline)
    return pipeline


@st.cache_resource(show_spinner= 'models loading...')
def load_KNN_pipeline():
    pipeline = joblib.load('./Models/KNN_pipeline.joblib')
    print(pipeline)
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

    
        columns = ['gender', 'partner', 'dependents', 'phoneservice',
                'multiplelines', 'internetservice', 'onlinesecurity', 'onlinebackup',
                'deviceprotection', 'techsupport', 'streamingtv', 'streamingmovies',
                 'contract', 'paperlessbilling', 'paymentmethod']
    
        data = [['gender', 'partner', 'dependents', 'phoneservice',
                'multiplelines', 'internetservice', 'onlinesecurity', 'onlinebackup',
                'deviceprotection', 'techsupport', 'streamingtv', 'streamingmovies',
                 'contract', 'paperlessbilling', 'paymentmethod']]
    
        # Create a dataframe
        df= pd.DataFrame(data, columns=columns)

        # This makes prediction for History
        df['Predictions Time'] = datetime.date.today()
        df['Model Used'] = st.session_state['selected_model']

        df.to.csv('./Data/history.csv' ,mode='a',header=not os.path.exists('./Data/history.csv'), index=False)

        # Make prediction
        pred = pipeline.predict(df)
        pred = int(pred[0])
        prediction = encoder.inverse_transform([pred])

        # Get probabilities
        probability = pipeline.predict_proba[df]

        # Updating state
        st.session_state['prediction'] = prediction[0]
        st.session_state['probability'] = probability[0]

        return prediction, probability


                

def display_form():
    pipeline, encoder = select_model()
    col1, col2, col3 = st.columns(3)
    
    with col1:
            st.write('### Personal Information')
            gender = st.selectbox('Gender', ['Male', 'Female'], key= 'gender')
            partner = st.selectbox('Partner', ['Yes', 'No'], key= 'partner')
            dependents = st.selectbox('Dependents', ['Yes', 'No'], key= 'dependents')

    with col2:
            st.write('### Service Information')
            phoneservice = st.selectbox('Phone Service', ['Yes', 'No'], key= 'phoneservice')
            multiplelines = st.selectbox('Multiple Lines', ['Yes', 'No'], key='multiplelines')
            internetservice = st.selectbox('Internet Service', ['DSL', 'Fiber Optic', 'No'], key= 'internetservice')
            onlinesecurity = st.selectbox('Online Security', ['Yes', 'No'], key= 'onlinesecurity')
            onlinebackup = st.selectbox('Online Backup', ['Yes', 'No'], key= 'onlinebackup')
            deviceprotection = st.selectbox('Device Protection', ['Yes', 'No'], key= 'deviceprotection')
            techsupport = st.selectbox('Tech Support', ['Yes', 'No'], key= 'techsupport')

    with col3:
            st.write('### Billing Information')
            contract = st.selectbox('Contract', ['Month-to-Month', 'One Year', 'Two Year'], key= 'contract')
            paperlessbilling = st.selectbox('Paperless Billing', ['Yes', 'No'], key= 'paperlessbilling')
            paymentmethod = st.selectbox('Payment Method', ['Electronic Check', 'Mailed Check', 'Bank Transfer', 'Credit Card'], key= 'paymentmethod')
            seniorcitizen = st.selectbox('Senior Citizen', ['Yes', 'No'], key='seniorcitizen')
            tenure = st.number_input('Tenure', min_value=0, max_value=72, value=12)
            monthlycharges = st.number_input('Monthly Charges', min_value=0, max_value=1000, value=60)

    
            form = st.form(key='my_form')
            submit_button = form.form_submit_button(label='Make prediction')
    
    if submit_button:
          make_predictions(pipeline, encoder)
    
    
    #with st.form:
          #st.form_submit_button('Make prediction', on_click= make_predictions, kwargs=dict(pipeline=pipeline, encoder=encoder))


if __name__ == "__main__":
    st.title("Make a Prediction")
    display_form()
    
    prediction = st.session_state['predictions']
    probability = st.session_state['probability']

    

    if not prediction:
               st.markdown("### Prediction will show here")
    elif prediction == "Yes":
        probability_of_yes = probability[0][1] * 100
        st.markdown(f"### The customer will leave the company services with a probability of {round(probability_of_yes,2)}%")
    else:
        probability_of_no = probability[0][0]*100
        st.markdown(f"### The customer not will leave the company services with a probability of {round(probability_of_no,2)}%")
        st.write(st.session_state)




        



                 



    


        





