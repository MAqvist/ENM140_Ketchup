import streamlit as st
from db_handler import init_db, update_state, get_state, add_response, get_responses, reset_game, has_submitted, get_utility_nexts, add_utility_next
import matplotlib.pyplot as plt
from game_engine import concert_utility
import numpy as np

# Initialize the database
init_db()

# Selection screen
st.title("Game App")
role = st.radio("Select your role:", ["Player", "Game Master"])

# Shared database connection setup
current_round = get_state("current_round")
round_active = get_state("round_active")

gm_pw = "password"
n_time_steps = 10

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
            st.session_state["refresh"] = not st.session_state.get("refresh", False)

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

                # Calculate utility
                previous_round = {}
                for name in names:
                    next_round_utility = get_utility_nexts(str(int(current_round)-1), name)
                    print(f"next utility: {next_round_utility}")
                    if not next_round_utility:
                        previous_round[name] = 0.0
                    else:
                        previous_round[name] = float(next_round_utility[0][0])
                
                print(f"previous round: {previous_round}")
                utility, utility_factor_next = concert_utility(names, answers, previous_round, n_time_steps)
                
                for i, name in enumerate(names):
                    add_utility_next(name, current_round, utility_factor_next[i])

                # Plot lines
                fig, ax = plt.subplots()
                for i, name in enumerate(names):
                    ax.plot(range(n_time_steps), np.cumsum(utility[i]), label=name)
                
                ax.set_xlabel("Time")
                ax.set_ylabel("Cumulative Utility")
                ax.legend()
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
        answer = st.select_slider(f"Leave concert {current_round} at time:", options=range(0, n_time_steps+1))

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

