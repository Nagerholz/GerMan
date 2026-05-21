import sqlite3

conn = sqlite3.connect('/home/daniel/Documents/Schule/Prog/Programmieren/Project/HardwareDB.db')
cursor = conn.cursor()  #curser() erstellt ein object das SQL befehle ausführen kann

#cursor.execute("""CREATE TABLE IF NOT EXISTS Kostenstelle (
#                   Nummer TEXT PRIMARY KEY,
#                    Besitzer TEXT NOT NULL
#)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Standort (
                    Kürzel TEXT PRIMARY KEY,
                    Raum TEXT NOT NULL,
                    Adresse TEXT NOT NULL,
                    Stadt TEXT NOT NULL,
                    Postleitzahl TEXT NOT NULL
)""")


#Gejointe Tabelle für Kostenstelle und Standort, da diese N zu N sind
#cursor.execute(""" CREATE TABLE IF NOT EXISTS Kostenstelle_Standort (
#                    Kürzel TEXT NOT NULL,
#                    Nummer TEXT NOT NULL,
#                    PRIMARY KEY (Kürzel, Nummer),
#                    FOREIGN KEY (Kürzel) REFERENCES Standort(Kürzel),
#                    FOREIGN KEY (Nummer) REFERENCES Kostenstelle(Nummer)
#)""")

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


"""Hinzufügen:
gerätename = input
Kategerie = inpput
...

if geräte name Korrekt dann  x=gerätename
...

cursor.execute("INSERT INTO Gerät (?, ?, ?), gerätename, kategorie, forntine)
"""