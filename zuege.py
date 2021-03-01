import pygame

def moeglicheZuege(feld, spieler):
    for y in range(len(feld)):
        for x in range(len(feld)):
            feld[y][x].zügeBerechnen(feld, spieler, y, x)

def spielerZug(feld):
    return None, None

def computerZug(feld):
    return None, None