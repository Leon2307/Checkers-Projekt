
letzteMarkiert = None
letzteNachbarn = []

def setLetzteMarkiert(markiert):
    global letzteMarkiert
    letzteMarkiert = markiert

def getLetzteMarkiert():
    global letzteMarkiert
    return letzteMarkiert

def setLetzteNachbarn(nachbarn):
    global letzteNachbarn
    letzteNachbarn = nachbarn

def getLetzteNachbarn():
    global letzteNachbarn
    return letzteNachbarn

def zugAusfuehren(feld, spieler, y, x, h):
    global letzteMarkiert, letzteNachbarn
    nachbarIndex = None

    # Pruefen ob das Feld existiert
    if y < 0 or y > len(feld)-1 or x < 0 or x > len(feld)-1:
        return

    # Geklicktes Feld markieren
    if (spieler and feld[y][x].isPlayer() or not spieler and feld[y][x].isComputer()) and len(feld[y][x].getZuege()) > 0:

        # Das zuletzt markierte Feld leeren
        if letzteMarkiert != None:
            letzteMarkiert.makeClicked(False)
            for n in letzteNachbarn:
                n.makeMoeglicherZug(False)
            letzteNachbarn = []

        # Neues geklicktes Feld zum aktuellen Spieler machen
        letzteMarkiert = feld[y][x]
        feld[y][x].makeClicked(True)

        # mögliche Zuege markieren
        for zug in feld[y][x].getZuege():

            zug[0].makeMoeglicherZug(True)
            letzteNachbarn.append(zug[0])

    # Ist Geklicktes Feld Nachbar?
    elif feld[y][x].isMoeglicherZug():

        # Funktionen in der Main aufrufen
        h.resetBereitsBerechnet()
        h.wechselSpieler()
        h.addZugZurueck()

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

        # Pruefen ob eine Dame entsteht
        checkDame(feld[y][x], y, spieler)

        # Nachbarn zuruecksetzen und index des geklickten Nachbarn ermitteln
        i = 0
        for n in letzteNachbarn:
            if n == feld[y][x]:
                nachbarIndex = i
            n.makeMoeglicherZug(False)
            i += 1

        # rauswerfen
        if letzteMarkiert.getZuege()[nachbarIndex][1] != None:
            for letzteZuege in letzteMarkiert.getZuege()[nachbarIndex][1]:
                if letzteZuege != None:
                    letzteZuege.makePlayer(False)
                    letzteZuege.makeComputer(False)
                    letzteZuege.makeDame(False)

        # moegliche Zuege leeren
        letzteMarkiert.setZuege([])

        letzteMarkiert = None
        letzteNachbarn = []


# Prueft ob durch Zug eine Dame entsteht
def checkDame(aktuellesFeld, y, spieler):
    if spieler and y == 0 or not spieler and y == 7:
        aktuellesFeld.makeDame(True)