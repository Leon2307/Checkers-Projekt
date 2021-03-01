import pygame

def moeglicheZuege(feld, spieler):
    pass

def spielerZug(feld):
    for y in range(len(feld)):
        for x in range(len(feld)):
            feld[y][x].zügeBerechnen(feld, True, y, x)
    return None, None

def computerZug(feld):
    return None, None