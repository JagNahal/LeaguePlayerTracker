import sqlite3
from league_scraper import func

user = input("enter account name and tagline: ")
matches = func(user)

db = user + ".db"
# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db)

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS matches
                  (id INTEGER PRIMARY KEY, uid FLOAT, date TEXT, champion TEXT, result TEXT, kill INTEGER,
               death INTEGER, assist INTEGER, kda_r FLOAT, kp INTEGER, cstotal INT, csmin FLOAT)''')


# Insert a row of data
for match in matches:
    cursor.execute("INSERT INTO matches (uid, date, champion, result, kill, death, assist, kda_r, kp, cstotal, csmin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (match[0], match[1], match[2], match[3], match[4], match[5], match[6], match[7], match[8], match[9], match[10]))

# Save (commit) the changes
conn.commit()

# Query the database
cursor.execute('SELECT * FROM matches')
print(cursor.fetchall())

# Close the connection
conn.close()
