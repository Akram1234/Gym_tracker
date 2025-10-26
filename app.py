import streamlit as st
import pandas as pd
from utils.supabase_db import add_workout, fetch_workouts

# --- Constants ---
DEFAULT_EXERCISES = [
    "Leg Curl", "Leg Extension", "Hip Abduction", "Hip Adduction", "Seated Leg Press",
    "Hip Thrust", "Squats", "Plank", "Rotator Cutoff", "Push up",
    "Close Grip Lat Pulldown", "Wide Grip Row", "Close Grip Row", "Wide Lat Pulldown",
    "Face Pull", "Rear Deltoid", "Bicep Curl", "Rotator Cuff",
    "Flat Machine Chest Press", "Inclined Chest Press", "Shoulder Press",
    "Lateral Rise", "Tricep Pushdown", "Tricep Extension",
]
LIMIT = 30


# --- Utility Functions ---
def init_session_state():
    """Initialize exercises and names in session state."""
    if "exercises" not in st.session_state:
        st.session_state.exercises = sorted(set(DEFAULT_EXERCISES))
    if "names" not in st.session_state:
        st.session_state.names = ["Akram", "Arshiya"]



def render_exercise_selector():
    """Render exercise dropdown + add new field."""
    col1, col2 = st.columns([2, 1])
    with col1:
        exercise = st.selectbox(
            "Select exercise",
            st.session_state.exercises,
            index=None,
            placeholder="Choose from list..."
        )
    with col2:
        new_exercise = st.text_input("Add new")

    if new_exercise:
        if new_exercise not in st.session_state.exercises:
            st.session_state.exercises.append(new_exercise)
            st.success(f"✅ '{new_exercise}' added to list!")
            exercise = new_exercise
        else:
            st.info("Exercise already exists. You can select it from the list.")

    return exercise

def render_name_selector():
    """Render name dropdown + add new field."""
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.selectbox(
            "Who worked out?",
            st.session_state.names,
            index=None,
            placeholder="Select name..."
        )
    with col2:
        new_name = st.text_input("Add new name")

    if new_name:
        if new_name not in st.session_state.names:
            st.session_state.names.append(new_name)
            st.success(f"✅ '{new_name}' added to list!")
            name = new_name
        else:
            st.info("Name already exists. You can select it from the list.")

    return name

def render_workout_form():
    """Display the workout form."""
    st.subheader("📝 Log Workout")

    with st.form("workout_form"):
        name = render_name_selector()
        exercise = render_exercise_selector()

        # --- Set / Reps / Weight / Unit ---
        col3, col4, col5, col6 = st.columns(4)
        with col3:
            set_no = st.number_input("Set No", min_value=1, value=1)
        with col4:
            reps = st.number_input("Reps", min_value=1, value=10)
        with col5:
            weight = st.number_input("Weight", min_value=0.0, value=0.0)
        with col6:
            unit = st.selectbox("Unit", ["Kg", "Lb"], index=1)  # Lb default

        # --- Machine Difficulty + Comments ---
        col7, col8 = st.columns([1, 2])
        with col7:
            machine = st.selectbox("Machine", ["Easy", "Medium", "Hard"], index=2)
        with col8:
            comments = st.text_input("Comments (optional)")

        submitted = st.form_submit_button("Add Entry")

    if submitted and exercise:
        row = {
            "name": name,
            "exercise": exercise,
            "set_no": set_no,
            "reps": reps,
            "weight": weight,
            "unit": unit,
            "machine": machine,
            "comments": comments,
        }
        add_workout(row)
        st.success(f"Workout added: {exercise} | Set {set_no} | {weight}{unit} | {machine}")


def display_workout_log(limit=30):
    """Fetch, format, and display workout logs."""
    st.subheader("📊 Workout Log")
    df = fetch_workouts(limit)

    if df.empty:
        st.info("No data yet. Add your first workout!")
        return

    # Clean up columns
    if "id" in df.columns:
        df = df.drop(columns=["id"])
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"]).dt.date
        df = df.rename(columns={"created_at": "Date"})

    df.columns = [col.capitalize() for col in df.columns]

    # Display
    st.dataframe(df, use_container_width=True)


# --- Main Page Logic ---
def run():
    st.set_page_config(page_title="Couple Gym Tracker", page_icon="💪", layout="centered")
    st.sidebar.title("💑 Couple Gym Tracker")
    st.sidebar.markdown("Navigate between pages using the sidebar →")

    st.title("Welcome 💪")
    st.write("This is your **Couple Gym Tracker** — log workouts and track progress together!")

    init_session_state()
    render_workout_form()
    display_workout_log(LIMIT)


if __name__ == "__main__":
    run()
