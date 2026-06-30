from logik import datenbank
from logik import logik


# Löschen
def loeschen():
    print("\nWas möchtest du löschen?")
    löschenInput = input("1 - Standort\n2 - Gerät\n--- Ihre Wahl ---\n")

    match löschenInput:
        case "1":
            # Alle Standorte anzeigen
            datenbank.cursor.execute("SELECT * FROM Standort")
            standorte = datenbank.cursor.fetchall()

            if not standorte:
                print("Keine Standorte vorhanden!")
            else:
                print(f"\n{'Kürzel':<10} | {'Räume':<8} | {'Adresse':<25} | {'Stadt':<18} | {'Postleitzahl':<14}")
                print("-" * 85)
                for j in standorte:
                    print(f"{j[0]:<10} | {j[1]:<8} | {j[2]:<25} | {j[3]:<18} | {j[4]:<14}")

                kürzel = logik.pflichtfeld("\nKürzel des zu löschenden Standorts: ").strip().upper()

                datenbank.cursor.execute("SELECT * FROM Standort WHERE Kürzel = ?", (kürzel,))
                standort = datenbank.cursor.fetchone()

                if not standort:
                    print(f"Standort '{kürzel}' nicht gefunden!")
                else:
                    # Prüfen ob Geräte diesem Standort zugeordnet sind
                    datenbank.cursor.execute("SELECT COUNT(*) FROM Gerät WHERE Standort = ?", (kürzel,))
                    anzahl_geräte = datenbank.cursor.fetchone()[0]

                    if anzahl_geräte > 0:
                        print(f"Fehler: Standort '{kürzel}' hat noch {anzahl_geräte} Gerät(e) zugeordnet!")
                        print("Bitte zuerst die Geräte löschen oder einem anderen Standort zuweisen.")
                    else:
                        print(f"\nStandort '{kürzel}' ({standort[2]}, {standort[3]}) wird gelöscht.")
                        bestätigung = input("Bist du sicher? (ja/nein): ").strip().lower()

                        if bestätigung.lower() == "ja" or bestätigung.lower() == "j":
                            datenbank.cursor.execute("DELETE FROM Standort WHERE Kürzel = ?", (kürzel,))
                            datenbank.conn.commit()
                            print(f"Standort '{kürzel}' erfolgreich gelöscht!")
                        else:
                            print("Löschen abgebrochen.")

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

                geräte_id = logik.pflichtfeld("\nID des zu löschenden Geräts: ").strip()

                datenbank.cursor.execute("SELECT * FROM Gerät WHERE ID = ?", (geräte_id,))
                gerät = datenbank.cursor.fetchone()

                if not gerät:
                    print(f"Gerät mit ID '{geräte_id}' nicht gefunden!")
                else:
                    print(f"\nGerät ID={gerät[0]}, Modell={gerät[3]}, Hersteller={gerät[2]}, Standort={gerät[9]} wird gelöscht.")
                    bestätigung = input("Bist du sicher? (ja/nein): ").strip().lower()

                    if bestätigung.lower() == "ja" or bestätigung.lower() == "j":
                        datenbank.cursor.execute("DELETE FROM Gerät WHERE ID = ?", (geräte_id,))
                        datenbank.conn.commit()
                        print(f"Gerät '{gerät[3]}' (ID: {geräte_id}) erfolgreich gelöscht!")
                    else:
                        print("Löschen abgebrochen.")

        case _:
            print("Ungültige Eingabe :(")