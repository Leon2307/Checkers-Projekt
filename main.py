import feld
import gui.events as evnt
import gui.draw as draw
import zuege.berechnen as zuege


class Hauptklasse:

    feld = []
    SPIELFELDGROESSE = 8

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

    # Feld zurücksetzen
    def resetFeld(self):
        self.feld = self.startFeld()
        self.momSpieler = True

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
                    evnt.mausGedrueckt(self.feld, self.SPIELFELDGROESSE, False, h)

                draw.draw(self.feld, self.SPIELFELDGROESSE, self.momSpieler)

            # Wenn das Spiel beendet ist
            while gewonnen:
                return


if __name__ == "__main__":
    h = Hauptklasse()
    h.main(h)
