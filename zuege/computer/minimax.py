from zuege import spielstand, berechnen
from zuege.computer import ausfuehrenComputer as ausComp
import copy


speicherFeld = []


# Minimax
def minimax(feld, tiefe, spieler):

    if tiefe == 5:
        speicherFeld = copy.deepcopy(feld)

    if tiefe == 0:
        return zugBewerten(feld, speicherFeld, spieler), None

    sieger = spielstand.spielStand(feld, spieler)[0]
    if sieger != None:
        return (-99999 if sieger else 99999), None

    if spieler:
        bestesErgebnis = float('inf')
        besterZug = None
        for i, zug in enumerate(zuglisteGenerieren(feld, True)):
            feldKopie = copy.deepcopy(feld)
            ausComp.ziehen(feldKopie, zug, spieler)
            bewertung, _ = minimax(feldKopie, tiefe-1, False)[0]
            #ausComp.ziehenZurueck(feld, zugKopie, spieler)
            bestesErgebnis = min(bewertung, bestesErgebnis)
            if bestesErgebnis == bewertung:
                besterZug = zug

        return bestesErgebnis, besterZug

    else:
        bestesErgebnis = float('-inf')
        besterZug = None
        for i, zug in enumerate(zuglisteGenerieren(feld, False)):
            feldKopie = copy.deepcopy(feld)
            ausComp.ziehen(feldKopie, zug, spieler)
            bewertung = minimax(feldKopie, tiefe-1, True)[0]
            #feld = copy.deepcopy(feldKopie)
            #ausComp.ziehenZurueck(feld, zugKopie, spieler)
            bestesErgebnis = max(bewertung, bestesErgebnis)
            if bestesErgebnis == bewertung:
                besterZug = i

        return bestesErgebnis, besterZug


# Liste mit möglichen Zuegen generieren
def zuglisteGenerieren(feld, spieler):

    berechnen.moeglicheZuege(feld, spieler)

    alleZuege = []

    for y in range(8):
        for x in range(8):

            if feld[y][x].isPlayer() and spieler:
                for zug in feld[y][x].getZuege():
                    alleZuege.append(zug)

            elif feld[y][x].isComputer() and not spieler:
                for zug in feld[y][x].getZuege():
                    alleZuege.append(zug)

    return alleZuege


# Bewertungsfunktion um Zug zu Bewerten
def zugBewerten(neuesFeld, altesFeld, spieler):

    # Gewichtung
    rauswurf = 2
    dame = 4

    # Damen muessen noch berechnet werden
    dameSpielerAlt = 1
    dameSpielerNeu = 1
    dameComputerAlt = 1
    dameComputerNeu = 1

    # Spielstand holen
    gewinnerAlt, anzahlComputerAlt, anzahlSpielerAlt = spielstand.spielStand(
        altesFeld, spieler)
    gewinnerNeu, anzahlComputerNeu, anzahlSpielerNeu = spielstand.spielStand(
        neuesFeld, spieler)

    # Damedifferenz berechnen
    dameSpielerDiff = (dameSpielerNeu - dameSpielerAlt)*dame
    dameComputerDiff = (dameComputerNeu - dameComputerAlt)*dame

    dameDiff = dameSpielerDiff - dameComputerDiff if spieler \
        else dameComputerDiff - dameSpielerDiff

    # Steinedifferenz berechnen
    spielerDiff = (anzahlSpielerNeu - anzahlSpielerAlt)*rauswurf
    computerDiff = (anzahlComputerNeu - anzahlComputerAlt)*rauswurf

    steineDiff = spielerDiff - computerDiff if spieler \
        else computerDiff - spielerDiff

    # Bewertung ausrechnen und zurueckgeben
    bewertung = dameDiff + steineDiff

    return bewertung