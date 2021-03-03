import pygame
import gui

letzteMarkiert = None
letzteNachbarn = []

def moeglicheZuege(feld, spieler):
    for y in range(len(feld)):
        for x in range(len(feld)):
            feld[y][x].zügeBerechnen(feld, spieler, y, x)

def zugAusführen(feld, spieler, y, x, h):
    global letzteMarkiert, letzteNachbarn
    nachbarIndex = None
    
    #Geklicktes Feld markieren
    if (spieler and feld[y][x].isPlayer()
    or not spieler and feld[y][x].isComputer()) and len(feld[y][x].getZüge()) > 0:
        if letzteMarkiert != None:
            letzteMarkiert.makeClicked(False)
            for n in letzteNachbarn:
                n[0].makeNachbar(False)
            letzteNachbarn = []
        letzteMarkiert = feld[y][x]
        feld[y][x].makeClicked(True)

        #Nachbarn markieren
        for zug in feld[y][x].getZüge():
            zug[0].makeNachbar(True)
            letzteNachbarn.append(zug)

    #Ist Geklicktes Feld Nachbar?
    elif feld[y][x].isNachbar():
        letzteMarkiert.makePlayer(False)
        letzteMarkiert.makeComputer(False)
        letzteMarkiert.makeClicked(False)
        feld[y][x].makePlayer(True) if spieler else feld[y][x].makeComputer(True)
        i = 0
        for n in letzteNachbarn:
            if n[0] == feld[y][x]:
                nachbarIndex = i
            n[0].makeNachbar(False)
            i += 1
        h.wechselSpieler()
        #rauswerfen
        if letzteMarkiert.getZüge()[nachbarIndex][1] != None:
            letzteMarkiert.getZüge()[nachbarIndex][1].makePlayer(False)
            letzteMarkiert.getZüge()[nachbarIndex][1].makeComputer(False)
        letzteMarkiert = None
        letzteNachbarn = []

def spielerZug(feld, feldgroesse, h):
   gui.mausGedrueckt(feld,feldgroesse,True, h)

def computerZug(feld, feldgroesse, h):
    gui.mausGedrueckt(feld,feldgroesse,False, h)