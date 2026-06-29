from logik import datenbank
from logik import logik


# Suchen
def suchen():
    print("\nWas möchtest du suchen?")
    searchInput = input("1 - Standort\n2 - Gerät\n--- Deine Wahl: ---\n")

    match searchInput:
        case "1":
            print("\nWonach möchtest du suchen?")
            suchbegriff = logik.pflichtfeld("Kürzel / Adresse / Stadt: ").strip()

            datenbank.cursor.execute("""SELECT * FROM Standort 
                                WHERE Kürzel = ? 
                                OR Adresse = ? 
                                OR Stadt = ?""",
                            (suchbegriff,) * 3)
            ergebnis = datenbank.cursor.fetchall()

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
            suchbegriff = logik.pflichtfeld("ID / Kategorie / Hersteller / Modell / IP / Status / Kostenstelle: ").strip()

            datenbank.cursor.execute("""SELECT * FROM Gerät 
                                WHERE CAST(ID AS TEXT) = ?
                                OR Gerätekategorie = ?
                                OR Hersteller = ?
                                OR Modell = ?
                                OR IP_Adresse = ?
                                OR Status = ?
                                OR Kostenstelle = ?
                                OR Standort = ?""",
                            (suchbegriff,) * 8)
            ergebnis = datenbank.cursor.fetchall()

            if ergebnis:
                print(f"\n{len(ergebnis)} Ergebnis(se) gefunden:")
                print(f"{'ID':<7} | {'Kategorie':<20} | {'Hersteller':<20} | {'Modell':<20} | {'IP':<17} | {'MAC':<19} | {'Status':<14} | {'Beschreibung':<20} | {'Kostenstelle':<15} | {'Standort':<12}")
                print("-" * 178)
                for g in ergebnis:
                    print(f"{g[0]:<7} | {g[1]:<20} | {g[2]:<20} | {g[3]:<20} | {g[4]:<17} | {str(g[5] or '-'):<19} | {g[6]:<14} | {str(g[7] or '-'):<20} | {g[8]:<15} | {g[9]:<12}")
            else:
                print(f"Keine Geräte mit '{suchbegriff}' gefunden.")

        case _:
            print("Ungültige Eingabe!")