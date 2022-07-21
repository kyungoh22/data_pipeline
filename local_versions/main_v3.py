# When I got to the stage of using the AWS Lambda function, 
# was having trouble with installing the dependencies in the zip file. 
# This was probably due to the google api.
# So now I'm going to use gspread, as originally described on the LMS

# This script is the version with ****MULTIPLE DAYS OF DATA****.

import urllib3
import json
import os
from dotenv import load_dotenv

import gspread


import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import streamlit as st


load_dotenv()

def get_data():
    

    http = urllib3.PoolManager()
    #url = "https://cloud.iexapis.com/stable/stock/tsla/previous?token=" + os.environ.get("API_KEY") # Define URL, with token coming from environment variable
    url = "https://sandbox.iexapis.com/stable/stock/TSLA/chart/1m?token=Tpk_181f3c56f73441798055291edda9cc09"
    resp = http.request("GET", url)
    values = json.loads(resp.data)
    return values





def write_data():
    data = get_data()
    gc = gspread.service_account(filename="service_account.json")
    wks = gc.open("free-data-pipeline").sheet1
    dates = []
    closing_prices = []
    for elem in data:
        date = elem['date']
        closing = elem['close']
        dates.append(date)
        closing_prices.append(closing)

    
    wks.append_row(dates)
    wks.append_row(closing_prices)


#write_data()

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



#plot_data()