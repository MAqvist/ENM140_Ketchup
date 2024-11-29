import streamlit as st
from firebase_admin import credentials, db, initialize_app
from firebase_admin import credentials, initialize_app, get_app
from firebase_admin.exceptions import FirebaseError
import pandas as pd
import time


import streamlit as st
from firebase_admin import credentials, initialize_app, get_app
from firebase_admin.exceptions import FirebaseError

# Firebase setup
if "firebase_initialized" not in st.session_state:
    try:
        # Try to get the default Firebase app
        app = get_app()
        st.session_state.firebase_initialized = True
        st.write("Firebase app already initialized.")
    except ValueError:
        # Initialize Firebase if it doesn't already exist
        cred = credentials.Certificate("app/festival-game-6f53a-firebase-adminsdk-x47fu-bdd2a42766.json")
        initialize_app(cred, {
            'databaseURL': 'https://festival-game-6f53a-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        st.session_state.firebase_initialized = True
        st.write("Firebase app initialized successfully.")

# Database references
game_ref = db.reference("game")
decision_ref = game_ref.child("decisions")
state_ref = game_ref.child("state")

# Initialize game state
if not state_ref.get():
    state_ref.set({
        "step": 1,
        "cooperate_count": 0,
        "defect_count": 0,
    })

# Get game state
game_state = state_ref.get()

# Title
st.title("Real-Time Multiplayer Game")

# Display game state
st.write(f"Timestep {game_state['step']}: Make your decision!")
st.write(f"Cooperate votes: {game_state['cooperate_count']}, Defect votes: {game_state['defect_count']}")

# User input
decision = st.radio("Choose your action:", ["Cooperate", "Defect"])
if st.button("Submit Decision"):
    decision_ref.push({"decision": decision})
    st.success("Your decision has been recorded!")

# Listen for updates
st.write("Waiting for other players...")
while True:
    decisions = decision_ref.get()
    if decisions:
        decisions_list = list(decisions.values())
        cooperate_count = sum(1 for d in decisions_list if d["decision"] == "Cooperate")
        defect_count = sum(1 for d in decisions_list if d["decision"] == "Defect")

        # Update state
        state_ref.update({
            "cooperate_count": cooperate_count,
            "defect_count": defect_count,
        })

        st.write(f"Updated State: Cooperate = {cooperate_count}, Defect = {defect_count}")
        time.sleep(5)
        break
