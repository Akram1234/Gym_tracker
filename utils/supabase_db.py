from supabase import create_client, Client
import streamlit as st
import pandas as pd
from datetime import date

def get_client() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def fetch_workouts(limit=30):
    client = get_client()
    response = client.table("workouts").select("*").order("id", desc=True).limit(limit).execute()
    return pd.DataFrame(response.data)

def add_workout(row):
    client = get_client()
    def safe_int(value):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return None
    data = {
        "name": row["name"],
        "exercise": row["exercise"],
        "set_no": safe_int(row["set_no"]),
        "reps": safe_int(row["reps"]),
        "weight": float(row["weight"]) if row["weight"] is not None else None,
        "unit": row["unit"],
        "machine": row["machine"],
        "comments": row["comments"]
    }

    client.table("workouts").insert(data).execute()

