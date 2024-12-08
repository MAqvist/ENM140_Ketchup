import sqlite3
import numpy as np

# Initialize the database
def init_db():
    conn = sqlite3.connect("game_state.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_state (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            player TEXT,
            round INTEGER,
            answer TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilities (
            player TEXT,
            round INTEGER,
            utility REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utility_nexts (
            player TEXT,
            round INTEGER,
            utility_next INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Update game state
def update_state(key, value):
    conn = sqlite3.connect("game_state.db")
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO game_state (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

# Get game state
def get_state(key):
    conn = sqlite3.connect("game_state.db")
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM game_state WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Add player response
def add_response(player, round_num, answer):
    conn = sqlite3.connect("game_state.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO responses (player, round, answer) VALUES (?, ?, ?)", (player, round_num, answer))
    conn.commit()
    conn.close()

# Get all responses for a round
def get_responses(round_num):
    conn = sqlite3.connect("game_state.db")
    cursor = conn.cursor()
    cursor.execute("SELECT player, answer FROM responses WHERE round = ?", (round_num,))
    results = cursor.fetchall()
    conn.close()
    return results

# Reset game state and responses
def reset_game():
    conn = sqlite3.connect("game_state.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM game_state")
    cursor.execute("DELETE FROM responses")
    cursor.execute("DELETE FROM utilities")
    cursor.execute("DELETE FROM utility_nexts")
    conn.commit()
    conn.close()

# Check if a player has already submitted a response for the current round
def has_submitted(player, round_num):
    conn = sqlite3.connect("game_state.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM responses WHERE player = ? AND round = ?", (player, round_num))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Add utility for each player for the current round
import json

def add_utility(player, round_num, utility):
    utility = utility.tolist()
    conn = sqlite3.connect("game_state.db")
    cursor = conn.cursor()

    # Check if a record already exists for this player and round
    cursor.execute("SELECT 1 FROM utilities WHERE player = ? AND round = ?", (player, round_num))
    if cursor.fetchone():
        # print(f"Utility for player '{player}' in round {round_num} already exists. Skipping insert.")
        pass
    else:
        utility_json = json.dumps(utility)  # Convert list to JSON
        cursor.execute("INSERT INTO utilities (player, round, utility) VALUES (?, ?, ?)", (player, round_num, utility_json))
    conn.commit()
    conn.close()


# Get all utilities for a round
def get_utilities(round_num, player_name):
    conn = sqlite3.connect("game_state.db")
    cursor = conn.cursor()
    cursor.execute("SELECT utility FROM utilities WHERE round = ? AND player = ?", (round_num, player_name))
    results = cursor.fetchall()
    conn.close()

    utilities = []
    for result in results:
        try:
            if result[0]:  # Ensure the value is not empty or None
                utilities.append(json.loads(result[0]))
        except json.JSONDecodeError as e:
            print(f"Error decoding utility for round {round_num}, player {player_name}: {e}")
    return utilities


# Add player position for the current round
def add_position(player, round_num, position):
    conn = sqlite3.connect("game_state.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO positions (player, round, position) VALUES (?, ?, ?)", (player, round_num, position))
    conn.commit()
    conn.close()

# Get all positions for a round
def get_positions(round_num):
    conn = sqlite3.connect("game_state.db")
    cursor = conn.cursor()
    cursor.execute("SELECT player, position FROM positions WHERE round = ?", (round_num,))
    results = cursor.fetchall()
    conn.close()
    return results

# Add utility factor for next concert for each player for the current round
def add_utility_next(player, round_num, utility_next):
    conn = sqlite3.connect("game_state.db")
    cursor = conn.cursor()

    # Check if a record already exists for this player and round
    cursor.execute("SELECT 1 FROM utility_nexts WHERE player = ? AND round = ?", (player, round_num))
    if cursor.fetchone():  # If a record exists
        # print(f"Utility factor for player '{player}' in round {round_num} already exists. Skipping insert.")
        pass
    else:
        # Insert the utility factor if no record exists
        cursor.execute("INSERT INTO utility_nexts (player, round, utility_next) VALUES (?, ?, ?)", (player, round_num, utility_next))
        # print(f"Utility factor added for player '{player}' in round {round_num}.")
    conn.commit()
    conn.close()

# Get all utility factors for next concert for a round for a name
def get_utility_nexts(round_num, name):
    conn = sqlite3.connect("game_state.db")
    cursor = conn.cursor()
    cursor.execute("SELECT utility_next FROM utility_nexts WHERE round = ? AND player = ?", (round_num, name))
    results = cursor.fetchone()
    conn.close()
    return results

