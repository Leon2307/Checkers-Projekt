import pygame
import gui

def moeglicheZuege(feld, spieler):
    for y in range(len(feld)):
        for x in range(len(feld)):
            feld[y][x].zügeBerechnen(feld, spieler, y, x)

def spielerZug(feld, feldgroesse):
   gui.mausGedrueckt(feld,feldgroesse)

def computerZug(feld):
    pass