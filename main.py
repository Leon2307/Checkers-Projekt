from zuege import ausfuehren
import feld
import gui.events as evnt
import gui.draw as draw
import zuege.berechnen as zuege
import zuege.minimax as mm
from time import sleep

class Hauptklasse:

    feld = []
    gewonnen = False
    SPIELFELDGROESSE = 8
    moegZuege = None
    bereitsBerechnet = False
    miniMaxOnBlau = False
    miniMaxOnGruen = False
    besterZug = None

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
        self.gewonnen = False
        self.bereitsBerechnet = False
        self.momSpieler = True

    # bereitsBerechnet zuruecksetzen
    def resetBereitsBerechnet(self):
        self.bereitsBerechnet = False

    # Zwischen Minimax und Manuell wechseln
    def wechselMiniMaxOnBlau(self):
        if self.miniMaxOnBlau and self.besterZug != None:
            self.besterZug[3].makeClicked(False)
            self.besterZug[0].makeMoeglicherZug(False)
        self.miniMaxOnBlau = not self.miniMaxOnBlau
    
    def getMiniMaxOnBlau(self):
        return self.miniMaxOnBlau
    
    def wechselMiniMaxOnGruen(self):
        if self.miniMaxOnGruen and self.besterZug != None:
            self.besterZug[3].makeClicked(False)
            self.besterZug[0].makeMoeglicherZug(False)
        self.miniMaxOnGruen = not self.miniMaxOnGruen
    
    def getMiniMaxOnGruen(self):
        return self.miniMaxOnGruen

    # Hauptklasse
    def main(self, h):
        
        # Startfeld erzeugen
        self.feld = self.startFeld()

        # Dauerschleife
        while True:

            # Alle moeglichen Zuege fuer den aktuellen Spieler berechnen
            zuege.moeglicheZuege(self.feld, self.momSpieler)

            # Manuell ziehen
            if not self.miniMaxOnBlau and not self.momSpieler or not self.miniMaxOnGruen and self.momSpieler:
                evnt.mausGedrueckt(self.feld, self.SPIELFELDGROESSE, self.momSpieler, h)

            # Minimax
            else:

                # Gezeichnete Punkte und Wege rückgängig machen
                letzteMarkiert = ausfuehren.getLetzteMarkiert()
                if letzteMarkiert != None:
                    letzteMarkiert.makeClicked(False)
                for nachbar in ausfuehren.getLetzteNachbarn():
                    nachbar.makeMoeglicherZug(False)
                
                # Berechnet den besten Zug
                if not self.bereitsBerechnet:
                    self.besterZug = mm.minimax(
                        self.feld, self.momSpieler)[1]
                    self.bereitsBerechnet = True
                    continue
                
                # Setzt den besten Zug
                else:
                    self.besterZug[3].makeClicked(True)
                    ausfuehren.setLetzteMarkiert(self.besterZug[3])
                    self.besterZug[0].makeMoeglicherZug(True)
                    ausfuehren.setLetzteNachbarn([self.besterZug[0]])
                    zuege.setzeBestenZug(self.feld, self.besterZug)
                    evnt.mausGedrueckt(self.feld, self.SPIELFELDGROESSE, self.momSpieler, h)

            draw.draw(self.feld, self.SPIELFELDGROESSE, self.momSpieler, h)


if __name__ == "__main__":
    h = Hauptklasse()
    h.main(h)
