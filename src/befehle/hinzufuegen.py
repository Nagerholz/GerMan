from logik import datenbank
from logik import logik


# Hinzufügen
def hinzufugen():
    print("\nEinen Standort oder Gerät hinzufügen?")
    wahlInput = input("1 - Standort\n2 - Gerät\n3 - Abbrechen\n")

    match wahlInput:
        case "1":

            #Verfügbare Standorte anzeigen
            datenbank.cursor.execute("SELECT Kürzel FROM Standort")
            standorte = [row[0] for row in datenbank.cursor.fetchall()]
            if standorte:
                print(f"\nVerfügbare Standorte: {', '.join(standorte)}")
            else:
                print("\nKeine Standorte vorhanden! Bitte zuerst einen Standort anlegen.")

            print("--- Neuen Standort hinzufügen ---")
            kürzel      = logik.pflichtfeld("Kürzel: ")
            räume       = logik.pflichtfeld("Anzahl Räume: ")
            adresse     = logik.pflichtfeld("Adresse: ")
            stadt       = logik.pflichtfeld("Stadt: ")
            postleitzahl = logik.pflichtfeld("Postleitzahl: ")

            befehl = "INSERT INTO Standort (Kürzel, Räume, Adresse, Stadt, Postleitzahl) VALUES (?, ?, ?, ?, ?)"
            inserts = (kürzel, räume, adresse, stadt, postleitzahl)

            #Try Block mir IntegrityError um Key zu checken.
            try:
                datenbank.cursor.execute(befehl, inserts)
                datenbank.conn.commit()
                print(f"Standort '{kürzel}' erfolgreich hinzugefügt!")
            except datenbank.sqlite3.IntegrityError:
                print(f"Fehler: Kürzel '{kürzel}' existiert bereits!")

        case "2":
            print("\n--- Neues Gerät hinzufügen ---")
            
            #Verfügbare Standorte anzeigen
            datenbank.cursor.execute("SELECT Kürzel FROM Standort")
            standorte = [row[0] for row in datenbank.cursor.fetchall()]
            if standorte:
                print(f"Verfügbare Standorte: {', '.join(standorte)}")
            else:
                print("Keine Standorte vorhanden! Bitte zuerst einen Standort anlegen.")
                pass

            while True:     
                standort = input("Standort-Kürzel: ").upper()

                if standorte and standort not in standorte:
                    print(f"\nFehler: Standort '{standort}' existiert nicht!")
                else:
                    break
                
            gerätekategorie = logik.setzeKategorie()
            hersteller      = logik.pflichtfeld("Hersteller: ")
            modell          = logik.pflichtfeld("Modell: ")
            ip_adresse      = logik.ipEingabe("IP-Adresse: ")
            mac_adresse     = logik.macEingabe("MAC-Adresse (optional, Enter überspringen): ")
            status          = logik.statusEingabe()
            beschreibung    = input("Beschreibung (optional): ")
            kostenstelle    = logik.pflichtfeld("Kostenstelle: ")

            befehl = """INSERT INTO Gerät 
                        (Gerätekategorie, Hersteller, Modell, IP_Adresse, MAC_Adresse,
                        Status, Beschreibung, Kostenstelle, Standort)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            inserts = (gerätekategorie, hersteller, modell, ip_adresse, mac_adresse,
                    status, beschreibung, kostenstelle, standort)

            #Catch errors
            try:
                datenbank.cursor.execute(befehl, inserts)
                datenbank.conn.commit()
                print(f"Gerät '{modell}' erfolgreich hinzugefügt (ID: {datenbank.cursor.lastrowid})!")
            except datenbank.sqlite3.Error as e:
                print(f"Datenbankfehler: {e}")
        case "3":
            pass
        case _:
            print("Ungültige Eingabe!")
