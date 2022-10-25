import urllib3
import json
import os
from dotenv import load_dotenv


def get_data_lambda(event, context):
    
    load_dotenv()
    http = urllib3.PoolManager()
    url = "https://cloud.iexapis.com/stable/stock/tsla/previous?token=" + os.environ.get("API_KEY") # Define URL, with token coming from environment variable
    #url = "https://sandbox.iexapis.com/stable/stock/TSLA/chart/1m?token=Tpk_181f3c56f73441798055291edda9cc09"
    resp = http.request("GET", url)
    values = json.loads(resp.data)
    return values
