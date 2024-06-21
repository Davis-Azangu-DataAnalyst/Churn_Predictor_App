import streamlit as st
import plotly.express as px
import pandas as pd


# Configuring the page setup
st.set_page_config(
    page_title= 'Customer_Churn_Dashboard',
    page_icon=":bar_chart:",
    layout= 'wide'
)


# Load the cleaned final data
df = pd.read_csv('./Data/final_df.csv')

# Filters on sidebar
st.sidebar.subheader('Filters')

# For gender
gender = st.sidebar.multiselect("Pick your gender", df["gender"].unique())
if not gender:
    final = df.copy()
else:
    final = df[df["gender"].isin(gender)]


# For contract types
contract_type = st.sidebar.multiselect("Pick your contract type", df["contract"].unique())
if contract_type:
    final = final[final["contract"].isin(contract_type)]


# For payment method
payment_method = st.sidebar.multiselect("Pick your payment method", df["paymentmethod"].unique())
if payment_method:
    final= final[final["paymentmethod"].isin(payment_method)]


#Function for eda_dashboard
def eda_dashboard():
    st.markdown('## 🕵️ Exploratory Data Analysis:')
    
    st.markdown('##### a. Univariate Analysis')

  
  # Monthly charges histogram
    col1,col2,col3 = st.columns(3)
    with col1:
        monthlycharges_histogram = px.histogram(final,x="monthlycharges",title="Distribution of monthly charges")
        monthlycharges_histogram.update_traces(marker_color="darkblue")
        st.plotly_chart(monthlycharges_histogram)

    
   # Tenure distribution histogram
    with col2:
        tenure_histogram = px.histogram(final,x="tenure",title="Distribution of tenure")
        tenure_histogram.update_traces(marker_color="darkblue")
        st.plotly_chart(tenure_histogram)


    # Total charges histogram
    with col3:
        totalcharges_histogram = px.histogram(final,x="totalcharges",title="Distribution of total charges")
        totalcharges_histogram.update_traces(marker_color="darkblue")
        st.plotly_chart(totalcharges_histogram)

    st.divider()

    
    st.markdown('##### b. Bivariate Analysis')
    
    
    
    col4,col5 = st.columns(2)
    with col4:
        colors = ['green', 'darkblue']
        pieplot = px.pie(final,names="churn", title= "Churn Rate", color="churn",color_discrete_sequence=colors)
        st.plotly_chart(pieplot)
    with col5:
        churn_gender_counts = final.groupby(['gender', 'churn']).size().reset_index(name='count') #Groupby
        fig = px.bar(churn_gender_counts, x='gender', y='count', color='churn', barmode='group',
             color_discrete_map={'No': 'darkblue', 'Yes': 'green'}) # Barplot and its settings.

        fig.update_layout(
        xaxis_title='Gender',
        yaxis_title='Count',
        title='Distribution of Churn in Gender') # Barplot layout

        st.plotly_chart(fig) # Display the chart

        st.divider()


    st.markdown('##### c. Multivariate Analysis')
    

    # Scatterplot for tenure and monthly charges over churn
    fig = px.scatter(final, x='tenure', y='monthlycharges', title='Tenure to monthly charges Distribution in the Churn',
                     color='churn', color_discrete_map={'Yes':'green', 'No':'darkblue'})
    fig.update_layout(
        width=600,
        height=400,
        margin=dict(l=20, r=20, t=20, b=20)

    )
    
    st.plotly_chart(fig)

    st.divider()
    
    col6,col7 = st.columns(2)
    
    with col6:
      fig=px.histogram(final, x="contract", color="churn", title="Histogram for contract in churn", color_discrete_map={'Yes':'green', 'No':'darkblue'})
      st.plotly_chart(fig)
    
    with col7:
        fig=px.histogram(final, x="paymentmethod", color="churn", title="Histogram for contract in churn", color_discrete_map={'Yes':'green', 'No':'darkblue'})
        st.plotly_chart(fig)
     
    st.divider()

    
    # Monthly charges trend over tenure
    average_monthlycharges = final.groupby("tenure")["monthlycharges"].mean().reset_index()

    fig = px.line(average_monthlycharges, x="tenure", y="monthlycharges", title="Average Monthly Charges over Tenure")
    fig.update_layout(
        xaxis_title='Tenure',
        yaxis_title='Average Monthly Charges',
        width=800,
        height=600
    )

    st.plotly_chart(fig)


    # Avarage churn trend by tenure
    total_churn=final.groupby("tenure")["churn"].count().reset_index()

    fig = px.line(total_churn, x="tenure", y="churn", title="Total Churn over Tenure")

    fig.update_layout(
        xaxis_title='Tenure',
        yaxis_title='Total Churn',
        width=800,
        height=600)
    st.plotly_chart(fig)


    # Define KPI dashboard function
