import sqlite3  
import re

#  ██████╗ ███████╗██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
# ██╔════╝ ██╔════╝██╔══██╗████╗ ████║██╔══██╗████╗  ██║
# ██║  ███╗█████╗  ██████╔╝██╔████╔██║███████║██╔██╗ ██║
# ██║   ██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══██║██║╚██╗██║
# ╚██████╔╝███████╗██║  ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║
#  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝


conn = sqlite3.connect('/home/daniel/Documents/Schule/Prog/Programmieren/Project/HardwareDB.db')
cursor = conn.cursor()  #curser() erstellt ein object das SQL befehle ausführen kann

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

#fragt solange pflichtfelder ab bis sie gefüllt sind
def pflichtfeld(pflichteingabe):
    while True:
        wert = input(pflichteingabe).strip()
        if wert:
            return wert
        print("Dieses Feld ist Pflicht, bitte ausfüllen!")

def ipEingabe(eingabe):
    muster = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    while True:
        wert = input(eingabe).strip()
        if re.match(muster, wert):
            # Prüfen ob jede Zahl zwischen 0-255 liegt
            teile = wert.split(".")
            if all(0 <= int(t) <= 255 for t in teile):
                return wert
        print("Ungültige IP-Adresse! Erwartet: z.B 192.168.1.1")

def macEingabe(eingabe):
    # Akzeptiert XX:XX:XX:XX:XX:XX
    muster = r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"
    while True:
        wert = input(eingabe).strip()
        if not wert:
            return None  # Optional
        if re.match(muster, wert):
            return wert.upper()
        print("Ungültige MAC-Adresse! Erwartet: z.B. AA:BB:CC:DD:EE:FF")

def statusEingabe():
    optionen = {"1": "Aktiv", "2": "Defekt", "3": "Ausgemustert"}
    print("Status:")
    for key, val in optionen.items():
        print(f"  {key} - {val}")
    while True:
        wert = input("Auswahl: ").strip()
        if wert in optionen:
            return optionen[wert]
        print("Bitte 1, 2 oder 3 eingeben!\nStatus:")
        for key, val in optionen.items():
            print(f"  {key} - {val}")


"""
#Hinzufügen
sql = "INSERT INTO Standort (Kürzel, Räume, Adresse, Stadt, Postleitzahl) VALUES (?, ?, ?, ?, ?)"
val = ("ITEN", "3", "Janstraße 1", "Engen", "78234")
cursor.execute(sql, val)
conn.commit()
"""

#What to do?
print("Was willst du?")
doInput = input("1 - Hinzufügen\n2 - Anzeigen\n3 - Suchen\n4 - Bearbeiten\n5 - Löschen\n--- Deine Wahl: ---\n")

