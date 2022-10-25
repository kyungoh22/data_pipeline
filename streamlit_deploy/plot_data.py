import gspread
#from google.oauth2 import service_account
#from googleapiclient import discovery
import plotly.express as px
import streamlit as st
import pandas as pd

print (st.secrets["gcp_service_account"])

# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# SAMPLE_SPREADSHEET_ID = '1YBDYsqbOqbs94K1inMrL6ppFcjH-qbtYPE_mCXxCXzA'      # Get this from the url // Refer to google API documentation
# SAMPLE_RANGE_NAME = 'A1:AA1000'


# def read_data():

#     credentials = service_account.Credentials.from_service_account_file( 
#             "service_account.json", scopes=SCOPES)                            
#     service = discovery.build('sheets', 'v4', credentials=credentials,cache_discovery=False)

#     result = service.spreadsheets().values().get(
#                 spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
#     result = result['values']
#     col_1 = result[0]
#     col_2 = result[1]
#     df = pd.DataFrame({'date': col_1, 'closing_price': col_2})
#     # The data for dates before 24 Aug 2022 seems to be corrupt
#     # So select only the dates after that.
#     df['date'] = pd.to_datetime(df['date'])
#     df = df [df['date'] > '2022-08-24']

#     return df

def read_data():
    gc = gspread.service_account(filename="service_account.json")
    
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