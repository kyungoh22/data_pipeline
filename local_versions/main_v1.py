import urllib3
import json
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from apiclient import discovery


# You can either define the hidden variable "API_KEY" in the terminal
# Or you can load them from the ".env" file. 
# If you want to load from the ".env" file, use "load_dotenv()"
load_dotenv()


# Get data from API
def get_data_lambda():
    
    print (os.environ.get("API_KEY"))
    http = urllib3.PoolManager()    # Create PoolManager object
    url = "https://cloud.iexapis.com/stable/stock/tsla/previous?token=" + os.environ.get("API_KEY") # Define URL, with token coming from environment variable
    resp = http.request("GET", url)     # Make GET request and save the response
    print(resp.status)                  # The response object has several attributes.
    values = json.loads(resp.data)      # One attribute is the actual data. Load as JSON and save to "valeus"
    print(values)
    return values



# Write data to google sheet

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1YBDYsqbOqbs94K1inMrL6ppFcjH-qbtYPE_mCXxCXzA'      # Get this from the url // Refer to google API documentation
SAMPLE_RANGE_NAME = 'A1:AA1000'

def Export_Data_To_Sheets():

    credentials = service_account.Credentials.from_service_account_file(    # These lines will always be the same.
        "service_account.json", scopes=SCOPES)                              # These lines will always be the same.
    service = discovery.build('sheets', 'v4', credentials=credentials)      # These lines will always be the same. 

    values = get_data_lambda()
    values_list = list(values.values())
    final_list = []
    final_list.append(values_list)
    dict_me = dict(values=final_list)

    service.spreadsheets().values().append(                                 # These lines will always be the same.
        spreadsheetId=SAMPLE_SPREADSHEET_ID ,
        valueInputOption='RAW',
        range=SAMPLE_RANGE_NAME,
        body=dict_me).execute()

    print('Sheet successfully Updated')


#Export_Data_To_Sheets()


# Reading data from a google sheet works almost exactly the same way as writing:


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1YBDYsqbOqbs94K1inMrL6ppFcjH-qbtYPE_mCXxCXzA'
SAMPLE_RANGE_NAME = 'A1:AA1000'

def Read_Data_From_Sheets():

    credentials = service_account.Credentials.from_service_account_file( 
            "service_account.json", scopes=SCOPES)                            
    service = discovery.build('sheets', 'v4', credentials=credentials)

    result = service.spreadsheets().values().get(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    return result

Read_Data_From_Sheets()

