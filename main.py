from zuege import ausfuehren
import feld
import gui.events as evnt
import gui.draw as draw
import zuege.berechnen as zuege
import zuege.minimax as mm
from time import sleep

class Hauptklasse:

    feld = []
    SPIELFELDGROESSE = 8
    moegZuege = None
    bereitsBerechnet = False

    def __init__(self):
        self.momSpieler = True  # Momentaner Spieler => spieler = True; computer = False

    # Erzeugen des Ausgangszustandes des Spielfeldes
    def startFeld(self):
        spielfeld = []
        for y in range(self.SPIELFELDGROESSE):
            spielfeld.append([])
            for x in range(self.SPIELFELDGROESSE):
                spielfeld[y].append(feld.Feld(y, x))

                # Farbe des Feldes
                if (y + x) % 2 == 0:
                    spielfeld[y][x].makeBlack(True)

                    # Steine belegung
                    if y < 3:
                        spielfeld[y][x].makeComputer(True)
                    elif y > 4:
                        spielfeld[y][x].makePlayer(True)
                else:
                    spielfeld[y][x].makeWhite(True)

        return spielfeld

    # aktuellen Spieler wechseln
    def wechselSpieler(self):
        self.momSpieler = not self.momSpieler

    # Feld zuruecksetzen
    def resetFeld(self):
        self.feld = self.startFeld()
        self.momSpieler = True

    # bereitsBerechnet zuruecksetzen
    def resetBereitsBerechnet(self):
        self.bereitsBerechnet = False

    # Hauptklasse
    def main(self, h):
        self.feld = self.startFeld()

        gewonnen = False

        # Dauerschleife
        while True:

            # Solange das Spiel läuft
            while not gewonnen:
                zuege.moeglicheZuege(self.feld, self.momSpieler)
                if self.momSpieler:
                    evnt.mausGedrueckt(self.feld, self.SPIELFELDGROESSE, True, h)
                else:
                    #evnt.mausGedrueckt(self.feld, self.SPIELFELDGROESSE, False, h)
                    if not self.bereitsBerechnet:
                        besterZug = mm.minimax(
                            self.feld, False)[1]
                        self.bereitsBerechnet = True
                        besterZug[3].makeClicked(True)
                        ausfuehren.setLetzteMarkiert(besterZug[3])
                        besterZug[0].makeMoeglicherZug(True)
                        ausfuehren.setLetzteNachbarn([besterZug[0]])
                        continue
                    else:
                        zuege.setzeBestenZug(self.feld, besterZug)
                        evnt.mausGedrueckt(self.feld, self.SPIELFELDGROESSE, False, h)

                draw.draw(self.feld, self.SPIELFELDGROESSE, self.momSpieler)

            # Wenn das Spiel beendet ist
            while gewonnen:
                return


if __name__ == "__main__":
    h = Hauptklasse()
    h.main(h)
