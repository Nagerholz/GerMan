import sqlite3
import os

#Pfad dynamisch ermitteln, __file__ --> Aktueller Pfad des Programms
#os.path.abspath() --> Absoluter Pfadname
#os.path.dirname() nimmt nur den Ordner aus dem Pfad
#os.path.join() hängt Dateinamen dran
db_pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "HardwareDB.db")
conn = sqlite3.connect(db_pfad)
cursor = conn.cursor() #curser() erstellt ein object das SQL befehle ausführen kann

"""Hardcoded Pfad zur Datenbank --> Keine Pfad eingabe speichert die DB irgendwo im usr folder, nur in Linux der Fall (?)
conn = sqlite3.connect('DEIN PFAD')
cursor = conn.cursor()  #curser() erstellt ein object das SQL befehle ausführen kann
"""

cursor.execute("""CREATE TABLE IF NOT EXISTS Standort (
                    Kürzel TEXT PRIMARY KEY,
                    Räume TEXT NOT NULL,
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