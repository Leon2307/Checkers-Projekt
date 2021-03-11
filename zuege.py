import pygame
import gui
import feld as f
import main
import sys

letzteMarkiert = None
letzteNachbarn = []

dZügePlayer = [[-1, 1], [-1, -1]]
dZügeComputer = [[1, -1], [1, 1]]
dZügeDame = [[-1, 1], [-1, -1], [1, -1], [1, 1]]

zwangZüge = []
anfangsX = 0
anfangsY = 0


# Berechnet für jedes Feld die möglichen Züge
def moeglicheZuege(feld, spieler):
    for y in range(len(feld)):
        for x in range(len(feld)):
            feld[y][x].zügeBerechnen(feld, spieler, y, x)


# Überprüft wie viele Steine noch drin sind und ob gewonnen wurde
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


# Lösche Item von Liste
def deleteFromList(list, item):

    for index, i in enumerate(list):
        if i == item:
            list.pop(index)

    return list


# Überprüft ob in einer Liste mit Zügen mehrere mit dem gleichen Zielfeld sind und pickt den besseren
def pickeBeste(zuege):
    for i, zug1 in enumerate(zuege.copy()):
        for j, zug2 in enumerate(zuege.copy()):

            # Auf gleiches Zielfeld überprüfen
            if zug1[0] == zug2[0] and not zug1 == zug2:

                # Überprüfen welcher Zug mehr Steine rauswirft
                if len(zug1[1]) > len(zug2[1]):
                    zuege = deleteFromList(zuege, zug2)
                elif len(zug1[1]) < len(zug2[1]):
                    zuege = deleteFromList(zuege, zug1)
                else:
                    zuege = deleteFromList(zuege, zug1)

    return zuege


def zugzwang(feld, spieler, y, x, eckfelder, rausgeworfen, durchgang):
    global zwangZüge, anfangsX, anfangsY

    # Wenn der Durchgang 0 (1. Mal) ist wird alles auf Ausgangswert gesetzt
    if durchgang == 0:
        zwangZüge = []
        eckfelder = []
        rausgeworfen = []
        anfangsX = x
        anfangsY = y

    elif durchgang > 7:
        return False

    deltaZüge = dZügePlayer if spieler else dZügeComputer
    zuegeMoeglich = False
    moeglich = False

    # Alle Möglichkeiten durchgehen
    for j, i in deltaZüge:
        j2 = j*2
        i2 = i*2

        if durchgang != 0:
            eckfelderSave = eckfelder.copy()
            rausgeworfenSave = rausgeworfen.copy()
        else:
            eckfelderSave = []
            rausgeworfenSave = []

        # Auf Existenz prüfen
        if y+j < 0 or y+j > 7 or x+i < 0 or x+i > 7:
            continue

        # Auf leere des nächsten Feldes prüfen
        if not feld[y+j][x+i].isPlayer() and not feld[y+j][x+i].isComputer() and durchgang == 0:

            # Nächstes Feld als moeglicher Zug hinzufügen
            zwangZüge.append(
                (feld[y+j][x+i], (None, None), [None]))
            # continue

        # Auf Existenz prüfen
        if y+j2 < 0 or y+j2 > 7 or x+i2 < 0 or x+i2 > 7:
            continue

        # Auf Gegner prüfen und leere des dahinter liegenden Feldes
        if (feld[y+j][x+i].isComputer() and spieler or feld[y+j][x+i].isPlayer() and not spieler) and not feld[y+j2][x+i2].isPlayer() and not feld[y+j2][x+i2].isComputer():

            zuegeMoeglich = True
            neuesFeld = feld[y+j2][x+i2]
            rausgeworfenSave.append(feld[y+j][x+i])
            eckfelderSave.append(feld[y][x])

            # Versuchen noch einen Zug weiter zu gehen
            moeglich = zugzwang(feld, spieler, y+j2, x+i2,
                                eckfelderSave, rausgeworfenSave, durchgang+1)

            # Falls nicht weiter gegangen werden konnte aktuelles Feld hinzufügen
            if not moeglich:
                zwangZüge.append(
                    (neuesFeld, rausgeworfenSave.copy(), eckfelderSave.copy()))
                rausgeworfenSave.pop()
                eckfelderSave.pop()

    if durchgang == 0:
        return pickeBeste(zwangZüge)
    else:
        return zuegeMoeglich


# Checkt ob Der nächste Zug auf ein mögliches/neues Feld geht
def bereitsWeg(neuesY, neuesX, eckfelder):

    # Checkt ob Startfeld
    if neuesY == anfangsY and neuesX == anfangsX:
        return False

    # Checkt ob bereits abgegangen(eckfeld)
    for eFeld in eckfelder.copy():
        if eFeld.getPosition() == (neuesX, neuesY):
            return False

    # Checkt ob es bereits ein belegtes Feld ist
    for zug in zwangZüge.copy():
        if zug[0].getPosition() == (neuesY, neuesX) and zug[2] == [None]:
            return False

    # Ansonsten True
    return True


