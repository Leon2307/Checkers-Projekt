from zuege import spielstand, berechnen
from zuege.computer import ausfuehrenComputer as ausComp
import copy


speicherFeld = []


# Minimax
def minimax(feld, tiefe, spieler):

    if tiefe == 6:
        speicherFeld = copy.deepcopy(feld)

    if tiefe == 0:
        return zugBewerten(feld, speicherFeld, spieler), None

    sieger = spielstand.spielStand(feld, spieler)[0]
    if sieger != None:
        return (-99999 if sieger else 99999), None

    if spieler:
        bestesErgebnis = float('inf')
        besterZug = None
        for i, zugAlt in enumerate(zuglisteGenerieren(feld, True)):
            feldKopie = copy.deepcopy(feld)
            zugNeu = zuglisteGenerieren(feldKopie,True)[i]
            ausComp.ziehen(feldKopie, zugNeu, spieler)
            bewertung = minimax(feldKopie, tiefe-1, False)[0]
            bestesErgebnis = min(bewertung, bestesErgebnis)
            if bestesErgebnis == bewertung:
                besterZug = zugAlt

        return bestesErgebnis, besterZug

    else:
        bestesErgebnis = float('-inf')
        besterZug = None
        for i, zugAlt in enumerate(zuglisteGenerieren(feld, False)):
            feldKopie = copy.deepcopy(feld)
            zugNeu = zuglisteGenerieren(feldKopie, False)[i]
            ausComp.ziehen(feldKopie, zugNeu, spieler)
            bewertung = minimax(feldKopie, tiefe-1, True)[0]
            bestesErgebnis = max(bewertung, bestesErgebnis)
            if bestesErgebnis == bewertung:
                besterZug = zugAlt

        return bestesErgebnis, besterZug


# Liste mit möglichen Zuegen generieren
def zuglisteGenerieren(feld, spieler):

    berechnen.moeglicheZuege(feld, spieler)

    alleZuege = []

    for y in range(len(feld)):
        for x in range(len(feld)):

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
    rauswurf = 3
    dame = 4

    # Spielstand holen
    gewinnerAlt, anzahlComputerAlt, dameComputerAlt, anzahlSpielerAlt, dameSpielerAlt = spielstand.spielStand(
        altesFeld, spieler)
    gewinnerNeu, anzahlComputerNeu, dameComputerNeu, anzahlSpielerNeu, dameSpielerNeu = spielstand.spielStand(
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
    if gewinnerAlt == None and gewinnerNeu != None:
        bewertung = float('inf') if not spieler else float('-inf') 

    return bewertung