import sqlite3

conn = sqlite3.connect('/home/daniel/Documents/Schule/Prog/Programmieren/Project/testBank.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS testBenutzer (name TEXT, age INTEGER)')
#cursor.execute("INSERT INTO testBenutzer VALUES ('hallo', 123)")
conn.commit()

cursor.execute('SELECT * FROM testBenutzer')
result = cursor.fetchall()

#cursor.execute('DELETE FROM testBenutzer')
#conn.commit()

data = [
    ("Hallo", 1),
    ("pubg", 2),
    ("WoW", 3)
]
conn.executemany('INSERT INTO testBenutzer (name, age) VALUES (?, ?)', data)
conn.commit()

for row in result:
    print(f'fortnite: {row[0]}, brawlstars: {row[1]}')

"""
#Gibt einen Datensatz aus
cursor.execute('SELECT * FROM testBenutzer')
result = cursor.fetchone()
print(f'fortnite: {result[0]}, brawlstars: {result[1]}')
"""

conn.close()