def zugzwangDame(y, x, spieler, feld, eckfelder, rausgeworfen, durchgang, dZügeDameHergekommen):
    global zwangZüge, anfangsX, anfangsY, dZügeDame, dZügeDame2

    dZügeDameNeu = dZügeDame.copy()
    if dZügeDameHergekommen != None:
        for ind, dzug in enumerate(dZügeDameNeu):
            if dzug == dZügeDameHergekommen:
                del dZügeDameNeu[ind]

    # Wenn der Durchgang 0 (1. Mal) ist wird alles auf Ausgangswert gesetzt
    if durchgang == 0:
        zwangZüge = []
        eckfelder = []
        rausgeworfen = []
        anfangsX = x
        anfangsY = y

    elif durchgang > 7:
        return False

    zuegeMoeglich = False
    moeglich = False

    # Alle Möglichkeiten durchgehen
    for j, i in dZügeDameNeu:

        speicherJ = j
        speicherI = i
        while y+j < 8 and y+j >= 0 and x+i < 8 and x+i >= 0:

            # Auf leere des Feldes prüfen
            # Abbrechen wenn eigener Stein auf nächstem Feld
            if (feld[y+j][x+i].isPlayer() and spieler) or (feld[y+j][x+i].isComputer() and not spieler):
                break

            # Wenn frei ist und Durchgang 0
            elif not feld[y+j][x+i].isPlayer() and not feld[y+j][x+i].isComputer() and durchgang == 0:
                zwangZüge.append(
                    (feld[y+j][x+i], (None, None), [None]))

            # Wenn ein Gegner auf dem nächsten Feld ist
            elif feld[y+j][x+i].isComputer() and spieler or feld[y+j][x+i].isPlayer() and not spieler:

                # Auf Existenz prüfen
                if not(y+j+speicherJ < 8 and y+j+speicherJ >= 0 and x+i+speicherI < 8 and x+i+speicherI >= 0):
                    break

                # Wenn das Feld besetzt ist prüfen ob das darauf Folgende frei ist
                if not feld[y+j+speicherJ][x+i+speicherI].isComputer() and not feld[y+j+speicherJ][x+i+speicherI].isPlayer():

                    # Felder hinzufügen
                    zuegeMoeglich = True
                    neuesFeld = feld[y+j+speicherJ][x+i+speicherI]
                    rausgeworfen.append(feld[y+j][x+i])
                    eckfelder.append(feld[y][x])

                    # Wenn die neue Position nicht möglich ist, da bereits abgegangen
                    if bereitsWeg(y+j+speicherJ, x+i+speicherI, eckfelder.copy()):
                        moeglich = zugzwangDame(y+j+speicherJ, x+i+speicherI, spieler, feld,
                                                eckfelder, rausgeworfen, durchgang+1, [-speicherJ, -speicherI])

                    # Falls nicht weiter gegangen werden konnte aktuelles Feld hinzufügen
                    if not moeglich:

                        zwangZüge.append(
                            (neuesFeld, rausgeworfen.copy(), eckfelder.copy()))

                    rausgeworfen.pop()
                    eckfelder.pop()
                    moeglich = False

                break

            # j und i erhöhen
            j = j+speicherJ
            i = i+speicherI

    if durchgang == 0:
        return pickeBeste(zwangZüge)
    else:
        return zuegeMoeglich


def zugAusführen(feld, spieler, y, x, h):
    global letzteMarkiert, letzteNachbarn
    nachbarIndex = None

    # Prüfen ob das Feld existiert
    if y < 0 or y > len(feld)-1 or x < 0 or x > len(feld)-1:
        return

    # Geklicktes Feld markieren
    if (spieler and feld[y][x].isPlayer() or not spieler and feld[y][x].isComputer()) and len(feld[y][x].getZüge()) > 0:

        # Das zuletzt markierte Feld leeren
        if letzteMarkiert != None:
            letzteMarkiert.makeClicked(False)
            for n in letzteNachbarn:
                n.makeMoeglicherZug(False)
            letzteNachbarn = []

        # Neues geklicktes Feld zum aktuellen Spieler machen
        letzteMarkiert = feld[y][x]
        feld[y][x].makeClicked(True)

        # mögliche Züge markieren
        for zug in feld[y][x].getZüge():

            zug[0].makeMoeglicherZug(True)
            letzteNachbarn.append(zug[0])

    # Ist Geklicktes Feld Nachbar?
    elif feld[y][x].isMoeglicherZug():

        # Das zuletzt markierte Feld leeren
        letzteMarkiert.makePlayer(False)
        letzteMarkiert.makeComputer(False)
        letzteMarkiert.makeClicked(False)

        # Neus Feld zuweisen
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
            if n == feld[y][x]:
                nachbarIndex = i
            n.makeMoeglicherZug(False)
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


# Prüft ob durch Zug eine Dame entsteht
def checkDame(aktuellesFeld, y, spieler):
    if spieler and y == 0 or not spieler and y == 7:
        aktuellesFeld.makeDame(True)


# Der Spieler ist an der Reihe
def spielerZug(feld, feldgroesse, h):
    gui.mausGedrueckt(feld, feldgroesse, True, h)

# Der Computer ist an der Reihe


def computerZug(feld, feldgroesse, h):
    gui.mausGedrueckt(feld, feldgroesse, False, h)
