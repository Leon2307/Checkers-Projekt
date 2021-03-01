import pygame
import gui

def moeglicheZuege(feld, spieler):
    for y in range(len(feld)):
        for x in range(len(feld)):
            feld[y][x].zügeBerechnen(feld, spieler, y, x)

def spielerZug(feld, feldgroesse, h):
   gui.mausGedrueckt(feld,feldgroesse,True, h)

def computerZug(feld, feldgroesse, h):
    gui.mausGedrueckt(feld,feldgroesse,False, h)