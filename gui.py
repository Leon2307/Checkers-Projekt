import pygame
import sys
import zuege


WEITE = 1000
HOEHE = 1000

BLACK = (32, 32, 32)
WHITE = (255, 255, 255)
GRAU = (100, 100, 100)
BLAU = (114, 186, 207)
GRUEN = (113, 146, 113)

LINIENFARBE = (235, 171, 52)
LINIENDICKE = 5

# Spielfiguren
figurGruen = pygame.image.load("images/steinGruen.png")
figurGruen = pygame.transform.scale(figurGruen, (WEITE//8, HOEHE//8))
figurBlau = pygame.image.load("images/steinBlau.png")
figurBlau = pygame.transform.scale(figurBlau, (WEITE//8, HOEHE//8))

dameGruen = pygame.image.load("images/dameGruen.png")
dameGruen = pygame.transform.scale(dameGruen, (WEITE//8, HOEHE//8))
dameBlau = pygame.image.load("images/dameBlau.png")
dameBlau = pygame.transform.scale(dameBlau, (WEITE//8, HOEHE//8))

# Fenster initialisieren
pygame.init()
screen = pygame.display.set_mode((WEITE, HOEHE))
pygame.display.set_caption("Checkers")


def mausGedrueckt(feld, feldgroesse, spieler, h):
    global letzteMarkiert, letzteNachbarn

    #mausGedrueckt(feld, feldgroesse)
    if pygame.mouse.get_pressed()[0]:
        y, x = getMausFeld(feldgroesse)

        zuege.zugAusführen(feld, spieler, y, x, h)


# Kontrolliert Abbruchbedingung und Events
def events(feldgroesse, feld):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Auswertung der Mausposition


def getMausFeld(feldgroesse):
    x, y = pygame.mouse.get_pos()
    field_size = WEITE // feldgroesse
    derzeitigesX = x // field_size
    derzeitigesY = y // field_size
    return derzeitigesY, derzeitigesX

# Funktion zum Zeichnen der Oberfläche


def draw(feld, feldgroesse):

    feldWeite = WEITE // feldgroesse
    feldHoehe = HOEHE // feldgroesse

    screen.fill((255, 255, 255))

    # Felder im Hintergrund zeichnen (unterste Ebene)
    for y in range(feldgroesse):
        for x in range(feldgroesse):

            # Feldfarbe
            feldFarbe = WHITE if feld[y][x].isWhite() else BLACK
            if feld[y][x].isClicked():
                feldFarbe = GRAU
            pygame.draw.rect(screen, feldFarbe, (x*feldWeite,
                                                 y*feldHoehe, feldWeite, feldHoehe))

            # Zug möglich
            if len(feld[y][x].getZüge()) > 0:

                # Rechteck um Feld zeichnen
                pygame.draw.line(screen, LINIENFARBE, (x*feldWeite+LINIENDICKE//2, y*feldHoehe+LINIENDICKE//2),
                                 (x*feldWeite+feldWeite-LINIENDICKE//2, y*feldHoehe+LINIENDICKE//2), LINIENDICKE)
                pygame.draw.line(screen, LINIENFARBE, (x*feldWeite+feldWeite-LINIENDICKE//2, y*feldHoehe),
                                 (x*feldWeite+feldWeite-LINIENDICKE//2, y*feldHoehe+feldHoehe+LINIENDICKE//2), LINIENDICKE)
                pygame.draw.line(screen, LINIENFARBE, (x*feldWeite+LINIENDICKE//2, y*feldHoehe+feldHoehe-LINIENDICKE//2),
                                 (x*feldWeite+feldWeite-LINIENDICKE//2, y*feldHoehe+feldHoehe-LINIENDICKE//2), LINIENDICKE)
                pygame.draw.line(screen, LINIENFARBE, (x*feldWeite+LINIENDICKE//2, y*feldHoehe),
                                 (x*feldWeite+LINIENDICKE//2, y*feldHoehe+feldHoehe+LINIENDICKE//2), LINIENDICKE)

    # Linie zu Ziel zeichnen (mittlere Ebene)
    for y in range(feldgroesse):
        for x in range(feldgroesse):
            if feld[y][x].isClicked():
                for index in range(len(feld[y][x].getZüge())):
                    punkteGui = []

                    # X,Y Wert von 0-7
                    punktePosition = feld[y][x].getPunkte(index)
                    print(punktePosition)

                    # Punkte werden zu Feldgröße skaliert
                    for p in punktePosition:
                        punkteGui.append(
                            (p[0]*feldWeite+feldWeite//2, p[1]*feldHoehe+feldHoehe//2))

                    # Linie zu Punkten zeichnen
                    linienFarbe = GRUEN if feld[y][x].isPlayer() else BLAU
                    pygame.draw.lines(screen, linienFarbe, False,
                                      punkteGui, width=10)

    # Steine und Punkte in Felder zeichnen (oberste Ebene)
    for y in range(feldgroesse):
        for x in range(feldgroesse):
           # Spielfigur
            if feld[y][x].isComputer():
                if feld[y][x].isDame():
                    screen.blit(dameBlau, (x*feldWeite, y*feldHoehe))
                else:
                    screen.blit(figurBlau, (x*feldWeite, y*feldHoehe))
            elif feld[y][x].isPlayer():
                if feld[y][x].isDame():
                    screen.blit(dameGruen, (x*feldWeite, y*feldHoehe))
                else:
                    screen.blit(figurGruen, (x*feldWeite, y*feldHoehe))

            # Nachbarn markieren
            if feld[y][x].isMoeglicherZug():

                # Kreis in Zentrum des Feldes zeichnen
                pygame.draw.circle(
                    screen, GRAU, (x*feldWeite+feldWeite//2, y*feldHoehe+feldHoehe//2), feldWeite//6)

    pygame.display.update()

    events(feldgroesse, feld)
