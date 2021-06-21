from zuege import ausfuehren
import feld
import gui.events as evnt
import gui.draw as draw
import zuege.berechnen as zuege
import zuege.minimax as mm
import copy


class Hauptklasse:

    feld = []
    SPIELFELDGROESSE = 8
    moegZuege = None
    bereitsBerechnet = False
    miniMaxOnBlau = False
    miniMaxOnGruen = False
    besterZug = None
    startspieler = True
    vorherigeZuege = []

    def __init__(self):
        self.momSpieler = True  # Momentaner Spieler => gruen = True; blau = False

    # Erzeugen des Ausgangszustandes des Spielfeldes
    def startFeld(self):

        spielfeld = []

        # Fuer jedes Feld ein Objekt von feld erstellen
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

    # Einen Zug zurueck gehen
    def zugZurueck(self):

        # Neues Feld = letztes gespeichertes Feld
        if self.vorherigeZuege != []:
            self.feld = self.vorherigeZuege[-1]
            self.vorherigeZuege.pop()
            self.momSpieler = not self.momSpieler
            self.bereitsBerechnet = False
            self.miniMaxOnBlau = False
            self.miniMaxOnGruen = False

    # Zug zu vorherigen Zuegen hinzufuegen
    def addZugZurueck(self):

        altesFeld = copy.deepcopy(self.feld)

        # Alle felder entmarkieren um Grafikfehler zu vermeiden
        for y in range(self.SPIELFELDGROESSE):
            for x in range(self.SPIELFELDGROESSE):

                altesFeld[y][x].makeClicked(False)
                altesFeld[y][x].makeMoeglicherZug(False)

        self.vorherigeZuege.append(altesFeld)

    # aktuellen Spieler wechseln
    def wechselSpieler(self):

        self.momSpieler = not self.momSpieler

    # Feld zuruecksetzen
    def resetFeld(self):

        self.feld = self.startFeld()
        self.gewonnen = False
        self.bereitsBerechnet = False
        self.startspieler = not self.startspieler
        self.momSpieler = self.startspieler
        self.vorherigeZuege = []

    # bereitsBerechnet zuruecksetzen
    def resetBereitsBerechnet(self):
        self.bereitsBerechnet = False

    # Zwischen Minimax und Manuell wechseln Blau
    def wechselMiniMaxOnBlau(self):

        # Checken ob bereits ein bester Zug ermittelt wurde und ggf. entfernen
        if self.miniMaxOnBlau and self.besterZug != None:
            self.besterZug[3].makeClicked(False)
            self.besterZug[0].makeMoeglicherZug(False)

        self.miniMaxOnBlau = not self.miniMaxOnBlau

    # Stand des Buttons aufrufen
    def getMiniMaxOnBlau(self):
        return self.miniMaxOnBlau

    # Zwischen Minimax und Manuell wechseln Gruen
    def wechselMiniMaxOnGruen(self):

        # Checken ob bereits ein bester Zug ermittelt wurde und ggf. entfernen
        if self.miniMaxOnGruen and self.besterZug != None:
            self.besterZug[3].makeClicked(False)
            self.besterZug[0].makeMoeglicherZug(False)

        self.miniMaxOnGruen = not self.miniMaxOnGruen

    # Stand des Buttons aufrufen
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
                evnt.mausGedrueckt(
                    self.feld, self.SPIELFELDGROESSE, self.momSpieler, h)

            # Minimax
            else:

                # Gezeichnete Punkte und Wege rueckgängig machen
                letzteMarkiert = ausfuehren.getLetzteMarkiert()

                if letzteMarkiert != None:
                    letzteMarkiert.makeClicked(False)

                for nachbar in ausfuehren.getLetzteNachbarn():
                    nachbar.makeMoeglicherZug(False)

                # Berechnet den besten Zug
                if not self.bereitsBerechnet:
                    self.besteBewertung, self.besterZug = mm.minimax(
                        self.feld, self.momSpieler)
                    self.bereitsBerechnet = True
                    continue

                # Setzt den besten Zug
                else:

                    # Wenn bereits ein bester Zug berechnet wurde diesen anzeigen
                    if self.besterZug != None:
                        self.besterZug[3].makeClicked(True)
                        ausfuehren.setLetzteMarkiert(self.besterZug[3])
                        self.besterZug[0].makeMoeglicherZug(True)
                        ausfuehren.setLetzteNachbarn([self.besterZug[0]])
                        zuege.setzeBestenZug(self.feld, self.besterZug)
                    evnt.mausGedrueckt(
                        self.feld, self.SPIELFELDGROESSE, self.momSpieler, h)

            # Das aktuelle Spielfeld zeichnen
            draw.draw(self.feld, self.SPIELFELDGROESSE, self.momSpieler, h)


if __name__ == "__main__":
    h = Hauptklasse()
    h.main(h)
