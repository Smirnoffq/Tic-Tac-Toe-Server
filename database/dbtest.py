import sqlite3
import os

database_filename = "tic_tac_toe.db"

if not os.path.isfile(database_filename):
    print("Database does not exist")
    exit()

connection = sqlite3.connect(database_filename)
cursor = connection.cursor()

print("Inserting 3 players...")
cursor.execute('INSERT INTO players (name) VALUES ("Test Player")')
cursor.execute('INSERT INTO players (name) VALUES ("Test Player2")')
cursor.execute('INSERT INTO players (name) VALUES ("Test Player3")')
connection.commit()

result = cursor.execute('''
    SELECT * FROM players
''')
result = result.fetchall()

if len(result) <= 0:
    print("Couldn't insert Test Players...")
    exit()
else:
    for row in result:
        print(row)

print("Removing 3 players...")
cursor.execute('DELETE FROM players WHERE name LIKE "Test Player%"')
connection.commit()

result = cursor.execute('''
    SELECT * FROM players
''')
result = result.fetchall()

if len(result) <= 0:
    print("Removing done successfully...")
else:
    for row in result:
        print(row)

connection.close()