import zuege.listeOptimieren as optm


dZuegePlayer = [[-1, 1], [-1, -1]]
dZuegeComputer = [[1, -1], [1, 1]]
dZuegeDame = [[-1, 1], [-1, -1], [1, -1], [1, 1]]
zwangZuege = []

# Berechnet fuer jedes Feld die möglichen Zuege
def moeglicheZuege(feld, spieler):
    for y in range(len(feld)):
        for x in range(len(feld)):
            feld[y][x].zuegeBerechnen(feld, spieler, y, x)

# Nur den einen möglichen Zug des Computers anzeigen
def setzeBestenZug(feld, einzigerZug):
    for y in range(len(feld)):
        for x in range(len(feld)):
            feld[y][x].setZuege([])
    
    einzigerZug[3].setZuege([einzigerZug])


def zugzwang(feld, spieler, y, x, eckfelder=None, rausgeworfen=None, durchgang=0):
    global zwangZuege, anfangsX, anfangsY

    # Wenn der Durchgang 0 (1. Mal) ist wird alles auf Ausgangswert gesetzt
    if durchgang == 0:
        zwangZuege = []
        eckfelder = []
        rausgeworfen = []
        anfangsX = x
        anfangsY = y

    elif durchgang > 7:
        return False

    deltaZuege = dZuegePlayer if spieler else dZuegeComputer
    zuegeMoeglich = False
    moeglich = False

    # Alle Möglichkeiten durchgehen
    for j, i in deltaZuege:
        j2 = j*2
        i2 = i*2

        if durchgang != 0:
            eckfelderSave = eckfelder.copy()
            rausgeworfenSave = rausgeworfen.copy()
        else:
            eckfelderSave = []
            rausgeworfenSave = []

        # Auf Existenz pruefen
        if y+j < 0 or y+j > 7 or x+i < 0 or x+i > 7:
            continue

        # Auf leere des nächsten Feldes pruefen
        if not feld[y+j][x+i].isPlayer() and not feld[y+j][x+i].isComputer() and durchgang == 0:

            # Nächstes Feld als moeglicher Zug hinzufuegen
            zwangZuege.append(
                [feld[y+j][x+i], [None, None], [None], feld[y][x]])
            # continue

        # Auf Existenz pruefen
        if y+j2 < 0 or y+j2 > 7 or x+i2 < 0 or x+i2 > 7:
            continue

        # Auf Gegner pruefen und leere des dahinter liegenden Feldes
        if (feld[y+j][x+i].isComputer() and spieler or feld[y+j][x+i].isPlayer() and not spieler) and not feld[y+j2][x+i2].isPlayer() and not feld[y+j2][x+i2].isComputer():

            zuegeMoeglich = True
            neuesFeld = feld[y+j2][x+i2]
            rausgeworfenSave.append(feld[y+j][x+i])
            eckfelderSave.append(feld[y][x])

            # Versuchen noch einen Zug weiter zu gehen
            moeglich = zugzwang(feld, spieler, y+j2, x+i2,
                                eckfelderSave, rausgeworfenSave, durchgang+1)

            # Falls nicht weiter gegangen werden konnte aktuelles Feld hinzufuegen
            if not moeglich:
                zwangZuege.append(
                    (neuesFeld, rausgeworfenSave.copy(), eckfelderSave.copy(), feld[anfangsY][anfangsX]))
                rausgeworfenSave.pop()
                eckfelderSave.pop()

    if durchgang == 0:
        return optm.pickeBeste(zwangZuege)
    else:
        return zuegeMoeglich


def zugzwangDame(y, x, spieler, feld, eckfelder, rausgeworfen, durchgang, dZuegeDameHergekommen):
    global zwangZuege, anfangsX, anfangsY, dZuegeDame, dZuegeDame2

    dZuegeDameNeu = dZuegeDame.copy()
    if dZuegeDameHergekommen != None:
        for ind, dzug in enumerate(dZuegeDameNeu):
            if dzug == dZuegeDameHergekommen:
                del dZuegeDameNeu[ind]

    # Wenn der Durchgang 0 (1. Mal) ist wird alles auf Ausgangswert gesetzt
    if durchgang == 0:
        zwangZuege = []
        eckfelder = []
        rausgeworfen = []
        anfangsX = x
        anfangsY = y

    elif durchgang > 7:
        return False

    zuegeMoeglich = False
    moeglich = False

    # Alle Möglichkeiten durchgehen
    for j, i in dZuegeDameNeu:

        speicherJ = j
        speicherI = i
        while y+j < 8 and y+j >= 0 and x+i < 8 and x+i >= 0:

            # Auf leere des Feldes pruefen
            # Abbrechen wenn eigener Stein auf nächstem Feld
            if (feld[y+j][x+i].isPlayer() and spieler) or (feld[y+j][x+i].isComputer() and not spieler):
                break

            # Wenn frei ist und Durchgang 0
            elif not feld[y+j][x+i].isPlayer() and not feld[y+j][x+i].isComputer() and durchgang == 0:
                zwangZuege.append(
                    [feld[y+j][x+i], [None, None], [None], feld[y][x]])

            # Wenn ein Gegner auf dem nächsten Feld ist
            elif feld[y+j][x+i].isComputer() and spieler or feld[y+j][x+i].isPlayer() and not spieler:

                # Auf Existenz pruefen
                if not(y+j+speicherJ < 8 and y+j+speicherJ >= 0 and x+i+speicherI < 8 and x+i+speicherI >= 0):
                    break

                # Wenn das Feld besetzt ist pruefen ob das darauf Folgende frei ist
                if not feld[y+j+speicherJ][x+i+speicherI].isComputer() and not feld[y+j+speicherJ][x+i+speicherI].isPlayer():

                    # Felder hinzufuegen
                    zuegeMoeglich = True
                    neuesFeld = feld[y+j+speicherJ][x+i+speicherI]
                    rausgeworfen.append(feld[y+j][x+i])
                    eckfelder.append(feld[y][x])

                    # Wenn die neue Position nicht möglich ist, da bereits abgegangen
                    if optm.bereitsWeg(y+j+speicherJ, x+i+speicherI, eckfelder, zwangZuege):
                        moeglich = zugzwangDame(y+j+speicherJ, x+i+speicherI, spieler, feld,
                                                eckfelder, rausgeworfen, durchgang+1, [-speicherJ, -speicherI])

                    # Falls nicht weiter gegangen werden konnte aktuelles Feld hinzufuegen
                    if not moeglich:

                        zwangZuege.append(
                            (neuesFeld, rausgeworfen.copy(), eckfelder.copy(), feld[anfangsY][anfangsX]))

                    rausgeworfen.pop()
                    eckfelder.pop()
                    moeglich = False

                break

            # j und i erhöhen
            j = j+speicherJ
            i = i+speicherI

    if durchgang == 0:
        return optm.pickeBeste(zwangZuege)
    else:
        return zuegeMoeglich