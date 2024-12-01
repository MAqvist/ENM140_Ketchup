import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# Initialize session state to store responses
if "responses" not in st.session_state:
    st.session_state["responses"] = []

# Title and instructions
st.title("Game Input and Real-Time Visualization")
st.write("Welcome to the game! Answer the question within the given time.")

# Define a question and timer duration
question = "How much utility do you gain from this activity? (0-10)"
timer_duration = 10  # seconds

# Timer logic
if "start_time" not in st.session_state:
    st.session_state["start_time"] = time.time()

elapsed_time = time.time() - st.session_state["start_time"]
remaining_time = max(timer_duration - elapsed_time, 0)

# Display question and time remaining
st.write(f"Question: {question}")
st.write(f"Time remaining: {int(remaining_time)} seconds")

# Input form
if remaining_time > 0:
    answer = st.number_input("Your Answer:", min_value=0, max_value=10, step=1, key="current_input")
    if st.button("Submit"):
        st.session_state["responses"].append(answer)
        st.success("Answer submitted!")
else:
    st.warning("Time is up! Waiting for the next round.")

# Reset timer for the next round (optional for gameplay)
if remaining_time == 0 and st.button("Next Round"):
    st.session_state["start_time"] = time.time()

# Display current responses
if st.session_state["responses"]:
    st.write("Responses so far:", st.session_state["responses"])

    # Perform computations
    df = pd.DataFrame(st.session_state["responses"], columns=["Answers"])
    average_score = df["Answers"].mean()
    st.write(f"Average Utility: {average_score:.2f}")

    # Visualize responses
    st.bar_chart(df["Answers"].value_counts(sort=False))

# Footer for updates
st.write("This app updates automatically as players submit answers.")
