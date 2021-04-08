from zuege import ausfuehren


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

