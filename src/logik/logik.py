import re

# Liste bekannter Gerätetypen
kategorien = {"1":"Switch", "2":"Router", "3":"AP", "4":"Firewall", "5":"Server", "6":"PC", "7":"Drucker"}

def setzeKategorie():
    while True:
        for key, val in kategorien.items():
            print(f"  {key} - {val}")
        wert = input("\nGebe Sie die Gerätekategorie an: ").strip()
        if wert.strip() in kategorien:
            return kategorien[wert.strip()]
        
        print("Ungültige Eingabe!")


# Pflichgelder Methode

def pflichtfeld(pflichteingabe):
    while True:
        wert = input(pflichteingabe).strip()
        if wert:
            return wert
        print("Dieses Feld ist Pflicht, bitte ausfüllen!")

# Reguläre Eingabe Methoden

def ipEingabe(eingabe):
    # Akzeptiert DDD.DDD.DDD.DDD
    muster = r"^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$"
    while True:
        wert = input(eingabe).strip()
        if re.match(muster, wert):
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
    # Bekannte Status (dict)
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