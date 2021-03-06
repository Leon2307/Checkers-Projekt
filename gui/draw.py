import pygame
import gui.variablen as var
import gui.events as evnt
from zuege.berechnen import spielStand


# Zeichnet den Seitenbalken
def drawSeitenleiste(feld, spieler, mainObjekt):
    global wiederholt

    # Dame-Bild
    aktDameBild = var.dameBild if not var.resetting else var.dameBildGold
    var.gameScreen.blit(aktDameBild, (var.GAMEWEITE, 0))

    # Spielstand holen
    sieger, steineComputer, _, steineSpieler, _ = spielStand(feld, spieler)

    # rausgeworfene Steine zeichnen
    for i in range(12):

        # Computer
        bild = var.figurBlauSeite if not(
            i - steineComputer < 0) else var.figurBlauTransSeite

        xPos = var.GAMEWEITE+i % var.teiler * var.SEITENWEITE // var.teiler
        yPos = var.GAMEHOEHE-(var.SEITENWEITE//var.teiler)*(12//var.teiler) + \
            i // var.teiler * (var.SEITENWEITE // var.teiler)

        var.gameScreen.blit(bild, (xPos, yPos))

        # Spieler
        bild = var.figurGruenSeite if not(
            i - steineSpieler < 0) else var.figurGruenTransSeite

        xPos = var.GAMEWEITE+i % var.teiler * var.SEITENWEITE // var.teiler
        yPos = var.SEITENWEITE + i // var.teiler * \
            (var.SEITENWEITE // var.teiler)

        var.gameScreen.blit(bild, (xPos, yPos))

    # Button fuer Minimax
    # Blau
    minMaxButton = var.miniMaxOn if mainObjekt.getMiniMaxOnBlau() else var.miniMaxOff
    var.gameScreen.blit(minMaxButton, (var.GAMEWEITE, var.GAMEHOEHE//2.5))

    # Schrift fuer Minimax
    var.gameScreen.blit(var.miniMaxSchriftBlau, (var.GAMEWEITE +
                                                 int(var.SEITENWEITE*0.4), var.GAMEHOEHE//2.5))

    # Gruen
    minMaxButton = var.miniMaxOn if mainObjekt.getMiniMaxOnGruen() else var.miniMaxOff
    var.gameScreen.blit(minMaxButton, (var.GAMEWEITE, var.GAMEHOEHE//1.3))

    # Schrift fuer Minimax
    var.gameScreen.blit(var.miniMaxSchriftGruen, (var.GAMEWEITE +
                                                  int(var.SEITENWEITE*0.4), var.GAMEHOEHE//1.3))

    # Zug zurueck Button
    var.gameScreen.blit(var.zurueckButton, (var.GAMEWEITE +
                                            int(var.SEITENWEITE*0.4), var.GAMEHOEHE//1.45))

    # Gewinner zeichnen
    if sieger != None and not var.resetting:
        var.wiederholt += 1
        if var.wiederholt > 1:
            siegerSpieler = var.gruenSieger if sieger else var.blauSieger
            var.gameScreen.blit(
                siegerSpieler, (var.GAMEWEITE, var.GAMEHOEHE//1.8))
    else:
        var.wiederholt = 0


# Zeichnet das Spielfeld
def draw(feld, feldgroesse, spieler, mainObjekt):

    feldWeite = var.GAMEWEITE // feldgroesse
    feldHoehe = var.GAMEHOEHE // feldgroesse

    var.gameScreen.fill((255, 255, 255))

    # Felder im Hintergrund zeichnen (unterste Ebene)
    for y in range(feldgroesse):
        for x in range(feldgroesse):

            # Feldfarbe
            feldFarbe = var.WHITE if feld[y][x].isWhite() else var.BLACK
            if feld[y][x].isClicked():
                feldFarbe = var.GRAU
            pygame.draw.rect(var.gameScreen, feldFarbe, (x*feldWeite,
                                                         y*feldHoehe, feldWeite, feldHoehe))

            # Zug moeglich
            if len(feld[y][x].getZuege()) > 0:

                # Rechteck um Feld zeichnen
                pygame.draw.line(var.gameScreen, var.LINIENFARBE, (x*feldWeite, y*feldHoehe),
                                 (x*feldWeite+feldWeite-var.LINIENDICKE//2, y*feldHoehe), var.LINIENDICKE)
                pygame.draw.line(var.gameScreen, var.LINIENFARBE, (x*feldWeite+feldWeite-var.LINIENDICKE//2, y*feldHoehe),
                                 (x*feldWeite+feldWeite-var.LINIENDICKE//2, y*feldHoehe+feldHoehe), var.LINIENDICKE)
                pygame.draw.line(var.gameScreen, var.LINIENFARBE, (x*feldWeite, y*feldHoehe+feldHoehe-var.LINIENDICKE//2),
                                 (x*feldWeite+feldWeite-var.LINIENDICKE//2, y*feldHoehe+feldHoehe-var.LINIENDICKE//2), var.LINIENDICKE)
                pygame.draw.line(var.gameScreen, var.LINIENFARBE, (x*feldWeite, y*feldHoehe),
                                 (x*feldWeite, y*feldHoehe+feldHoehe), var.LINIENDICKE)

    # Linie zu Ziel zeichnen (mittlere Ebene)
    for y in range(feldgroesse):
        for x in range(feldgroesse):
            if feld[y][x].isClicked():
                for index in range(len(feld[y][x].getZuege())):
                    punkteGui = []

                    # X,Y Wert von 0-7
                    punktePosition = feld[y][x].getPunkte(index)

                    # Punkte werden zu Feldgroeße skaliert
                    for p in punktePosition:
                        punkteGui.append(
                            (p[0]*feldWeite+feldWeite//2, p[1]*feldHoehe+feldHoehe//2))

                    # Linie zu Punkten zeichnen
                    linienFarbe = var.GRUEN if feld[y][x].isPlayer(
                    ) else var.BLAU
                    pygame.draw.lines(var.gameScreen, linienFarbe, False,
                                      punkteGui, width=var.GAMEWEITE//100)

    # Steine und Punkte in Felder zeichnen (oberste Ebene)
    for y in range(feldgroesse):
        for x in range(feldgroesse):

           # Spielfigur
            if feld[y][x].isComputer():
                if feld[y][x].isDame():
                    var.gameScreen.blit(
                        var.dameBlau, (x*feldWeite, y*feldHoehe))
                else:
                    var.gameScreen.blit(
                        var.figurBlau, (x*feldWeite, y*feldHoehe))
            elif feld[y][x].isPlayer():
                if feld[y][x].isDame():
                    var.gameScreen.blit(
                        var.dameGruen, (x*feldWeite, y*feldHoehe))
                else:
                    var.gameScreen.blit(
                        var.figurGruen, (x*feldWeite, y*feldHoehe))

            # Nachbarn markieren
            if feld[y][x].isMoeglicherZug():

                # Kreis in Zentrum des Feldes zeichnen
                pygame.draw.circle(
                    var.gameScreen, var.GRAU, (x*feldWeite+feldWeite//2, y*feldHoehe+feldHoehe//2), feldWeite//6)

    # Seitenfenster mit Anzeige etc.
    drawSeitenleiste(feld, spieler, mainObjekt)

    pygame.display.update()

    evnt.checkAbbruch(feldgroesse, feld)
