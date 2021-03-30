

# Überprüft wie viele Steine noch drin sind und ob gewonnen wurde
def spielStand(feld, spieler):

    # verbliebene Steine auf dem Spielfeld
    anzahlSpieler = 0
    anzahlComputer = 0

    # verbliebene Züge auf dem Spielfeld
    übrigeZügeSpieler = []
    übrigeZügeComputer = []

    for y in range(len(feld)):
        for x in range(len(feld)):

            # Anzahl checken
            if feld[y][x].isPlayer():
                anzahlSpieler += 1
                if feld[y][x].getZüge() != []:
                    übrigeZügeSpieler.append(feld[y][x].getZüge())

            elif feld[y][x].isComputer():
                anzahlComputer += 1
                if feld[y][x].getZüge() != []:
                    übrigeZügeComputer.append(feld[y][x].getZüge())

    # return Sieger, computerSteine, spielerSteine
    # Spieler hat gewonnen
    if übrigeZügeComputer == [] and not spieler or anzahlComputer < 1:
        return True, anzahlComputer, anzahlSpieler

    # Computer hat gewonnen
    elif übrigeZügeSpieler == [] and spieler or anzahlSpieler < 1:
        return False, anzahlComputer, anzahlSpieler

    # Keiner hat gewonnen
    else:
        return None, anzahlComputer, anzahlSpieler


