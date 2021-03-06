import pygame
import gui
import feld as f
import main

letzteMarkiert = None
letzteNachbarn = []

dZügePlayer = [[-1, 1], [-1, -1]]
dZügeComputer = [[1, -1], [1, 1]]
dZügeDame = [[-1, 1], [-1, -1], [1, -1], [1, 1]]
dZügeDame = [[1, -1], [1, 1], [-1, 1], [-1, -1]]
# Invertiert um beim löschen der gekommenen Richtung die Entgegengesetzte zu entfernen


def moeglicheZuege(feld, spieler):
    for y in range(len(feld)):
        for x in range(len(feld)):
            feld[y][x].zügeBerechnen(feld, spieler, y, x)


def spielStand(feld, spieler):

    # verbliebene Steine auf dem Spielfeld
    anzahlSpieler = 0
    anzahlComputer = 0

    # verbliebene Züge auf dem Spielfeld
    übrigeZügeSpieler = []
    übrigeZügeComputer = []

    for y in range(len(feld)):
        for x in range(len(feld)):

            # Anzahl checken
            if feld[y][x].isPlayer():
                anzahlSpieler += 1
                if feld[y][x].getZüge() != []:
                    übrigeZügeSpieler.append(feld[y][x].getZüge())
            elif feld[y][x].isComputer():
                anzahlComputer += 1
                if feld[y][x].getZüge() != []:
                    übrigeZügeComputer.append(feld[y][x].getZüge())

    # return Sieger, computerSteine, spielerSteine
    # Spieler hat gewonnen
    if übrigeZügeComputer == [] and not spieler or anzahlComputer < 1:
        return True, anzahlComputer, anzahlSpieler

    # Computer hat gewonnen
    elif übrigeZügeSpieler == [] and spieler or anzahlSpieler < 1:
        return False, anzahlComputer, anzahlSpieler

    # Keiner hat gewonnen
    else:
        return None, anzahlComputer, anzahlSpieler


def zugzwang(feld, spieler, y, x, übersprungenerStein, isDame, dZügeDameHergekommen):

    zwangZüge = []

    if not isDame:
        deltaZüge = dZügePlayer if spieler else dZügeComputer

        # Alle Möglichkeiten durchgehen
        for j, i in deltaZüge:
            j2 = j*2
            i2 = i*2

            # Auf Gegner prüfen und leere des dahinter liegenden Feldes
            if not(y+j2 < 0 or y+j2 > 7 or x+i2 < 0 or x+i2 > 7):
                if (feld[y+j][x+i].isComputer() and spieler or feld[y+j][x+i].isPlayer() and not spieler) and not feld[y+j2][x+i2].isPlayer() and not feld[y+j2][x+i2].isComputer():
                    zwangZüge.append(
                        (feld[y+j2][x+i2], (feld[y+j][x+i], übersprungenerStein), feld[y][x]))

    else:

        dZügeDameNeu = dZügeDame.copy()
        del dZügeDameNeu[dZügeDameHergekommen]

        # Alle Möglichkeiten durchgehen
        for j, i in dZügeDameNeu:

            speicherJ = j
            speicherI = i
            while y+j < 8 and y+j >= 0 and x+i < 8 and x+i >= 0:

                # Auf leere des Feldes prüfen
                # Abbrechen wenn eigener Stein auf nächstem Feld
                if (feld[y+j][x+i].isPlayer() and spieler) or (feld[y+j][x+i].isComputer() and not spieler):
                    break

                # Wenn ein Gegner auf dem nächsten Feld ist
                elif feld[y+j][x+i].isComputer() and spieler or feld[y+j][x+i].isPlayer() and not spieler:

                    # Auf Existenz prüfen
                    if not(y+j+speicherJ < 8 and y+j+speicherJ >= 0 and x+i+speicherI < 8 and x+i+speicherI >= 0):
                        break

                    # Wenn das Feld besetzt ist prüfen ob das darauf Folgende frei ist
                    if not feld[y+j+speicherJ][x+i+speicherI].isComputer() and not feld[y+j+speicherJ][x+i+speicherI].isPlayer():

                        # Felder hinzufügen
                        zwangZüge.append(
                            (feld[y+j+speicherJ][x+i+speicherI], (feld[y+j][x+i], übersprungenerStein), feld[y][x]))
                    break

                # j und i erhöhen
                j = j+speicherJ
                i = i+speicherI

    return zwangZüge


def zugAusführen(feld, spieler, y, x, h):
    global letzteMarkiert, letzteNachbarn
    nachbarIndex = None

    # Prüfen ob das Feld existiert
    if y < 0 or y > len(feld)-1 or x < 0 or x > len(feld)-1:
        return
    # Geklicktes Feld markieren
    if (
        spieler and feld[y][x].isPlayer(
        ) or not spieler and feld[y][x].isComputer()
    ) and len(feld[y][x].getZüge()) > 0:
        if letzteMarkiert != None:
            letzteMarkiert.makeClicked(False)
            for n in letzteNachbarn:
                n[0].makeMoeglicherZug(False)
            letzteNachbarn = []
        letzteMarkiert = feld[y][x]
        feld[y][x].makeClicked(True)

        # Nachbarn markieren
        for zug in feld[y][x].getZüge():
            zug[0].makeMoeglicherZug(True)
            letzteNachbarn.append(zug)

    # Ist Geklicktes Feld Nachbar?
    elif feld[y][x].isMoeglicherZug():
        letzteMarkiert.makePlayer(False)
        letzteMarkiert.makeComputer(False)
        letzteMarkiert.makeClicked(False)
        feld[y][x].makePlayer(
            True) if spieler else feld[y][x].makeComputer(True)
        if letzteMarkiert.isDame():
            feld[y][x].makeDame(True)
        letzteMarkiert.makeDame(False)

        # Prüfen ob eine Dame entsteht
        checkDame(feld[y][x], y, spieler)

        # Nachbarn zurücksetzen und index des geklickten Nachbarn ermitteln
        i = 0
        for n in letzteNachbarn:
            if n[0] == feld[y][x]:
                nachbarIndex = i
            n[0].makeMoeglicherZug(False)
            i += 1
        h.wechselSpieler()

        # rauswerfen
        if letzteMarkiert.getZüge()[nachbarIndex][1] != None:
            for letzteZüge in letzteMarkiert.getZüge()[nachbarIndex][1]:
                if letzteZüge != None:
                    letzteZüge.makePlayer(False)
                    letzteZüge.makeComputer(False)
                    letzteZüge.makeDame(False)

        letzteMarkiert = None
        letzteNachbarn = []


def checkDame(aktuellesFeld, y, spieler):
    if spieler and y == 0 or not spieler and y == 7:
        aktuellesFeld.makeDame(True)


def spielerZug(feld, feldgroesse, h):
    gui.mausGedrueckt(feld, feldgroesse, True, h)


def computerZug(feld, feldgroesse, h):
    gui.mausGedrueckt(feld, feldgroesse, False, h)
