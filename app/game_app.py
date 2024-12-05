import streamlit as st
from db_handler import init_db, update_state, get_state, add_response, get_responses, reset_game, has_submitted, get_utility_nexts, add_utility_next, add_utility, get_utilities
import matplotlib.pyplot as plt
from game_engine import concert_utility2, string_to_color
import numpy as np
import pandas as pd

# Initialize the database
init_db()

# Selection screen
st.title("Game App")
role = st.radio("Select your role:", ["Player", "Game Master"])

# Shared database connection setup
current_round = get_state("current_round")
round_active = get_state("round_active")

gm_pw = "pw"
n_time_steps = 10
max_concerts = 2

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
        st.write(f"Concert number: {current_round}")
        if int(current_round) <= max_concerts:
            responses = get_responses(int(current_round))
            if responses:
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
                utility, utility_factor_next, _ = concert_utility2(names, answers, previous_round, n_time_steps)
                print(f"utility: {utility}")
                print(f"utility factor next: {utility_factor_next}")
                for i, name in enumerate(names):
                    add_utility_next(name, current_round, utility_factor_next[i])
                    add_utility(name, current_round, np.sum(utility[i]))

                # plot positons and stage
                n = len(names)
                n_cols = np.floor(n ** 0.5).astype(int)
                n_rows = n // n_cols
                if n % n_cols != 0:
                    n_rows += 1
                possible_positions = [(i, j) for i in range(n_rows) for j in range(n_cols)]
                
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot([0, n_cols-1], [n_rows, n_rows], 'k-', lw=4) # Stage line
                ax.text((n_cols-1)/2, n_rows + 0.5, 'Stage', ha='center', va='center', fontsize=30, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
                positions = sorted(range(len(answers)), key=lambda i: answers[i])
                for idx, (i, j) in enumerate(possible_positions):
                    if idx < n // n_cols * n_cols:
                        x = j
                        y = n_rows - 1 - i
                        ax.text(x, y+(n_rows*0.1), names[positions[idx]], ha='center', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
                        ax.scatter(x, y, s=500, c=string_to_color(names[positions[idx]]), edgecolor='black', linewidth=2)
                # Center last row
                if n % n_cols != 0:
                    last_row_start = (n_cols - (n % n_cols)) / 2
                    for idx in range(n - (n % n_cols), n):
                        x = last_row_start + (idx % n_cols)
                        y = 0
                        ax.text(x, y+(n_rows*0.1), names[positions[idx]], ha='center', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
                        ax.scatter(x, y, s=500, c=string_to_color(names[positions[idx]]), edgecolor='black', linewidth=2)

                # Add row numbers
                for i in range(n_rows):
                    ax.text(-0.5, n_rows - 1 - i, f"Row {i+1}", ha='right', va='center', fontsize=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

                ax.axis('off')
                ax.set_xlim(-1, n_cols)
                ax.set_ylim(-1, n_rows + 1)
                st.pyplot(fig)

                # Plot lines
                fig, ax = plt.subplots()
                for i, name in enumerate(names):
                    ax.plot(range(n_time_steps+1), np.cumsum(utility[i]), label=name, color=string_to_color(name))
                
                ax.set_xticks(range(n_time_steps+1))
                ax.set_xlabel("Time")
                ax.set_ylabel("Cumulative Utility")
                ax.legend()
                ax.grid()
                st.pyplot(fig)

                # Sum up total utility so far for all players who have answered this round
                total_utility_so_far = {}
                for round in range(1, int(current_round)+1):
                    utilities = get_utilities(round)
                    for utilitie in utilities:
                        name = utilitie[0]
                        value = utilitie[1]
                        if name in total_utility_so_far:
                            total_utility_so_far[name] += value
                        else:
                            total_utility_so_far[name] = value

                # Display total utility so far
                st.write("Total Utility So Far:")
                st.table(pd.DataFrame(total_utility_so_far.items(), columns=["Name", "Total Utility"]))

                # Display individual utility for this round
                st.write("Utility for this round:")
                my_dict = {'name' : names, 'leave_time' : answers, 'utility' : np.sum(utility, axis=1),'utility_factor_current' : list(previous_round.values()), 'utility_factor_next' : utility_factor_next}
                st.table(pd.DataFrame(my_dict))

            else:
                st.write("No responses yet for this round.")
        elif int(current_round) > max_concerts:
            st.write("Game Over!")
            st.write("Results:")
            all_utilities = {}
            for round in range(1, max_concerts+1):
                utilities = get_utilities(round)
                for utilitie in utilities:
                    name = utilitie[0]
                    value = utilitie[1]
                    if name in all_utilities:
                        all_utilities[name].append(value)
                    else:
                        all_utilities[name] = [value]

            # Plot cumulative utility for each player
            fig, ax = plt.subplots()
            for name, utility_list in all_utilities.items():
                cumulative_utility = np.cumsum(utility_list)
                ax.plot(range(1, len(cumulative_utility) + 1), cumulative_utility, label=name, color=string_to_color(name))

            ax.set_xticks(range(1, max_concerts + 1))
            ax.set_xlabel("Concert Number")
            ax.set_ylabel("Cumulative Utility")
            ax.legend()
            ax.grid()
            st.pyplot(fig)
                        
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

