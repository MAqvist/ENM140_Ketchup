import streamlit as st
from db_handler import init_db, update_state, get_state, add_response, get_responses, reset_game, has_submitted, get_utility_nexts, add_utility_next, add_utility, get_utilities
import matplotlib.pyplot as plt
from game_engine import concert_utility2
import numpy as np
import pandas as pd
import utilities as ut
from graphs2 import SeminarGraph, plot_cumulative_utility

# lägga in lucaas figure
# ta bort tabellen med data
# lägg in tabell överst med rundans resultat
# ta bort rad för användare
# fixa slut cumulativa utility, gör det till en checkbox

# Initialize the database
init_db()

# Selection screen
st.title("Festival Game")
role = st.radio("Select your role:", ["Player", "Game Master"])

# Shared database connection setup
current_round = get_state("current_round")
round_active = get_state("round_active")

gm_pw = "pw"
n_time_steps = 10
max_concerts = 10

number_to_ordinal = [
    'first', 'second', 'third', 'fourth', 'fifth',
    'sixth', 'seventh', 'eighth', 'ninth', 'tenth',
    'eleventh', 'twelfth', 'thirteenth', 'fourteenth',
    'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth',
    'nineteenth', 'twentieth'
]

if role == "Game Master":
    # Auto-refresh every n seconds
    # st_autorefresh(interval=1000)  # Interval is in milliseconds
    
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

        show_concert = st.checkbox("Show Concert", value=True)
        # show_utility = st.checkbox("Show Utility", value=False)
        show_cumulative_utility = st.checkbox("Show Cumulative Utility", value=False)
        show_seminar_graph = st.checkbox("Show Seminar Graph", value=False)
        show_current_utility_table = st.checkbox("Show Current Utility Table", value=False)

        # View Responses
        if current_round:
            if int(current_round) <= max_concerts:
                label = f"The {number_to_ordinal[int(current_round)-1]} concert is active."
                s = f"<p style='font-size:40px;'>{label}</p>"
                st.markdown(s, unsafe_allow_html=True) 
                # st.write(f"The {number_to_ordinal[current_round]} concert is active.")
                responses = get_responses(int(current_round))
                if responses:
                    # Extract answers for histogram
                    answers = [int(response[1]) for response in responses]
                    names = [response[0] for response in responses]

                    # Calculate utility
                    previous_round = {}
                    for name in names:
                        utility_factor = ut.utility_for_next_concert(int(current_round)-1, name)
                        previous_round[name] = utility_factor
                    utility, utility_factor_next, _ = concert_utility2(names, answers, previous_round, n_time_steps)

                    # Save utility for next concert
                    for i, name in enumerate(names):
                        add_utility_next(name, current_round, utility_factor_next[i])
                        add_utility(name, current_round, utility[i])

                    # Plot cumulative utility for each player
                    # if show_utility:
                    #     fig = ut.plot_cumulative_utility(names, utility)
                    #     st.pyplot(fig)

                    # Sum up total utility so far for all players who have answered this round
                    utility_total = {}
                    for round in range(1, int(current_round) + 1):
                        for name in names:
                            if name not in utility_total:
                                utility_total[name] = []
                            utilities = get_utilities(round, name)
                            utiliity_factor_next = get_utility_nexts(round, name)
                            if utilities:
                                utility_total[name].extend(utilities)

                    if show_current_utility_table:
                        # Display individual utility for this round
                        st.write("Utility for this round:")
                        my_dict = {'name' : names, 'leave_time' : answers, 'utility' : np.sum(utility, axis=1),'utility_factor_current' : list(previous_round.values()), 'utility_factor_next' : utility_factor_next}
                        my_df = pd.DataFrame(my_dict).sort_values(by='utility', ascending=False)
                        st.table(my_df)

                    # Plot seminar graph
                    if show_seminar_graph:
                        graph = SeminarGraph(names, answers, n_time_steps, int(current_round))
                        fig = graph.create_plot_data()
                        st.pyplot(fig)

                    # Plot concert
                    if show_concert:
                        fig, _ = ut.concert_fig(names, answers)
                        st.pyplot(fig)

                    if show_cumulative_utility:
                        fig = plot_cumulative_utility(names, utility_total, current_round, n_time_steps)
                        st.pyplot(fig)
                        
                    if 2 < 1:
                        # Display total utility so far
                        st.write("Total Utility So Far:")
                        st.table(pd.DataFrame(utility_total.items(), columns=["Name", "Total Utility"]))

                else:
                    st.write("No responses yet for this round.")

            elif int(current_round) > max_concerts:
                st.write("Game Over!")
                st.write("Results:")

                responses = get_responses(int(current_round)-1)
                names = [response[0] for response in responses]

                all_utilities = {}
                for round in range(1, max_concerts+1):
                    for name in names:
                        utilities = get_utilities(round, name)
                        print(utilities)
                        if utilities:
                            if name not in all_utilities:
                                all_utilities[name] = []
                            all_utilities[name].extend(utilities)
                            print(all_utilities)

                fig = plot_cumulative_utility(names, all_utilities, current_round, n_time_steps)
                st.pyplot(fig)
                            
        else:
            st.write("No round is active.")


        # Reset Game
        if st.button("Reset Game"):
            reset_game()
            st.warning("Game has been reset!")


elif role == "Player":
    # Get current round and state
    current_round = get_state("current_round")
    round_active = get_state("round_active")

    st.header(f"How long are you staying at the concert?")

    # Update (refresh) the page using a button
    if st.button("Refresh"):
        st.session_state["refresh"] = not st.session_state.get("refresh", False)

    if current_round:
        if int(current_round) <= max_concerts:
            if round_active == "true":
                st.write(f"Concert {current_round} is active.")
                player_name = st.text_input("Enter your name:", help="Name should be unique, but same every concert.")
                # answer = st.text_input("Your Answer:")
                answer = st.select_slider(f"Leave the {number_to_ordinal[int(current_round)-1]} concert at time:", options=range(0, n_time_steps+1))

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
                
                # If the player has submitted a response for this round show their position at concert
                if has_submitted(player_name, int(current_round)):
                    responses = get_responses(int(current_round))
                    names = [response[0] for response in responses]
                    answers = [int(response[1]) for response in responses]

                    _, positions = ut.concert_fig(names, answers)
                    idx = names.index(player_name)
                    position = positions[idx]

                    n = len(names)
                    n_cols = np.floor(n ** 0.5).astype(int)
                    n_rows = n // n_cols
                    if n % n_cols != 0:
                        n_rows += 1
    
                    row = position // n_cols
                    # st.write(f"You will be stood in the {number_to_ordinal[row]} row at the next concert.")
                                       

        else:
            st.write("Game Over!")
    else:
                st.warning("No concert active. Wait for the game master to start the next concert.")
