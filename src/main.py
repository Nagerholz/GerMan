#  ██████╗ ███████╗██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
# ██╔════╝ ██╔════╝██╔══██╗████╗ ████║██╔══██╗████╗  ██║
# ██║  ███╗█████╗  ██████╔╝██╔████╔██║███████║██╔██╗ ██║
# ██║   ██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══██║██║╚██╗██║
# ╚██████╔╝███████╗██║  ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║
#  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
                                                      
# INTERNE IMPORTE
from befehle import befehle
from anzeige import anzeige
from logik import logik

GerManStr = """ ██████╗ ███████╗██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
██╔════╝ ██╔════╝██╔══██╗████╗ ████║██╔══██╗████╗  ██║
██║  ███╗█████╗  ██████╔╝██╔████╔██║███████║██╔██╗ ██║
██║   ██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══██║██║╚██╗██║
╚██████╔╝███████╗██║  ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║
 ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝"""



# DER PROGRAMMCODE STARET HIER
if __name__ == "__main__":
    while True:
        print(f"{anzeige.LEEREN}{26*"- "}-\n{anzeige.farbe.GRUEN}{GerManStr}{anzeige.farbe.RESET}\n- - - - - - von Adrian, Eliano und Daniel - - - - - -")


        print("\nWählen Sie eine Funktion.")
        eingabe = input("1 - Hinzufügen\n2 - Anzeigen\n3 - Suchen\n4 - Bearbeiten\n5 - Löschen\n6 - Beenden\n--- Ihre Wahl ---\n").strip()

        match eingabe:
            case "1":
                befehle.hinzufuegen.hinzufugen()
            case "2":
                befehle.anzeigen.anzeigen()
            case "3":
                befehle.suchen.suchen()
            case "4":
                befehle.bearbeiten.bearbeiten()
            case "5":
                befehle.loeschen.loeschen()
            case "6":
                break
            case _:
                input("Ungültige Eingabe!")

            
        input("\nZurück zum Menü\n")
print("GerMan beendet...")