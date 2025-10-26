import streamlit as st
from datetime import date
from utils.google_sheets import append_workout, fetch_all_workouts

# --- Default Exercise List ---
DEFAULT_EXERCISES = [
    "Leg Curl", "Leg Extension", "Hip Abduction", "Hip Adduction", "Seated Leg Press",
    "Hip Thrust", "Squats", "Plank", "Rotator Cutoff", "Push up",
    "Close Grip Lat Pulldown", "Wide Grip Row", "Close Grip Row", "Wide Lat Pulldown",
    "Face Pull", "Rear Deltoid", "Bicep Curl", "Rotator Cuff",
    "Flat Machine Chest Press", "Inclined Chest Press", "Shoulder Press",
    "Lateral Rise", "Tricep Pushdown", "Tricep Extension",
]

def run():
    st.title("💪 Couple Gym Tracker - Log Workout")
    st.write("Log your workouts and view shared progress!")

    # --- Initialize session state ---
    if "exercises" not in st.session_state:
        st.session_state.exercises = sorted(set(DEFAULT_EXERCISES))

    with st.form("workout_form"):
        name = st.selectbox("Who worked out?", ["Akram", "Arshiya"])

        # --- Exercise fields side by side ---
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

        # Add new exercise if entered
        if new_exercise:
            if new_exercise not in st.session_state.exercises:
                st.session_state.exercises.append(new_exercise)
                st.success(f"✅ '{new_exercise}' added to list!")
                exercise = new_exercise
            else:
                st.info("Exercise already exists. You can select it from the list.")

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
            machine = st.selectbox("Machine", ["Easy", "Medium", "Hard"], index=2)  # Hard default
        with col8:
            comments = st.text_input("Comments (optional)")

        submitted = st.form_submit_button("Add Entry")

    # --- Handle submission ---
    if submitted and exercise:
        row = [
            str(date.today()),
            name,
            exercise,
            set_no,
            reps,
            weight,
            unit,
            machine,
            comments,
        ]
        append_workout(row)
        st.success(f"Workout added: {exercise} | Set {set_no} | {weight}{unit} | {machine}")

    # --- Show log ---
    df = fetch_all_workouts()
    if df.empty:
        st.info("No data yet. Add your first workout!")
    else:
        st.subheader("Workout Log")
        st.dataframe(df, use_container_width=True)
        # st.bar_chart(df.groupby("Name")["Set No"].count())

if __name__ == "__main__":
    run()
