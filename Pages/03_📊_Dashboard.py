import streamlit as st
import plotly.express as px
import pandas as pd




st.set_page_config(
    page_title= 'Customer_Churn_Dashboard',
    page_icon=":bar_chart:",
    layout= 'wide'
)


df = pd.read_csv('./Data/final_df.csv')
def eda_dashboard():
    st.markdown('### Exploratory Data Analysis')

    col1,col2 = st.columns(2)
    with col1:
         scatter_plot = px.scatter(df, x='tenure', y='monthlycharges', title='Tenure to monthly charges Distribution in the Churn',
                     color='churn', color_discrete_map={'Yes':'green', 'No':'darkblue'})
         st.plotly_chart(scatter_plot)
    with col2:
        churn_gender_counts = df.groupby(['gender', 'churn']).size().reset_index(name='count') #Groupby
        fig = px.bar(churn_gender_counts, x='gender', y='count', color='churn', barmode='group',
             color_discrete_map={'No': 'darkblue', 'Yes': 'green'}) # Barplot and its settings.

        fig.update_layout(
        xaxis_title='Gender',
        yaxis_title='Count',
        title='Distribution of Churn in Gender') # Barplot layout

        st.plotly_chart(fig) # Display the chart

    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        churn_rate = df.groupby('paymentmethod')['churn'].count().sort_values(ascending=False)
        # Create hori #zontal bar chart
        fig = px.bar(
        churn_rate,
        orientation='h',
        labels={'index': 'Payment Method', 'value': 'churn Count'},
        title='Payment Methods with the Highest Churn Rate')
        fig.update_traces(marker_color='darkblue')
    st.plotly_chart(fig)

    st.divider()
    
    with col4:
       def visualize_heatmap():
           
           st.divider()

def kpi_dashboard():
    st.markdown('### Key Performance Indicators')

    col1, col2 =st.columns(2)
    with col1:
       st.markdown('<div style="background-color: #CCE5FF; border-radius: 10px; padding: 20px;">', unsafe_allow_html=True)
       st.markdown('<h3>Quick Stats About Dataset</h3>', unsafe_allow_html=True)

       churn_rate = (df['churn'].value_counts(normalize=True).get('Yes', 0) * 100)
       st.markdown(f'<p>Churn Rate: <strong>{churn_rate:.2f}%</strong></p>', unsafe_allow_html=True)

       average_monthly_charges = df['monthlycharges'].mean()
       st.markdown(f'<p>Average Monthly Charges: <strong>${average_monthly_charges:.2f}</strong></p>', unsafe_allow_html=True)

       average_total_charges = df['totalcharges'].mean()
       st.markdown(f'<p>Average Total Charges: <strong>${average_total_charges:.2f}</strong></p>', unsafe_allow_html=True)

       total_churn = df['churn'].value_counts().get('Yes', 0)
       st.markdown(f'<p>Total Churn: <strong>{total_churn}</strong></p>', unsafe_allow_html=True)

       st.markdown('</div>', unsafe_allow_html=True)
    
    
    with col2:
        pass


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


