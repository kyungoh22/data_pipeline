import gspread

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import streamlit as st

def read_data():
    gc = gspread.service_account(filename="service_account.json")
    sh = gc.open("free-data-pipeline").get_worksheet(0) # index 0 = sheet1, index 1 = sheet2, etc.

    row_1 = sh.row_values(1)
    row_2 = sh.row_values(2)
    print(row_1, row_2)
    df = pd.DataFrame({'date': row_1, 'closing_price': row_2})
    return df

def plot_data():
    df = read_data()
    df['closing_price'] = df['closing_price'].astype(float)

    fig = px.line(data_frame = df, 
                x = 'date' ,
                y = 'closing_price')
    st.plotly_chart(fig)
    
plot_data()