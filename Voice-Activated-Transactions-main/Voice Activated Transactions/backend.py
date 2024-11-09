import sqlite3

# Database connection
def create_connection():
    conn = sqlite3.connect("transactions.db")
    return conn

# Initialize database with predefined users
def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                           name TEXT PRIMARY KEY,
                           balance REAL,
                           username TEXT UNIQUE,
                           password TEXT
                       )''')
    
    # Predefined users with usernames matching their names and a default password "123"
    users = [
        ("Aarav", 50000, "Aarav", "123"),
        ("Vihaan", 50000, "Vihaan", "123"),
        ("Arjun", 50000, "Arjun", "123"),
        ("Vivaan", 50000, "Vivaan", "123"),
        ("Ayaan", 50000, "Ayaan", "123"),
        ("Reyansh", 50000, "Reyansh", "123"),
        ("Sai", 50000, "Sai", "123"),
        ("Karan", 50000, "Karan", "123"),
        ("Rohan", 50000, "Rohan", "123"),
        ("Dev", 50000, "Dev", "123")
    ]
    
    for name, balance, username, password in users:
        cursor.execute("INSERT OR IGNORE INTO accounts (name, balance, username, password) VALUES (?, ?, ?, ?)", 
                       (name, balance, username, password))
    
    conn.commit()
    conn.close()

# Check if login credentials are valid
def validate_login(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM accounts WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Add a new user to the database
def add_user(name, balance, username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO accounts (name, balance, username, password) VALUES (?, ?, ?, ?)", 
                   (name, balance, username, password))
    conn.commit()
    conn.close()

# Delete a user from the database
def delete_user(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accounts WHERE name=?", (name,))
    conn.commit()
    conn.close()

# Add or update account balance
def update_balance(name, amount):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE name=?", (name,))
    result = cursor.fetchone()

    if result:
        new_balance = result[0] + amount
        cursor.execute("UPDATE accounts SET balance=? WHERE name=?", (new_balance, name))
    else:
        cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, amount))

    conn.commit()
    conn.close()

# Retrieve account balance
def get_balance(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE name=?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Check if user exists
def user_exists(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM accounts WHERE name=?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Execute a transaction based on transcription
def process_transaction(transcription, sender_name):
    # Parse transcription to identify amount and receiver
    words = transcription.split()
    amount = None
    receiver = None

    for i, word in enumerate(words):
        if word.isdigit():  # Assuming amount is a digit in transcription
            amount = int(word)
        elif word.istitle() and word != sender_name:  # Assuming title case for names and ignoring sender's name
            receiver = word

    if amount and receiver:
        # Check if receiver exists
        if not user_exists(receiver):
            return f"User '{receiver}' does not exist. Please re-record the transaction.", None, None

        # Get sender's balance before transaction
        sender_balance_before = get_balance(sender_name)
        
        # Deduct amount from sender
        update_balance(sender_name, -amount)

        # Add amount to receiver
        update_balance(receiver, amount)
        
        # Get sender's balance after transaction
        sender_balance_after = get_balance(sender_name)

        return f"Transaction of {amount} Rs from {sender_name} to {receiver} completed.", sender_balance_before, sender_balance_after
    else:
        return "Could not process the transaction. Please ensure the transcription includes a valid amount and receiver.", None, None
