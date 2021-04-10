from zuege import spielstand, berechnen
from zuege import ausfuehren
import copy


speicherFeld = []
berechnungstiefe = 6


# Minimax
def minimax(feld, spieler, tiefe=berechnungstiefe):

    if tiefe == 6:
        speicherFeld = copy.deepcopy(feld)

    if tiefe == 0:
        return zugBewerten(feld, speicherFeld, spieler), None

    sieger = spielstand.spielStand(feld, spieler)[0]
    if sieger != None:
        return (-99999 if sieger else 99999), None

    bestesErgebnis = float('inf') if spieler else float('-inf')
    besterZug = None
    for i, zugAlt in enumerate(zuglisteGenerieren(feld, spieler)):
        feldKopie = copy.deepcopy(feld)
        zugNeu = zuglisteGenerieren(feldKopie, spieler)[i]
        ziehen(feldKopie, zugNeu, spieler)
        bewertung = minimax(feldKopie, tiefe-1, not spieler)[0]
        bestesErgebnis = min(bewertung, bestesErgebnis) if spieler \
            else max(bewertung, bestesErgebnis)
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


# Zug ausfuehren
def ziehen(feld, zug, spieler):

    # Das Startfeld leeren
    zug[3].makePlayer(False)
    zug[3].makeComputer(False)

    # Neues Feld zuweisen
    zug[0].makePlayer(True) if spieler else zug[0].makeComputer(True)

    # Wenn das Startfeld eine Dame ist: Dame zuweisen
    if zug[3].isDame():
        zug[0].makeDame(True)
        zug[3].makeDame(False)

    # Pruefen ob eine Dame entsteht
    ausfuehren.checkDame(zug[0], zug[0].getPosition()[1], spieler)

    # rauswerfen
    if zug[1] != (None, None):
        for letzteZuege in zug[1]:
            if letzteZuege != None:
                letzteZuege.makePlayer(False)
                letzteZuege.makeComputer(False)
                letzteZuege.makeDame(False)