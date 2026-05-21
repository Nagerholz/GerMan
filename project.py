import sqlite3
#import uuid

conn = sqlite3.connect('/home/daniel/Documents/Schule/Prog/Programmieren/Project/HardwareDB.db')
cursor = conn.cursor()  #curser() erstellt ein object das SQL befehle ausführen kann
cursor.execute("""CREATE TABLE IF NOT EXISTS Hardware (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Gerätekategorie TEXT NOT NULL,
                    Hersteller TEXT NOT NULL,
                    Modell TEXT NOT NULL,
                    IP_Adresse TEXT NOT NULL,
                    MAC_Adresse TEXT,
                    Standort TEXT NOT NULL,
                    Status TEXT NOT NULL,
                    Beschreibung TEXT
)""")
conn.commit

"""
# Generiert eine *verlässliche* zufällige Zahl
uniqueID = uuid.uuid4()
print(uniqueID)
"""