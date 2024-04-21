import sqlite3

def get_db_connection():
    """Create and return a database connection."""
    return sqlite3.connect('user_data4.db')

def setup_database():
    """Set up the database table if it doesn't already exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            phone TEXT UNIQUE,
            secret TEXT
        )
    """)
    conn.commit()
    conn.close()

def is_existing_user(username):
    """Check if a user already exists with the given username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def is_existing_phone(phone):
    """Check if a phone number is already registered."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE phone = ?", (phone,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_user_to_db(username, password, phone, secret):
    """Save a new user to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, phone, secret) VALUES (?, ?, ?, ?)",
                   (username, password, phone, secret))
    conn.commit()
    conn.close()

def get_user_data(username):
    """Retrieve user data based on the username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT phone, secret FROM users WHERE username = ?", (username,))
    data = cursor.fetchone()
    conn.close()
    return data  # This is a tuple with (phone, secret)

def get_username_by_phone(phone):
    """Retrieve username based on the phone number."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE phone = ?", (phone,))
    data = cursor.fetchone()
    conn.close()
    return data

def update_user_secret(username, secret):
    """Update the user's secret (OTP) in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET secret = ? WHERE username = ?", (secret, username))
    conn.commit()
    conn.close()

def update_user_password(username, new_password):
    """Update the user's password in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
    conn.commit()
    conn.close()