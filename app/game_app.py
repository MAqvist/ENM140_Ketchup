import streamlit as st
from firebase_admin import credentials, db, initialize_app
import pandas as pd
import time

# Firebase setup
if "firebase_initialized" not in st.session_state:
    cred = credentials.Certificate("app/festival-game-6f53a-firebase-adminsdk-x47fu-bdd2a42766.json")  # Download from Firebase
    initialize_app(cred, {'databaseURL': 'https://festival-game-6f53a-default-rtdb.europe-west1.firebasedatabase.app/'})
    st.session_state.firebase_initialized = True

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
