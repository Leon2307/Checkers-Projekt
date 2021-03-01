import feld
import gui
import zuege

SPIELFELDGROESSE = 8

def startFeld():
    spielfeld = []
    for y in range(SPIELFELDGROESSE):
        spielfeld.append([])
        for x in range(SPIELFELDGROESSE):
            spielfeld[y].append(feld.Feld())

            #Farbe des Feldes
            if (y + x) % 2 == 0:
                spielfeld[y][x].makeBlack(True)

                #Steine belegung
                if y < 3:
                    spielfeld[y][x].makeComputer(True)
                elif y > 4:
                    spielfeld[y][x].makePlayer(True)
            else:
                spielfeld[y][x].makeWhite(True)

    return spielfeld

def wechselSpieler(alterSpieler):
    return not alterSpieler

def main():
    feld = startFeld()

    gewonnen = False
    momSpieler = True #Momentaner Spieler => spieler = True; computer = False

    #Dauerschleife
    while True:

        #Solange das Spiel läuft
        while not gewonnen:
            if momSpieler:
                zuege.moeglicheZuege(feld, momSpieler)
                zuege.spielerZug(feld,SPIELFELDGROESSE)
            else:
                zuege.computerZug(feld)

            gui.draw(feld, SPIELFELDGROESSE)

        #Wenn das Spiel beendet ist
        while gewonnen:
            return

if __name__ == "__main__":
    main()