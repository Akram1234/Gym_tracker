import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st
from config.settings import SCOPE, CREDENTIALS_FILE, SHEET_NAME, WORKOUT_TAB
import os

def getCredentials():
    if os.path.exists(CREDENTIALS_FILE):
        return ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
    else:
        creds_dict = st.secrets["credentials"]
        return ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)

def get_worksheet():
    """Authorize and return the worksheet object."""
    creds = getCredentials()
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
