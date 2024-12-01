import sqlite3

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
