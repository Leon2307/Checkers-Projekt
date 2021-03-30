import zuege.listeOptimieren as optm


dZügePlayer = [[-1, 1], [-1, -1]]
dZügeComputer = [[1, -1], [1, 1]]
dZügeDame = [[-1, 1], [-1, -1], [1, -1], [1, 1]]
zwangZüge = []

# Berechnet für jedes Feld die möglichen Züge
def moeglicheZuege(feld, spieler):
    for y in range(len(feld)):
        for x in range(len(feld)):
            feld[y][x].zügeBerechnen(feld, spieler, y, x)


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
        return optm.pickeBeste(zwangZüge)
    else:
        return zuegeMoeglich


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
                    if optm.bereitsWeg(y+j+speicherJ, x+i+speicherI, eckfelder.copy(), zwangZüge.copy()):
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
        return optm.pickeBeste(zwangZüge)
    else:
        return zuegeMoeglich