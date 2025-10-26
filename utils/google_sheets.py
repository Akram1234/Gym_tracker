import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from config.settings import SCOPE, CREDENTIALS_FILE, SHEET_NAME, WORKOUT_TAB

def get_worksheet():
    """Authorize and return the worksheet object."""
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).worksheet(WORKOUT_TAB)
    return sheet

def append_workout(row):
    """Add a new row to the workout sheet."""
    sheet = get_worksheet()
    sheet.append_row(row)

def fetch_all_workouts():
    """Fetch all workout records as a DataFrame."""
    sheet = get_worksheet()
    data = sheet.get_all_records()
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)
