import pygame
import gui.variablen as var
import gui.events as evnt
import zuege.spielstand as zuege

# Funktion zum Zeichnen der Oberfläche
def drawSeitenleiste(feld, spieler):
    global wiederholt

    # Dame-Bild
    aktDameBild = var.dameBild if not var.resetting else var.dameBildGold
    var.gameScreen.blit(aktDameBild, (var.GAMEWEITE, 0))

    # Spielstand holen
    sieger, steineComputer, steineSpieler = zuege.spielStand(feld, spieler)

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
        yPos = var.SEITENWEITE + i // var.teiler * (var.SEITENWEITE // var.teiler)

        var.gameScreen.blit(bild, (xPos, yPos))

    # Gewinner zeichnen
    if sieger != None and not var.resetting:
        var.wiederholt += 1
        if var.wiederholt > 1:
            siegerSpieler = var.gruenSieger if sieger else var.blauSieger
            var.gameScreen.blit(siegerSpieler, (var.GAMEWEITE, var.GAMEHOEHE//2))

    else:
        wiederholt = 0


def draw(feld, feldgroesse, spieler):

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

            # Zug möglich
            if len(feld[y][x].getZuege()) > 0:

                # Rechteck um Feld zeichnen
                pygame.draw.line(var.gameScreen, var.LINIENFARBE, (x*feldWeite+var.LINIENDICKE//2, y*feldHoehe+var.LINIENDICKE//2),
                                 (x*feldWeite+feldWeite-var.LINIENDICKE//2, y*feldHoehe+var.LINIENDICKE//2), var.LINIENDICKE)
                pygame.draw.line(var.gameScreen, var.LINIENFARBE, (x*feldWeite+feldWeite-var.LINIENDICKE//2, y*feldHoehe),
                                 (x*feldWeite+feldWeite-var.LINIENDICKE//2, y*feldHoehe+feldHoehe+var.LINIENDICKE//2), var.LINIENDICKE)
                pygame.draw.line(var.gameScreen, var.LINIENFARBE, (x*feldWeite+var.LINIENDICKE//2, y*feldHoehe+feldHoehe-var.LINIENDICKE//2),
                                 (x*feldWeite+feldWeite-var.LINIENDICKE//2, y*feldHoehe+feldHoehe-var.LINIENDICKE//2), var.LINIENDICKE)
                pygame.draw.line(var.gameScreen, var.LINIENFARBE, (x*feldWeite+var.LINIENDICKE//2, y*feldHoehe),
                                 (x*feldWeite+var.LINIENDICKE//2, y*feldHoehe+feldHoehe+var.LINIENDICKE//2), var.LINIENDICKE)

    # Linie zu Ziel zeichnen (mittlere Ebene)
    for y in range(feldgroesse):
        for x in range(feldgroesse):
            if feld[y][x].isClicked():
                for index in range(len(feld[y][x].getZuege())):
                    punkteGui = []

                    # X,Y Wert von 0-7
                    punktePosition = feld[y][x].getPunkte(index)

                    # Punkte werden zu Feldgröße skaliert
                    for p in punktePosition:
                        punkteGui.append(
                            (p[0]*feldWeite+feldWeite//2, p[1]*feldHoehe+feldHoehe//2))

                    # Linie zu Punkten zeichnen
                    linienFarbe = var.GRUEN if feld[y][x].isPlayer() else var.BLAU
                    pygame.draw.lines(var.gameScreen, linienFarbe, False,
                                      punkteGui, width=10)

    # Steine und Punkte in Felder zeichnen (oberste Ebene)
    for y in range(feldgroesse):
        for x in range(feldgroesse):

           # Spielfigur
            if feld[y][x].isComputer():
                if feld[y][x].isDame():
                    var.gameScreen.blit(var.dameBlau, (x*feldWeite, y*feldHoehe))
                else:
                    var.gameScreen.blit(var.figurBlau, (x*feldWeite, y*feldHoehe))
            elif feld[y][x].isPlayer():
                if feld[y][x].isDame():
                    var.gameScreen.blit(var.dameGruen, (x*feldWeite, y*feldHoehe))
                else:
                    var.gameScreen.blit(var.figurGruen, (x*feldWeite, y*feldHoehe))

            # Nachbarn markieren
            if feld[y][x].isMoeglicherZug():

                # Kreis in Zentrum des Feldes zeichnen
                pygame.draw.circle(
                    var.gameScreen, var.GRAU, (x*feldWeite+feldWeite//2, y*feldHoehe+feldHoehe//2), feldWeite//6)

    # Seitenfenster mit Anzeige etc.
    drawSeitenleiste(feld, spieler)

    pygame.display.update()

    evnt.events(feldgroesse, feld)