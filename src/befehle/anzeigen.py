from logik import datenbank


# Anzeigen
def anzeigen():
    print("\n--- Geräte ---")
    datenbank.cursor.execute("""SELECT * FROM Gerät""")
    gerätAnzeige = datenbank.cursor.fetchall()

    if gerätAnzeige:
        print(f"{'ID':<7} | {'Kategorie':<20} | {'Hersteller':<20} | {'Modell':<20} | {'IP':<17} | {'MAC':<19} | {'Status':<14}  | {'Kostenstelle':<15} | {'Standort':<12} | {'Beschreibung':<40}")
        print("-" * 175)
        for g in gerätAnzeige:
            print(f"{g[0]:<7} | {g[1]:<20} | {g[2]:<20} | {g[3]:<20} | {g[4]:<17} | {str(g[5] or '-'):<19} | {g[6]:<14}  | {g[8]:<15} | {g[9]:<12} | {g[7] or '-'}")

    print("\n=== Standorte ===")
    datenbank.cursor.execute("""SELECT * FROM Standort""")
    standortAnzeige = datenbank.cursor.fetchall()

    if standortAnzeige:
        print(f"{'Kürzel':<10} | {'Räume':<8} | {'Adresse':<25} | {'Stadt':<18} | {'Postleitzahl':<14}")
    print("-" * 85)
    for j in standortAnzeige:
        print(f"{j[0]:<10} | {j[1]:<8} | {j[2]:<25} | {j[3]:<18} | {j[4]:<14}")