import sqlite3

connect = sqlite3.connect("password_saves.db")
cursor = connect.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Passwords(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_message TEXT,
    type TEXT,
    result TEXT
)
""")

connect.commit()
connect.close()

print("Done")
