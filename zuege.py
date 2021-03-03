import pygame
import gui

letzteMarkiert = None
letzteNachbarn = []

dZügePlayer = [[-1, 1], [-1, -1]]
dZügeComputer = [[1, -1], [1, 1]]
dZügeDame = [[-1, 1], [-1, -1], [1, -1], [1, 1]]


def moeglicheZuege(feld, spieler):
    for y in range(len(feld)):
        for x in range(len(feld)):
            feld[y][x].zügeBerechnen(feld, spieler, y, x)


def zugzwang(feld, spieler, y, x, übersprungenerStein, isDame):

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
                        (feld[y+j2][x+i2], (feld[y+j][x+i], übersprungenerStein)))

    else:

        # Alle Möglichkeiten durchgehen
        for j, i in dZügeDame:
            speicherJ = j
            speicherI = i
            print('test')
            while y+j < 8 and y+j >= 0 and x+i < 8 and x+i >= 0:
                # Auf leere des Feldes prüfen
                if feld[y+j][x+i].isPlayer() and spieler or feld[y+j][x+i].isComputer() and not spieler:
                    break
                elif feld[y+j][x+i].isComputer() and spieler or feld[y+j][x+i].isPlayer() and not spieler:
                    print('hier')
                    # Wenn das Feld besetzt ist prüfen ob das darauf Folgende frei ist
                    if not(y+j+speicherJ < 8 and y+j+speicherJ >= 0 and x+i+speicherI < 8 and x+i+speicherI >= 0):
                        break
                    if not feld[y+j+speicherJ][x+i+speicherI].isComputer() and not feld[y+j+speicherJ][x+i+speicherI].isPlayer():
                        print('hallo')
                        zwangZüge.append(
                            (feld[y+j+speicherJ][x+i+speicherI], (feld[y+j][x+i], übersprungenerStein)))
                    break

                # j und i erhöhen
                j = j+speicherJ
                i = i+speicherI

    return zwangZüge


def zugAusführen(feld, spieler, y, x, h):
    global letzteMarkiert, letzteNachbarn
    nachbarIndex = None

    # Geklicktes Feld markieren
    if (
        spieler and feld[y][x].isPlayer(
        ) or not spieler and feld[y][x].isComputer()
    ) and len(feld[y][x].getZüge()) > 0:
        if letzteMarkiert != None:
            letzteMarkiert.makeClicked(False)
            for n in letzteNachbarn:
                n[0].makeNachbar(False)
            letzteNachbarn = []
        letzteMarkiert = feld[y][x]
        feld[y][x].makeClicked(True)

        # Nachbarn markieren
        for zug in feld[y][x].getZüge():
            zug[0].makeNachbar(True)
            letzteNachbarn.append(zug)

    # Ist Geklicktes Feld Nachbar?
    elif feld[y][x].isNachbar():
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
            n[0].makeNachbar(False)
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
