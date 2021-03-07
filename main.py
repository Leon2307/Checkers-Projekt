import feld
import gui
import zuege


class Hauptklasse:

    SPIELFELDGROESSE = 8
    # momSpieler = True #Momentaner Spieler => spieler = True; computer = False

    def __init__(self):
        self.momSpieler = True  # Momentaner Spieler => spieler = True; computer = False

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

    def testFeld(self):
        spielfeld = []
        for y in range(self.SPIELFELDGROESSE):
            spielfeld.append([])
            for x in range(self.SPIELFELDGROESSE):
                spielfeld[y].append(feld.Feld(y, x))

                # Farbe des Feldes
                if (y + x) % 2 == 0:
                    spielfeld[y][x].makeBlack(True)

                    # Steine belegung
                    if y < 1:
                        spielfeld[y][x].makeComputer(True)
                    elif y > 4:
                        spielfeld[y][x].makePlayer(True)
                else:
                    spielfeld[y][x].makeWhite(True)

        return spielfeld

    def wechselSpieler(self):
        self.momSpieler = not self.momSpieler

    def main(self, h):
        feld = self.startFeld()
        # feld[5][5].makeDame(True)

        gewonnen = False

        # Dauerschleife
        while True:

            # Solange das Spiel läuft
            while not gewonnen:
                zuege.moeglicheZuege(feld, self.momSpieler)
                if self.momSpieler:
                    zuege.spielerZug(feld, self.SPIELFELDGROESSE, h)
                else:
                    zuege.computerZug(feld, self.SPIELFELDGROESSE, h)

                gui.draw(feld, self.SPIELFELDGROESSE, self.momSpieler)

            # Wenn das Spiel beendet ist
            while gewonnen:
                return


if __name__ == "__main__":
    h = Hauptklasse()
    h.main(h)
