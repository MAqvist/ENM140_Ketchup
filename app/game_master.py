import streamlit as st
from db_handler import init_db, update_state, get_state, get_responses

# Initialize the database
init_db()

# Game Master Interface
st.title("Game Master Dashboard")

# Start a new round
if st.button("Start New Round"):
    current_round = get_state("current_round")
    new_round = int(current_round) + 1 if current_round else 1
    update_state("current_round", str(new_round))
    update_state("round_active", "true")
    st.success(f"Started Round {new_round}")

# End the current round
if st.button("End Current Round"):
    update_state("round_active", "false")
    st.warning("Round ended!")

# View Responses
st.write("Responses for Current Round:")
current_round = get_state("current_round")
if current_round:
    responses = get_responses(int(current_round))
    st.table(responses)
else:
    st.write("No round active.")