def kpi_dashboard():
    st.markdown('## 📊 Key Performance Indicators')

    # Display quick stats about the dataset
        
    st.markdown("""
        <style>
        .card {
            background-color: #d4edda; 
            border: 1px solid #c3e6cb; 
            border-radius: 10px; 
            padding: 20px; 
            margin: 10px; 
            flex: 1; 
            text-align: center;
        }
        .card-container {
            display: flex; 
            justify-content: space-around; 
            flex-wrap: wrap;
        }
        </style>
    """, unsafe_allow_html=True)

        
    st.markdown('<h3>Quick Stats About Dataset</h3>', unsafe_allow_html=True)

        # Churn rate calculation
    churn_rate = (final['churn'].value_counts(normalize=True).get('Yes', 0) * 100)
    st.markdown(f'''
        <div class="card-container">
            <div class="card">
                <p>Churn Rate: <strong>{churn_rate:.2f}%</strong> 📉</p>
            </div>
    ''', unsafe_allow_html=True)

        # Average monthly charges calculation
    average_monthly_charges = final['monthlycharges'].mean()
    st.markdown(f'''
            <div class="card">
                <p>Average Monthly Charges: <strong>${average_monthly_charges:.2f}</strong> 💵</p>
            </div>
    ''', unsafe_allow_html=True)

        # Average total charges calculation
    average_total_charges = final['totalcharges'].mean()
    st.markdown(f'''
            <div class="card">
                <p>Average Total Charges: <strong>${average_total_charges:.2f}</strong> 💰</p>
            </div>
    ''', unsafe_allow_html=True)

        # Total churn calculation
    total_churn = final['churn'].value_counts().get('Yes', 0)
    st.markdown(f'''
            <div class="card">
                <p>Total Churn: <strong>{total_churn}</strong> ⚠️</p>
            </div>
    ''', unsafe_allow_html=True)

        # Total customers calculation
    total_customers = len(final)
    st.markdown(f'''
            <div class="card">
                <p>Total Customers: <strong>{total_customers}</strong> 👥</p>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
                
    st.divider()
        
        
    st.markdown("### Additional Visualizations")

    
            # Churn by Contract
    col8, col9 = st.columns(2)
            
    with col8:
        churn_by_contract = final.groupby("contract")["churn"].value_counts().unstack().reset_index()

        fig = px.pie(churn_by_contract, values="Yes", names="contract", hole=0.5,
                        title="Churn Distribution by Contract Type")

        fig.update_traces(textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig)

    with col9:
        churn_by_paymentmethod = final.groupby("paymentmethod")["churn"].value_counts().unstack().reset_index()
        fig = px.pie(churn_by_paymentmethod, values="Yes", names="paymentmethod", hole=0.5,
                        title="Churn Distribution by Payment Method")
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
    
    st.divider()

    col10,col11= st.columns(2)
    with col10:
        churn_security_counts = final.groupby(['onlinesecurity', 'churn']).size().reset_index(name='count') #Groupby
        fig = px.bar(churn_security_counts, x='onlinesecurity', y='count', color='churn', barmode='group',
             color_discrete_map={'No': 'darkblue', 'Yes': 'green'}) # Barplot and its settings.

        fig.update_layout(
        xaxis_title='Online Security',
        yaxis_title='Count',
        title='Distribution of Churn with Online Security') # Barplot layout
 
        st.plotly_chart(fig)

    with col11:
        churn_backup_counts = final.groupby(['onlinebackup', 'churn']).size().reset_index(name='count') #Groupby
        fig = px.bar(churn_backup_counts, x='onlinebackup', y='count', color='churn', barmode='group',
             color_discrete_map={'No': 'darkblue', 'Yes': 'green'}) # Barplot and its settings.

        fig.update_layout(
        xaxis_title='Online Backup',
        yaxis_title='Count',
        title='Distribution of Churn with Online Backup') # Barplot layout
 
        st.plotly_chart(fig)

    st.divider()

    col1, col2=st.columns(2)
    with col1:
        churn_streamingtv_counts = final.groupby(['streamingtv', 'churn']).size().reset_index(name='count') #Groupby
        fig = px.bar(churn_streamingtv_counts, x='streamingtv', y='count', color='churn', barmode='group',
             color_discrete_map={'No': 'darkblue', 'Yes': 'green'}) # Barplot and its settings.

        fig.update_layout(
        xaxis_title='Streaming Tv',
        yaxis_title='Count',
        title='Distribution of Churn with Streaming TV') # Barplot layout
 
        st.plotly_chart(fig)

    with col2:
        churn_streamingmovies_counts = final.groupby(['streamingmovies', 'churn']).size().reset_index(name='count') #Groupby
        fig = px.bar(churn_streamingmovies_counts, x='streamingmovies', y='count', color='churn', barmode='group',
             color_discrete_map={'No': 'darkblue', 'Yes': 'green'}) # Barplot and its settings.

        fig.update_layout(
        xaxis_title='Streaming Movies',
        yaxis_title='Count',
        title='Distribution of Churn with Streaming Movies') # Barplot layout
 
        st.plotly_chart(fig)



if __name__ == "__main__":
    st.title('DashBoard')
    col1, col2 = st.columns(2)
    with col1:
            pass
    with col2:
            st.selectbox('Select Type of Dashboard', options= ['EDA', 'KPI'],
                        key='selected_dashboard_type')
            

    if st.session_state['selected_dashboard_type'] == 'EDA':
        eda_dashboard()
    else:
        kpi_dashboard()


