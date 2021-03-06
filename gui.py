import pygame
import sys
import zuege


GAMEWEITE = 1000
GAMEHOEHE = 1000

SEITENWEITE = 200

BLACK = (32, 32, 32)
WHITE = (255, 255, 255)
GRAU = (100, 100, 100)
BLAU = (114, 186, 207)
GRUEN = (113, 146, 113)

LINIENFARBE = (235, 171, 52)
LINIENDICKE = 5

wiederholt = 0

# Spielfiguren
figurGruenBild = pygame.image.load("images/steinGruen.png")
figurGruen = pygame.transform.scale(
    figurGruenBild, (GAMEWEITE//8, GAMEHOEHE//8))
figurBlauBild = pygame.image.load("images/steinBlau.png")
figurBlau = pygame.transform.scale(figurBlauBild, (GAMEWEITE//8, GAMEHOEHE//8))

dameGruenBild = pygame.image.load("images/dameGruen.png")
dameGruen = pygame.transform.scale(dameGruenBild, (GAMEWEITE//8, GAMEHOEHE//8))
dameBlauBild = pygame.image.load("images/dameBlau.png")
dameBlau = pygame.transform.scale(dameBlauBild, (GAMEWEITE//8, GAMEHOEHE//8))

# Figuren Seitenfenster
teiler = 4

figurBlauTrans = pygame.image.load("images/steinBlauTrans.png")
figurGruenTrans = pygame.image.load("images/steinGruenTrans.png")
figurBlauSeite = pygame.transform.scale(
    figurBlauBild, (SEITENWEITE//teiler, SEITENWEITE//teiler))
figurGruenSeite = pygame.transform.scale(
    figurGruenBild, (SEITENWEITE//teiler, SEITENWEITE//teiler))
figurBlauTransSeite = pygame.transform.scale(
    figurBlauTrans, (SEITENWEITE//teiler, SEITENWEITE//teiler))
figurGruenTransSeite = pygame.transform.scale(
    figurGruenTrans, (SEITENWEITE//teiler, SEITENWEITE//teiler))

# Dame-Bild
dameBild = pygame.image.load('images/dameFigur.png')
dameBild = pygame.transform.scale(dameBild, (SEITENWEITE, SEITENWEITE))

# Sieger-Bild
gruenSieger = pygame.image.load("images/gruenGewonnen.png")
gruenSieger = pygame.transform.scale(
    gruenSieger, (SEITENWEITE, int(SEITENWEITE*0.3)))
blauSieger = pygame.image.load("images/blauGewonnen.png")
blauSieger = pygame.transform.scale(
    blauSieger, (SEITENWEITE, int(SEITENWEITE*0.3)))

# Fenster initialisieren
pygame.init()
gameScreen = pygame.display.set_mode((GAMEWEITE+SEITENWEITE, GAMEHOEHE))
pygame.display.set_caption("Checkers")

# Schrift initialisieren
textSize = SEITENWEITE//7
pygame.font.init()
font = pygame.font.SysFont("Laksaman", textSize)


def mausGedrueckt(feld, feldgroesse, spieler, h):
    global letzteMarkiert, letzteNachbarn

    # mausGedrueckt(feld, feldgroesse)
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
    field_size = GAMEWEITE // feldgroesse
    derzeitigesX = x // field_size
    derzeitigesY = y // field_size
    return derzeitigesY, derzeitigesX

# Funktion zum Zeichnen der Oberfläche


def drawSeitenleiste(feld, spieler):
    global wiederholt

    # Dame-Bild
    gameScreen.blit(dameBild, (GAMEWEITE, 0))

    # Spielstand holen
    sieger, steineComputer, steineSpieler = zuege.spielStand(feld, spieler)

    # rausgeworfene Steine zeichnen
    for i in range(12):

        # Computer
        bild = figurBlauSeite if not(
            i - steineComputer < 0) else figurBlauTransSeite

        xPos = GAMEWEITE+i % teiler * SEITENWEITE // teiler
        yPos = GAMEHOEHE-(SEITENWEITE//teiler)*(12//teiler) + \
            i // teiler * (SEITENWEITE // teiler)

        gameScreen.blit(bild, (xPos, yPos))

        # Spieler
        bild = figurGruenSeite if not(
            i - steineSpieler < 0) else figurGruenTransSeite

        xPos = GAMEWEITE+i % teiler * SEITENWEITE // teiler
        yPos = SEITENWEITE + i // teiler * (SEITENWEITE // teiler)

        gameScreen.blit(bild, (xPos, yPos))

    # Gewinner zeichnen
    if sieger != None:
        wiederholt += 1
        if wiederholt > 1:
            siegerSpieler = gruenSieger if sieger else blauSieger
            gameScreen.blit(siegerSpieler, (GAMEWEITE, GAMEHOEHE//2))

    else:
        wiederholt = 0


def draw(feld, feldgroesse, spieler):

    feldWeite = GAMEWEITE // feldgroesse
    feldHoehe = GAMEHOEHE // feldgroesse

    gameScreen.fill((255, 255, 255))

    # Felder im Hintergrund zeichnen (unterste Ebene)
    for y in range(feldgroesse):
        for x in range(feldgroesse):

            # Feldfarbe
            feldFarbe = WHITE if feld[y][x].isWhite() else BLACK
            if feld[y][x].isClicked():
                feldFarbe = GRAU
            pygame.draw.rect(gameScreen, feldFarbe, (x*feldWeite,
                                                     y*feldHoehe, feldWeite, feldHoehe))

            # Zug möglich
            if len(feld[y][x].getZüge()) > 0:

                # Rechteck um Feld zeichnen
                pygame.draw.line(gameScreen, LINIENFARBE, (x*feldWeite+LINIENDICKE//2, y*feldHoehe+LINIENDICKE//2),
                                 (x*feldWeite+feldWeite-LINIENDICKE//2, y*feldHoehe+LINIENDICKE//2), LINIENDICKE)
                pygame.draw.line(gameScreen, LINIENFARBE, (x*feldWeite+feldWeite-LINIENDICKE//2, y*feldHoehe),
                                 (x*feldWeite+feldWeite-LINIENDICKE//2, y*feldHoehe+feldHoehe+LINIENDICKE//2), LINIENDICKE)
                pygame.draw.line(gameScreen, LINIENFARBE, (x*feldWeite+LINIENDICKE//2, y*feldHoehe+feldHoehe-LINIENDICKE//2),
                                 (x*feldWeite+feldWeite-LINIENDICKE//2, y*feldHoehe+feldHoehe-LINIENDICKE//2), LINIENDICKE)
                pygame.draw.line(gameScreen, LINIENFARBE, (x*feldWeite+LINIENDICKE//2, y*feldHoehe),
                                 (x*feldWeite+LINIENDICKE//2, y*feldHoehe+feldHoehe+LINIENDICKE//2), LINIENDICKE)

    # Linie zu Ziel zeichnen (mittlere Ebene)
    for y in range(feldgroesse):
        for x in range(feldgroesse):
            if feld[y][x].isClicked():
                for index in range(len(feld[y][x].getZüge())):
                    punkteGui = []

                    # X,Y Wert von 0-7
                    punktePosition = feld[y][x].getPunkte(index)

                    # Punkte werden zu Feldgröße skaliert
                    for p in punktePosition:
                        punkteGui.append(
                            (p[0]*feldWeite+feldWeite//2, p[1]*feldHoehe+feldHoehe//2))

                    # Linie zu Punkten zeichnen
                    linienFarbe = GRUEN if feld[y][x].isPlayer() else BLAU
                    pygame.draw.lines(gameScreen, linienFarbe, False,
                                      punkteGui, width=10)

    # Steine und Punkte in Felder zeichnen (oberste Ebene)
    for y in range(feldgroesse):
        for x in range(feldgroesse):
           # Spielfigur
            if feld[y][x].isComputer():
                if feld[y][x].isDame():
                    gameScreen.blit(dameBlau, (x*feldWeite, y*feldHoehe))
                else:
                    gameScreen.blit(figurBlau, (x*feldWeite, y*feldHoehe))
            elif feld[y][x].isPlayer():
                if feld[y][x].isDame():
                    gameScreen.blit(dameGruen, (x*feldWeite, y*feldHoehe))
                else:
                    gameScreen.blit(figurGruen, (x*feldWeite, y*feldHoehe))

            # Nachbarn markieren
            if feld[y][x].isMoeglicherZug():

                # Kreis in Zentrum des Feldes zeichnen
                pygame.draw.circle(
                    gameScreen, GRAU, (x*feldWeite+feldWeite//2, y*feldHoehe+feldHoehe//2), feldWeite//6)

    # Seitenfenster mit Anzeige etc.
    drawSeitenleiste(feld, spieler)

    pygame.display.update()

    events(feldgroesse, feld)
