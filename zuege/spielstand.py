from zuege.berechnen import moeglicheZuege

# ueberprueft wie viele Steine noch drin sind und ob gewonnen wurde
def spielStand(feld, spieler):
    
    # verbliebene Steine auf dem Spielfeld
    anzahlSpieler = 0
    anzahlDameSpieler = 0
    anzahlComputer = 0
    anzahlDameComputer = 0

    # verbliebene Zuege auf dem Spielfeld
    uebrigeZuegeSpieler = []
    uebrigeZuegeComputer = []

    moeglicheZuege(feld, True)
    for y in range(len(feld)):
        for x in range(len(feld)):

            # Anzahl checken
            if feld[y][x].isPlayer():
                anzahlSpieler += 1
                if feld[y][x].isDame():
                    anzahlDameSpieler += 1
                if feld[y][x].getZuege() != []:
                    uebrigeZuegeSpieler.append(feld[y][x].getZuege())

    moeglicheZuege(feld, False)
    for y in range(len(feld)):
        for x in range(len(feld)):

            if feld[y][x].isComputer():
                anzahlComputer += 1
                if feld[y][x].isDame():
                    anzahlDameComputer += 1
                if feld[y][x].getZuege() != []:
                    uebrigeZuegeComputer.append(feld[y][x].getZuege())

    # return Sieger, computerSteine, spielerSteine
    # Spieler hat gewonnen
    if uebrigeZuegeComputer == [] and not spieler or anzahlComputer < 1:
        return True, anzahlComputer, anzahlDameComputer, anzahlSpieler, anzahlDameSpieler

    # Computer hat gewonnen
    elif uebrigeZuegeSpieler == [] and spieler or anzahlSpieler < 1:
        return False, anzahlComputer, anzahlDameComputer, anzahlSpieler, anzahlDameSpieler

    # Keiner hat gewonnen
    else:
        return None, anzahlComputer, anzahlDameComputer, anzahlSpieler, anzahlDameSpieler


