import sqlite3


def connect():
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS User (
     username VARCHAR(60),
     password VARCHAR (60),
     score INTEGER
     );
     """)
    connection.commit()
    connection.close()



def username_exists(username):
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()
    # Use a parameterized query to prevent SQL injection
    cursor.execute("SELECT COUNT(*) FROM User WHERE username = ?", (username,))
    count = cursor.fetchone()[0]

    connection.close()

    return count > 0


def is_password_correct(username, password):
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT password FROM User WHERE username = ?", (username,))
    stored_password = cursor.fetchone()

    connection.close()

    if stored_password is None:
        return -1  # User does not exist
    else:
        return stored_password[0] == password  # Return True if passwords match


def add_user(username, password, score):
    if username_exists(username):
        print(f"User '{username}' already exists.")
        return False

    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO User (username, password, score) VALUES (?, ?, ?)", (username, password, score))

    connection.commit()
    connection.close()

    print(f"User '{username}' added successfully.")
    return True
connect()