match doInput:
    case "1":
        #Hinzufügen
        print("\nEinen Standort oder Gerät hinzufügen?")
        wahlInput = input("1 - Standort\n2 - Gerät\n")

        match wahlInput:
            case "1":

                #Verfügbare Standorte anzeigen
                cursor.execute("SELECT Kürzel FROM Standort")
                standorte = [row[0] for row in cursor.fetchall()]
                if standorte:
                    print(f"\nVerfügbare Standorte: {', '.join(standorte)}")
                else:
                    print("\nKeine Standorte vorhanden! Bitte zuerst einen Standort anlegen.")

                print("--- Neuen Standort hinzufügen ---")
                kürzel      = pflichtfeld("Kürzel: ")
                räume       = pflichtfeld("Anzahl Räume: ")
                adresse     = pflichtfeld("Adresse: ")
                stadt       = pflichtfeld("Stadt: ")
                postleitzahl = pflichtfeld("Postleitzahl: ")

                befehl = "INSERT INTO Standort (Kürzel, Räume, Adresse, Stadt, Postleitzahl) VALUES (?, ?, ?, ?, ?)"
                inserts = (kürzel, räume, adresse, stadt, postleitzahl)

                #Try Block mir IntegrityError um Key zu checken.
                try:
                    cursor.execute(befehl, inserts)
                    conn.commit()
                    print(f"Standort '{kürzel}' erfolgreich hinzugefügt!")
                except sqlite3.IntegrityError:
                    print(f"Fehler: Kürzel '{kürzel}' existiert bereits!")

            case "2":
                print("\n--- Neues Gerät hinzufügen ---")
                

                gerätekategorie = pflichtfeld("Gerätekategorie: ")
                hersteller      = pflichtfeld("Hersteller: ")
                modell          = pflichtfeld("Modell: ")
                ip_adresse      = ipEingabe("IP-Adresse: ")
                mac_adresse     = macEingabe("MAC-Adresse (optional, Enter überspringen): ")
                status          = statusEingabe()
                beschreibung    = input("Beschreibung (optional): ")
                kostenstelle    = pflichtfeld("Kostenstelle: ")

                #Verfügbare Standorte anzeigen
                cursor.execute("SELECT Kürzel FROM Standort")
                standorte = [row[0] for row in cursor.fetchall()]
                if standorte:
                    print(f"Verfügbare Standorte: {', '.join(standorte)}")
                else:
                    print("Keine Standorte vorhanden! Bitte zuerst einen Standort anlegen.")
                standort        = input("Standort-Kürzel: ").upper()

                if standorte and standort not in standorte:
                    print(f"\nFehler: Standort '{standort}' existiert nicht!")
                else:
                    befehl = """INSERT INTO Gerät 
                                (Gerätekategorie, Hersteller, Modell, IP_Adresse, MAC_Adresse,
                                Status, Beschreibung, Kostenstelle, Standort)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                    inserts = (gerätekategorie, hersteller, modell, ip_adresse, mac_adresse,
                            status, beschreibung, kostenstelle, standort)

                #Catch errors
                try:
                    cursor.execute(befehl, inserts)
                    conn.commit()
                    print(f"Gerät '{modell}' erfolgreich hinzugefügt (ID: {cursor.lastrowid})!")
                except sqlite3.Error as e:
                    print(f"Datenbankfehler: {e}")

            case _:
                print("Ungültige Eingabe :(")



    case "2":
        #Anzeigen
        print("\n--- Geräte ---")
        cursor.execute("""SELECT * FROM Gerät""")
        gerätAnzeige = cursor.fetchall()

        if gerätAnzeige:
            print(f"{'ID':<7} | {'Kategorie':<20} | {'Hersteller':<20} | {'Modell':<20} | {'IP':<17} | {'MAC':<19} | {'Status':<14}  | {'Kostenstelle':<15} | {'Standort':<12} | {'Beschreibung':<40}")
            print("-" * 175)
            for g in gerätAnzeige:
                print(f"{g[0]:<7} | {g[1]:<20} | {g[2]:<20} | {g[3]:<20} | {g[4]:<17} | {str(g[5] or '-'):<19} | {g[6]:<14}  | {g[8]:<15} | {g[9]:<12} | {g[7] or '-'}")

        print("\n=== Standorte ===")
        cursor.execute("""SELECT * FROM Standort""")
        standortAnzeige = cursor.fetchall()

        if standortAnzeige:
            print(f"{'Kürzel':<10} | {'Räume':<8} | {'Adresse':<25} | {'Stadt':<18} | {'Postleitzahl':<14}")
        print("-" * 85)
        for j in standortAnzeige:
            print(f"{j[0]:<10} | {j[1]:<8} | {j[2]:<25} | {j[3]:<18} | {j[4]:<14}")



    case "3":
        #Suchen
        print("\nWas möchtest du suchen?")
        searchInput = input("1 - Standort\n2 - Gerät\n--- Deine Wahl: ---\n")
    
        match searchInput:
            case "1":
                print("\nWonach möchtest du suchen?")
                suchbegriff = pflichtfeld("Kürzel / Adresse / Stadt: ").strip()

                cursor.execute("""SELECT * FROM Standort 
                                  WHERE Kürzel = ? 
                                  OR Adresse = ? 
                                  OR Stadt = ?""",
                               (suchbegriff,) * 3)
                ergebnis = cursor.fetchall()
    
                if ergebnis:
                    print(f"\n{len(ergebnis)} Ergebnis(se) gefunden:")
                    print(f"{'Kürzel':<10} | {'Räume':<8} | {'Adresse':<25} | {'Stadt':<18} | {'Postleitzahl':<14}")
                    print("-" * 85)
                    for j in ergebnis:
                        print(f"{j[0]:<10} | {j[1]:<8} | {j[2]:<25} | {j[3]:<18} | {j[4]:<14}")
                else:
                    print(f"Keine Standorte mit '{suchbegriff}' gefunden.")
    
            case "2":
                print("\nWonach möchtest du suchen?")
                suchbegriff = pflichtfeld("ID / Kategorie / Hersteller / Modell / IP / Status / Kostenstelle: ").strip()

                cursor.execute("""SELECT * FROM Gerät 
                                  WHERE CAST(ID AS TEXT) = ?
                                  OR Gerätekategorie = ?
                                  OR Hersteller = ?
                                  OR Modell = ?
                                  OR IP_Adresse = ?
                                  OR Status = ?
                                  OR Kostenstelle = ?
                                  OR Standort = ?""",
                               (suchbegriff,) * 8)
                ergebnis = cursor.fetchall()
    
                if ergebnis:
                    print(f"\n{len(ergebnis)} Ergebnis(se) gefunden:")
                    print(f"{'ID':<7} | {'Kategorie':<20} | {'Hersteller':<20} | {'Modell':<20} | {'IP':<17} | {'MAC':<19} | {'Status':<14} | {'Beschreibung':<20} | {'Kostenstelle':<15} | {'Standort':<12}")
                    print("-" * 178)
                    for g in ergebnis:
                        print(f"{g[0]:<7} | {g[1]:<20} | {g[2]:<20} | {g[3]:<20} | {g[4]:<17} | {str(g[5] or '-'):<19} | {g[6]:<14} | {str(g[7] or '-'):<20} | {g[8]:<15} | {g[9]:<12}")
                else:
                    print(f"Keine Geräte mit '{suchbegriff}' gefunden.")
    
            case _:
                print("Ungültige Eingabe :(")
    
    # case "4":
    #Bearbeiten
    case "4":
    # Bearbeiten
        print("\nWas möchtest du bearbeiten?")
        bearbeitenInput = input("1 - Standort\n2 - Gerät\n--- Deine Wahl: ---\n")

        match bearbeitenInput:
            case "1":
                # Alle Standorte anzeigen
                cursor.execute("SELECT * FROM Standort")
                standorte = cursor.fetchall()

                if not standorte:
                    print("Keine Standorte vorhanden!")
                else:
                    print(f"\n{'Kürzel':<10} | {'Räume':<8} | {'Adresse':<25} | {'Stadt':<18} | {'Postleitzahl':<14}")
                    print("-" * 85)
                    for j in standorte:
                        print(f"{j[0]:<10} | {j[1]:<8} | {j[2]:<25} | {j[3]:<18} | {j[4]:<14}")

                    kürzel = pflichtfeld("\nKürzel des zu bearbeitenden Standorts: ").strip().upper()

                    # Prüfen ob Standort existiert
                    cursor.execute("SELECT * FROM Standort WHERE Kürzel = ?", (kürzel,))
                    standort = cursor.fetchone()

                    if not standort:
                        print(f"Standort '{kürzel}' nicht gefunden!")
                    else:
                        print(f"\nAktuell: Kürzel={standort[0]}, Räume={standort[1]}, Adresse={standort[2]}, Stadt={standort[3]}, PLZ={standort[4]}")
                        print("(Enter drücken um Feld zu behalten)\n")

                        neues_kürzel     = input(f"Neues Kürzel [{standort[0]}]: ").strip().upper() or standort[0]
                        neue_räume       = input(f"Neue Räume [{standort[1]}]: ").strip() or standort[1]
                        neue_adresse     = input(f"Neue Adresse [{standort[2]}]: ").strip() or standort[2]
                        neue_stadt       = input(f"Neue Stadt [{standort[3]}]: ").strip() or standort[3]
                        neue_plz         = input(f"Neue Postleitzahl [{standort[4]}]: ").strip() or standort[4]

                        try:
                            cursor.execute("""UPDATE Standort 
                                              SET Kürzel = ?, Räume = ?, Adresse = ?, Stadt = ?, Postleitzahl = ?
                                              WHERE Kürzel = ?""",
                                           (neues_kürzel, neue_räume, neue_adresse, neue_stadt, neue_plz, kürzel))
                            conn.commit()
                            print(f"\nStandort '{kürzel}' erfolgreich aktualisiert!")
                        except sqlite3.IntegrityError:
                            print(f"Fehler: Kürzel '{neues_kürzel}' existiert bereits!")

            case "2":
                # Alle Geräte anzeigen
                cursor.execute("SELECT * FROM Gerät")
                geräte = cursor.fetchall()

                if not geräte:
                    print("Keine Geräte vorhanden!")
                else:
                    print(f"\n{'ID':<7} | {'Kategorie':<20} | {'Hersteller':<20} | {'Modell':<20} | {'IP':<17} | {'MAC':<19} | {'Status':<14} | {'Beschreibung':<20} | {'Kostenstelle':<15} | {'Standort':<12}")
                    print("-" * 178)
                    for g in geräte:
                        print(f"{g[0]:<7} | {g[1]:<20} | {g[2]:<20} | {g[3]:<20} | {g[4]:<17} | {str(g[5] or '-'):<19} | {g[6]:<14} | {str(g[7] or '-'):<20} | {g[8]:<15} | {g[9]:<12}")

                    geräte_id = pflichtfeld("\nID des zu bearbeitenden Geräts: ").strip()

                    cursor.execute("SELECT * FROM Gerät WHERE ID = ?", (geräte_id,))
                    gerät = cursor.fetchone()

                    if not gerät:
                        print(f"Gerät mit ID '{geräte_id}' nicht gefunden!")
                    else:
                        print(f"\nAktuelles Gerät: ID={gerät[0]}, Modell={gerät[3]}, Status={gerät[6]}")
                        print("(Enter drücken um Feld zu behalten)\n")

                        neue_kategorie   = input(f"Neue Kategorie [{gerät[1]}]: ").strip() or gerät[1]
                        neuer_hersteller = input(f"Neuer Hersteller [{gerät[2]}]: ").strip() or gerät[2]
                        neues_modell     = input(f"Neues Modell [{gerät[3]}]: ").strip() or gerät[3]
                        neue_ip          = input(f"Neue IP-Adresse [{gerät[4]}]: ").strip()
                        if neue_ip:
                            neue_ip = ipEingabe(f"Neue IP-Adresse [{gerät[4]}]: ")
                        else:
                            neue_ip = gerät[4]

                        neue_mac         = input(f"Neue MAC-Adresse [{gerät[5] or '-'}] (Enter überspringen): ").strip()
                        if neue_mac:
                            neue_mac = macEingabe(f"Neue MAC-Adresse: ")
                        else:
                            neue_mac = gerät[5]

                        # Status Auswahl anzeigen, aktuellen anzeigen
                        print(f"Aktueller Status: {gerät[6]}")
                        neuer_status     = input("Neuen Status wählen? (Enter überspringen): ").strip()
                        if neuer_status:
                            neuer_status = statusEingabe()
                        else:
                            neuer_status = gerät[6]

                        neue_beschreibung = input(f"Neue Beschreibung [{gerät[7] or '-'}]: ").strip() or gerät[7]
                        neue_kostenstelle = input(f"Neue Kostenstelle [{gerät[8]}]: ").strip() or gerät[8]

                        # Verfügbare Standorte anzeigen
                        cursor.execute("SELECT Kürzel FROM Standort")
                        standorte = [row[0] for row in cursor.fetchall()]
                        print(f"Verfügbare Standorte: {', '.join(standorte)}")
                        neuer_standort   = input(f"Neuer Standort [{gerät[9]}]: ").strip().upper() or gerät[9]

                        if neuer_standort not in standorte:
                            print(f"Fehler: Standort '{neuer_standort}' existiert nicht!")
                        else:
                            try:
                                cursor.execute("""UPDATE Gerät 
                                                  SET Gerätekategorie = ?, Hersteller = ?, Modell = ?, IP_Adresse = ?,
                                                      MAC_Adresse = ?, Status = ?, Beschreibung = ?, Kostenstelle = ?, Standort = ?
                                                  WHERE ID = ?""",
                                               (neue_kategorie, neuer_hersteller, neues_modell, neue_ip,
                                                neue_mac, neuer_status, neue_beschreibung, neue_kostenstelle,
                                                neuer_standort, geräte_id))
                                conn.commit()
                                print(f"\nGerät '{neues_modell}' (ID: {geräte_id}) erfolgreich aktualisiert!")
                            except sqlite3.Error as e:
                                print(f"Datenbankfehler: {e}")

            case _:
                print("Ungültige Eingabe :(")

    
    case "5":
    # Löschen
        print("\nWas möchtest du löschen?")
        löschenInput = input("1 - Standort\n2 - Gerät\n--- Deine Wahl: ---\n")

        match löschenInput:
            case "1":
                # Alle Standorte anzeigen
                cursor.execute("SELECT * FROM Standort")
                standorte = cursor.fetchall()

                if not standorte:
                    print("Keine Standorte vorhanden!")
                else:
                    print(f"\n{'Kürzel':<10} | {'Räume':<8} | {'Adresse':<25} | {'Stadt':<18} | {'Postleitzahl':<14}")
                    print("-" * 85)
                    for j in standorte:
                        print(f"{j[0]:<10} | {j[1]:<8} | {j[2]:<25} | {j[3]:<18} | {j[4]:<14}")

                    kürzel = pflichtfeld("\nKürzel des zu löschenden Standorts: ").strip().upper()

                    cursor.execute("SELECT * FROM Standort WHERE Kürzel = ?", (kürzel,))
                    standort = cursor.fetchone()

                    if not standort:
                        print(f"Standort '{kürzel}' nicht gefunden!")
                    else:
                        # Prüfen ob Geräte diesem Standort zugeordnet sind
                        cursor.execute("SELECT COUNT(*) FROM Gerät WHERE Standort = ?", (kürzel,))
                        anzahl_geräte = cursor.fetchone()[0]

                        if anzahl_geräte > 0:
                            print(f"Fehler: Standort '{kürzel}' hat noch {anzahl_geräte} Gerät(e) zugeordnet!")
                            print("Bitte zuerst die Geräte löschen oder einem anderen Standort zuweisen.")
                        else:
                            print(f"\nStandort '{kürzel}' ({standort[2]}, {standort[3]}) wird gelöscht.")
                            bestätigung = input("Bist du sicher? (ja/nein): ").strip().lower()

                            if bestätigung == "ja":
                                cursor.execute("DELETE FROM Standort WHERE Kürzel = ?", (kürzel,))
                                conn.commit()
                                print(f"Standort '{kürzel}' erfolgreich gelöscht!")
                            else:
                                print("Löschen abgebrochen.")

            case "2":
                # Alle Geräte anzeigen
                cursor.execute("SELECT * FROM Gerät")
                geräte = cursor.fetchall()

                if not geräte:
                    print("Keine Geräte vorhanden!")
                else:
                    print(f"\n{'ID':<7} | {'Kategorie':<20} | {'Hersteller':<20} | {'Modell':<20} | {'IP':<17} | {'MAC':<19} | {'Status':<14} | {'Beschreibung':<20} | {'Kostenstelle':<15} | {'Standort':<12}")
                    print("-" * 178)
                    for g in geräte:
                        print(f"{g[0]:<7} | {g[1]:<20} | {g[2]:<20} | {g[3]:<20} | {g[4]:<17} | {str(g[5] or '-'):<19} | {g[6]:<14} | {str(g[7] or '-'):<20} | {g[8]:<15} | {g[9]:<12}")

                    geräte_id = pflichtfeld("\nID des zu löschenden Geräts: ").strip()

                    cursor.execute("SELECT * FROM Gerät WHERE ID = ?", (geräte_id,))
                    gerät = cursor.fetchone()

                    if not gerät:
                        print(f"Gerät mit ID '{geräte_id}' nicht gefunden!")
                    else:
                        print(f"\nGerät ID={gerät[0]}, Modell={gerät[3]}, Hersteller={gerät[2]}, Standort={gerät[9]} wird gelöscht.")
                        bestätigung = input("Bist du sicher? (ja/nein): ").strip().lower()

                        if bestätigung == "ja":
                            cursor.execute("DELETE FROM Gerät WHERE ID = ?", (geräte_id,))
                            conn.commit()
                            print(f"Gerät '{gerät[3]}' (ID: {geräte_id}) erfolgreich gelöscht!")
                        else:
                            print("Löschen abgebrochen.")

            case _:
                print("Ungültige Eingabe :(")

    case _:
        print("Diese option exestiert nischt :(")



cursor.close()








