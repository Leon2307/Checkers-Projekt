
anfangsX = 0
anfangsY = 0

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


# Checkt ob Der nächste Zug auf ein mögliches/neues Feld geht
def bereitsWeg(neuesY, neuesX, eckfelder, zwangzuege):

    # Checkt ob Startfeld
    if neuesY == anfangsY and neuesX == anfangsX:
        return False

    # Checkt ob bereits abgegangen(eckfeld)
    for eFeld in eckfelder.copy():
        if eFeld.getPosition() == (neuesX, neuesY):
            return False

    # Checkt ob es bereits ein belegtes Feld ist
    for zug in zwangzuege.copy():
        if zug[0].getPosition() == (neuesY, neuesX) and zug[2] == [None]:
            return False

    # Ansonsten True
    return True