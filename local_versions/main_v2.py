import urllib3
import json
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from apiclient import discovery

import plotly.express as px
import plotly.graph_objects as go


import pandas as pd
import streamlit as st


load_dotenv()

def get_data_lambda():
    
    print (os.environ.get("API_KEY"))
    http = urllib3.PoolManager()    # Create PoolManager object
    #url = "https://cloud.iexapis.com/stable/stock/tsla/previous?token=" + os.environ.get("API_KEY") # Define URL, with token coming from environment variable
    url = "https://sandbox.iexapis.com/stable/stock/TSLA/chart/1m?token=Tpk_181f3c56f73441798055291edda9cc09"
    resp = http.request("GET", url)     # Make GET request and save the response
    #print(resp.status)                  # The response object has several attributes.
    values = json.loads(resp.data)      # One attribute is the actual data. Load as JSON and save to "valeus"
    #print(values)
    return values

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1YBDYsqbOqbs94K1inMrL6ppFcjH-qbtYPE_mCXxCXzA'      # Get this from the url // Refer to google API documentation
SAMPLE_RANGE_NAME = 'A1:AA1000'


def Export_Data_To_Sheets():

    credentials = service_account.Credentials.from_service_account_file(    # These lines will always be the same.
        "service_account.json", scopes=SCOPES)                              # These lines will always be the same.
    service = discovery.build('sheets', 'v4', credentials=credentials)      # These lines will always be the same. 

    values = get_data_lambda()
    all_dates = []
    all_close = []
    for val in values: 
        date = val['date']
        close = val['close']
        all_dates.append(date)
        all_close.append(close)
    
    final_data = {'values':[all_dates,all_close]}               # When exporting, need to pass in a dictionary, where the key is "values"
                                                                # The value of the key "values" is a list of lists
                                                                # Each nested list then occupies a row

    service.spreadsheets().values().append(                                 # These lines will always be the same.
        spreadsheetId=SAMPLE_SPREADSHEET_ID ,
        valueInputOption='RAW',
        range=SAMPLE_RANGE_NAME,
        body=final_data).execute()


    print('Sheet successfully Updated')

#Export_Data_To_Sheets()

def Read_Data_From_Sheets():

    credentials = service_account.Credentials.from_service_account_file( 
            "service_account.json", scopes=SCOPES)                            
    service = discovery.build('sheets', 'v4', credentials=credentials,cache_discovery=False)

    result = service.spreadsheets().values().get(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()

    return result

result = Read_Data_From_Sheets()['values']
dates = result[0]
closing_prices = result[1]
df = pd.DataFrame({'date': dates, 'closing_price':closing_prices})
df['closing_price'] = df['closing_price'].astype(float)


# fig, ax = plt.subplots()
# ax.plot(df['date'], df['closing_price'])
# ax.set_xticks(ticks = list(range(len(df['date']))))
# # ax.set_xticklabels(labels = df['date'], rotation = 90)
# plt.show()
# st.pyplot(fig)

fig = px.line(data_frame = df, 
             x = 'date' ,
              y = 'closing_price')


st.plotly_chart(fig)
