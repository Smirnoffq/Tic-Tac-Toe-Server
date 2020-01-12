import sqlite3
import os

database_filename = "tic_tac_toe.db"

if os.path.isfile(database_filename):
    print("Database already exists")
    exit()

print("Creating database file...")
connection = sqlite3.connect(database_filename)
cursor = connection.cursor()

print("Creating players table...")
cursor.execute('''
    CREATE TABLE players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        mmr INTEGER DEFAULT 1000
    )
''')

print("Creating games table...")
cursor.execute('''
    CREATE TABLE games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player1Id INTEGER NULL,
        player2Id INTEGER NULL,
        winnerId INTEGER NULL,
        FOREIGN KEY (player1Id)
            REFERENCES players (id),
        FOREIGN KEY (player2Id)
            REFERENCES players (id),
        FOREIGN KEY (winnerId)
            REFERENCES players (id)
    )
''')

connection.commit()
connection.close()

print("Database created successfully...")