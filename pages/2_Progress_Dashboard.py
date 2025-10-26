import streamlit as st
from utils.google_sheets import fetch_all_workouts

def run():
    st.title("📈 Progress Dashboard")
    df = fetch_all_workouts()
    if df.empty:
        st.info("No workout data yet.")
        return

    st.line_chart(df.groupby("Date")["Sets"].sum(), use_container_width=True)
    st.bar_chart(df.groupby("Name")["Weight (kg)"].mean(), use_container_width=True)

if __name__ == "__main__":
    run()
