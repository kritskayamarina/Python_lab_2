import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
)''')

c.execute('''CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL
)''')

c.execute("INSERT OR IGNORE INTO users (username, password, email) "
          "VALUES ('alice', 'alice123', 'alice@example.com')")
c.execute("INSERT OR IGNORE INTO users (username, password, email) "
          "VALUES ('bob', 'bob123', 'bob@example.com')")

conn.commit()
conn.close()
print("Database initialized.")
