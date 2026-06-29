from logik import datenbank
from logik import logik


# Bearbeiten
def bearbeiten():
    print("\nWas möchtest du bearbeiten?")
    bearbeitenInput = input("1 - Standort\n2 - Gerät\n--- Deine Wahl: ---\n")

    match bearbeitenInput:
        case "1":
            # Alle Standorte anzeigen
            datenbank.cursor.execute("SELECT * FROM Standort")
            standorte = datenbank.curso.fetchall()

            if not standorte:
                print("Keine Standorte vorhanden!")
            else:
                print(f"\n{'Kürzel':<10} | {'Räume':<8} | {'Adresse':<25} | {'Stadt':<18} | {'Postleitzahl':<14}")
                print("-" * 85)
                for j in standorte:
                    print(f"{j[0]:<10} | {j[1]:<8} | {j[2]:<25} | {j[3]:<18} | {j[4]:<14}")

                kürzel = logik.pflichtfeld("\nKürzel des zu bearbeitenden Standorts: ").strip().upper()

                # Prüfen ob Standort existiert
                datenbank.cursor.execute("SELECT * FROM Standort WHERE Kürzel = ?", (kürzel,))
                standort = datenbank.cursor.fetchone()

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
                        datenbank.cursor.execute("""UPDATE Standort 
                                            SET Kürzel = ?, Räume = ?, Adresse = ?, Stadt = ?, Postleitzahl = ?
                                            WHERE Kürzel = ?""",
                                        (neues_kürzel, neue_räume, neue_adresse, neue_stadt, neue_plz, kürzel))
                        datenbank.conn.commit()
                        print(f"\nStandort '{kürzel}' erfolgreich aktualisiert!")
                    except datenbank.sqlite3.IntegrityError:
                        print(f"Fehler: Kürzel '{neues_kürzel}' existiert bereits!")

        case "2":
            # Alle Geräte anzeigen
            datenbank.cursor.execute("SELECT * FROM Gerät")
            geräte = datenbank.cursor.fetchall()

            if not geräte:
                print("Keine Geräte vorhanden!")
            else:
                print(f"\n{'ID':<7} | {'Kategorie':<20} | {'Hersteller':<20} | {'Modell':<20} | {'IP':<17} | {'MAC':<19} | {'Status':<14} | {'Beschreibung':<20} | {'Kostenstelle':<15} | {'Standort':<12}")
                print("-" * 178)
                for g in geräte:
                    print(f"{g[0]:<7} | {g[1]:<20} | {g[2]:<20} | {g[3]:<20} | {g[4]:<17} | {str(g[5] or '-'):<19} | {g[6]:<14} | {str(g[7] or '-'):<20} | {g[8]:<15} | {g[9]:<12}")

                geräte_id = logik.pflichtfeld("\nID des zu bearbeitenden Geräts: ").strip()

                datenbank.cursor.execute("SELECT * FROM Gerät WHERE ID = ?", (geräte_id,))
                gerät = datenbank.cursor.fetchone()

                if not gerät:
                    print(f"Gerät mit ID '{geräte_id}' nicht gefunden!")
                else:
                    print(f"\nAktuelles Gerät: ID={gerät[0]}, Modell={gerät[3]}, Status={gerät[6]}")
                    print("(Enter drücken um Feld zu behalten)\n")

                    print((f"Neue Kategorie [{gerät[1]}]: ").strip() or gerät[1])
                    neue_kategorie = logik.setzeKategorie()
                    neuer_hersteller = input(f"Neuer Hersteller [{gerät[2]}]: ").strip() or gerät[2]
                    neues_modell     = input(f"Neues Modell [{gerät[3]}]: ").strip() or gerät[3]
                    neue_ip          = input(f"Neue IP-Adresse [{gerät[4]}]: ").strip()
                    if neue_ip:
                        neue_ip = logik.ipEingabe(f"Neue IP-Adresse [{gerät[4]}]: ")
                    else:
                        neue_ip = gerät[4]

                    neue_mac         = input(f"Neue MAC-Adresse [{gerät[5] or '-'}] (Enter überspringen): ").strip()
                    if neue_mac:
                        neue_mac = logik.macEingabe(f"Neue MAC-Adresse: ")
                    else:
                        neue_mac = gerät[5]

                    # Status Auswahl anzeigen, aktuellen anzeigen
                    print(f"Aktueller Status: {gerät[6]}")
                    neuer_status     = input("Neuen Status wählen? (Enter überspringen): ").strip()
                    if neuer_status:
                        neuer_status = logik.statusEingabe()
                    else:
                        neuer_status = gerät[6]

                    neue_beschreibung = input(f"Neue Beschreibung [{gerät[7] or '-'}]: ").strip() or gerät[7]
                    neue_kostenstelle = input(f"Neue Kostenstelle [{gerät[8]}]: ").strip() or gerät[8]

                    # Verfügbare Standorte anzeigen
                    datenbank.cursor.execute("SELECT Kürzel FROM Standort")
                    standorte = [row[0] for row in datenbank.cursor.fetchall()]
                    print(f"Verfügbare Standorte: {', '.join(standorte)}")
                    neuer_standort   = input(f"Neuer Standort [{gerät[9]}]: ").strip().upper() or gerät[9]

                    if neuer_standort not in standorte:
                        print(f"Fehler: Standort '{neuer_standort}' existiert nicht!")
                    else:
                        try:
                            datenbank.cursor.execute("""UPDATE Gerät 
                                                SET Gerätekategorie = ?, Hersteller = ?, Modell = ?, IP_Adresse = ?,
                                                    MAC_Adresse = ?, Status = ?, Beschreibung = ?, Kostenstelle = ?, Standort = ?
                                                WHERE ID = ?""",
                                            (neue_kategorie, neuer_hersteller, neues_modell, neue_ip,
                                            neue_mac, neuer_status, neue_beschreibung, neue_kostenstelle,
                                            neuer_standort, geräte_id))
                            datenbank.conn.commit()
                            print(f"\nGerät '{neues_modell}' (ID: {geräte_id}) erfolgreich aktualisiert!")
                        except datenbank.sqlite3.Error as e:
                            print(f"Datenbankfehler: {e}")

        case _:
            print("Ungültige Eingabe :(")