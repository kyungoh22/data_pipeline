import gspread
#from google.oauth2 import service_account
#from googleapiclient import discovery
import plotly.express as px
import streamlit as st
import pandas as pd


credentials_dict = st.secrets

def read_data():
    #gc = gspread.service_account(filename="service_account.json")
    gc = gspread.service_account_from_dict(credentials_dict)
    sh = gc.open("free-data-pipeline").get_worksheet(1) # index 0 = sheet1, index 1 = sheet2, etc.

    col_1 = sh.col_values(1)
    col_2 = sh.col_values(2)
    
    df = pd.DataFrame({'date': col_1, 'closing_price': col_2})
    
    # The data for dates before 24 Aug 2022 seems to be corrupt
    # So select only the dates after that.
    df['date'] = pd.to_datetime(df['date'])
    df = df [df['date'] > '2022-08-24']
    return df

def plot_data():
    df = read_data()
    df['closing_price'] = df['closing_price'].astype(float)

    fig = px.line(data_frame = df, 
                x = 'date' ,
                y = 'closing_price',
                title = 'Tesla stock closing price by date')
    st.plotly_chart(fig)


plot_data()