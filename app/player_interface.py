import streamlit as st
from db_handler import init_db, get_state, add_response

# Initialize the database
init_db()

# Player Interface
st.title("Player Interface")

# Get current round and state
current_round = get_state("current_round")
round_active = get_state("round_active")

if round_active == "true":
    st.write(f"Round {current_round} is active! Submit your answer.")
    player_name = st.text_input("Enter your name:")
    answer = st.text_input("Your Answer:")

    if st.button("Submit"):
        if player_name and answer:
            add_response(player_name, int(current_round), answer)
            st.success("Answer submitted!")
        else:
            st.error("Please enter both name and answer.")
else:
    st.warning("No active round. Wait for the game master to start the next round.")
