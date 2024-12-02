import streamlit as st
from db_handler import init_db, update_state, get_state, add_response, get_responses, reset_game, has_submitted
import matplotlib.pyplot as plt

# Initialize the database
init_db()

# Selection screen
st.title("Game App")
role = st.radio("Select your role:", ["Player", "Game Master"])

# Shared database connection setup
current_round = get_state("current_round")
round_active = get_state("round_active")

gm_pw = "password"

if role == "Game Master":
    st.header("Game Master Dashboard")

    # Game master password
    password = st.text_input("Enter password:", type="password")
    if password == gm_pw:
        

        # Update (refresh) the page
        if st.button("Update"):
            st.session_state["refresh"] = not st.session_state.get("refresh", False)

        # Start a new round
        if st.button("Start New Round"):
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
        if current_round:
            responses = get_responses(int(current_round))
            if responses:
                st.table(responses)

                # Extract answers for histogram
                answers = [int(response[1]) for response in responses]
                names = [response[0] for response in responses]
                
                # Create histogram
                fig, ax = plt.subplots()
                ax.bar(names, answers)
                ax.set_xlabel('Names')
                ax.set_ylabel('Answers')
                ax.set_title(f'Responses for Round {current_round}')

                # Display histogram in Streamlit
                st.pyplot(fig)
            else:
                st.write("No responses yet for this round.")
        else:
            st.write("No round is active.")

        # Reset Game
        if st.button("Reset Game"):
            reset_game()
            st.warning("Game has been reset!")


elif role == "Player":
    st.header("Player Interface")

    # Update (refresh) the page using a button
    if st.button("Update"):
        st.session_state["refresh"] = not st.session_state.get("refresh", False)

    # Get current round and state
    current_round = get_state("current_round")
    round_active = get_state("round_active")

    if round_active == "true":
        st.write(f"Round {current_round} is active! Submit your answer.")
        player_name = st.text_input("Enter your name:")
        # answer = st.text_input("Your Answer:")
        answer = st.select_slider(f"Leave concert {current_round} at time:", options=range(0, 11))

        # if st.button("Submit"):
        if st.button("Submit"):
            if player_name and answer:
                # Check if the player has already submitted
                if has_submitted(player_name, int(current_round)):
                    st.error("You have already submitted a response for this round!")
                else:
                    add_response(player_name, int(current_round), answer)
                    st.success("Answer submitted!")
            else:
                st.error("Please enter both name and answer.")
    else:
        st.warning("No active round. Wait for the game master to start the next round.")

