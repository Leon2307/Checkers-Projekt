from zuege import berechnen
from zuege.berechnen import spielStand
from zuege import ausfuehren
import copy


speicherFeld = []
BERECHNUNGSTIEFE = 4


# Minimax
def minimax(feld, spieler, alpha=float("inf"), beta=float("-inf"), tiefe=BERECHNUNGSTIEFE):
    global BERECHNUNGSTIEFE, speicherFeld

    # Im ersten Durchlauf das Spielfeld speichern
    if tiefe == BERECHNUNGSTIEFE:
        speicherFeld = copy.deepcopy(feld)

    # Abbruchbedingungen
    if tiefe == 0:
        return zugBewerten(feld, speicherFeld, spieler), None

    sieger = spielStand(feld, spieler)[0]
    if sieger != None:
        return (float('-inf') if sieger else float('inf')), None

    bestesErgebnis = float('inf') if spieler else float('-inf')
    besterZug = None

    # Alle moeglichen Zuege ausprobieren
    for i, zugAlt in enumerate(zuglisteGenerieren(feld, spieler)):

        feldKopie = copy.deepcopy(feld)
        zugNeu = zuglisteGenerieren(feldKopie, spieler)[i]
        virtuellZiehen(feldKopie, zugNeu, spieler)
        bewertung = minimax(feldKopie, not spieler, alpha, beta, tiefe-1)[0]

        # Ergebnis des aktuellen Zuges mit bestem vorherigen vergleichen
        if spieler:
            if bestesErgebnis > bewertung:
                bestesErgebnis = bewertung
                besterZug = zugAlt
                alpha = min(bewertung, alpha)
        else:
            if bestesErgebnis < bewertung:
                bestesErgebnis = bewertung
                besterZug = zugAlt
                beta = max(bewertung, beta)

        # unterbricht die Schleife, falls kein besserer Wert mehr erwartet wird
        if alpha <= beta:
            if besterZug == None:
                besterZug = zugAlt
            break

    return bestesErgebnis, besterZug


# Liste mit moeglichen Zuegen generieren
def zuglisteGenerieren(feld, spieler):

    berechnen.moeglicheZuege(feld, spieler)

    alleZuege = []

    # Geht durch alle Felder des aktuellen Spielers und fuegt die Zuege zur Liste hinzu
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
    dame = 2

    # Spielstand holen
    gewinnerAlt, anzahlComputerAlt, dameComputerAlt, anzahlSpielerAlt, dameSpielerAlt = spielStand(
        altesFeld, spieler)
    gewinnerNeu, anzahlComputerNeu, dameComputerNeu, anzahlSpielerNeu, dameSpielerNeu = spielStand(
        neuesFeld, spieler)

    # Damedifferenz berechnen
    dameSpielerDiff = (dameSpielerNeu - dameSpielerAlt)*dame
    dameComputerDiff = (dameComputerNeu - dameComputerAlt)*dame

    dameDiff = dameComputerDiff - dameSpielerDiff

    # Steinedifferenz berechnen
    spielerDiff = (anzahlSpielerNeu - anzahlSpielerAlt)*rauswurf
    computerDiff = (anzahlComputerNeu - anzahlComputerAlt)*rauswurf

    steineDiff = computerDiff - spielerDiff

    # Bewertung ausrechnen und zurueckgeben
    bewertung = steineDiff + dameDiff

    # Wenn ein Spieler gewonnen hat unendlich zurueckgeben
    if gewinnerAlt == None and gewinnerNeu != None:
        bewertung = float('-inf') if spieler else float('inf')

    return bewertung


# Zug ausfuehren
def virtuellZiehen(feld, zug, spieler):

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
