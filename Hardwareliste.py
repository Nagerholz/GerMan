import sqlite3

conn = sqlite3.connect('/home/daniel/Documents/Schule/Prog/Programmieren/Project/HardwareDB.db')
cursor = conn.cursor()  #curser() erstellt ein object das SQL befehle ausführen kann

cursor.execute("""CREATE TABLE IF NOT EXISTS Standort (
                    Kürzel TEXT PRIMARY KEY,
                    Raum TEXT NOT NULL,
                    Adresse TEXT NOT NULL,
                    Stadt TEXT NOT NULL,
                    Postleitzahl TEXT NOT NULL
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Gerät (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Gerätekategorie TEXT NOT NULL,
                    Hersteller TEXT NOT NULL,
                    Modell TEXT NOT NULL,
                    IP_Adresse TEXT NOT NULL,
                    MAC_Adresse TEXT,
                    Status TEXT NOT NULL,
                    Beschreibung TEXT,
                    Kostenstelle TEXT NOT NULL,
                    Standort TEXT NOT NULL,
                    FOREIGN KEY (Standort) REFERENCES Standort(Kürzel)
)""")
conn.commit()