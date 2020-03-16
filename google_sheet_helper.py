import gspread
from oauth2client.service_account import ServiceAccountCredentials

#TODO: convert to a class

def get_google_sheets_client():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_creds.json", scope)
    client = gspread.authorize(creds)
    return client

def get_sheet(client):
    return client.open("Products").sheet1


def add_asin_to_sheet(sheet, asin):
    sheet.append_row(asin)


