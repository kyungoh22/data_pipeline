import gspread

def write_data_lambda(event, context):

    gc = gspread.service_account(filename="service_account.json")
    wks = gc.open("free-data-pipeline").get_worksheet(1)          
    
    date = event["responsePayload"]['date']
    closing_price = event["responsePayload"]['closing_price']

    
    wks.append_row([date, closing_price])
