import pygame
import sys

WEITE = 1000
HOEHE = 1000

BLACK = (32,32,32)
WHITE = (255,255,255)

GRAU = (100,100,100)
letzteMarkiert = None
letzteNachbarn = []

LINIENFARBE = (235,171,52)
LINIENDICKE = 5

#Spielfiguren
figurGruen = pygame.image.load("images/steinGruen.png")
figurGruen = pygame.transform.scale(figurGruen, (WEITE//8, HOEHE//8))
figurBlau = pygame.image.load("images/steinBlau.png")
figurBlau = pygame.transform.scale(figurBlau, (WEITE//8, HOEHE//8))

#Fenster initialisieren
pygame.init()
screen = pygame.display.set_mode((WEITE, HOEHE))
pygame.display.set_caption("Checkers") 

#Kontrolliert Abbruchbedingung und Events
def events(feldgroesse, feld):
    global letzteMarkiert

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    if pygame.mouse.get_pressed()[0]:
        y, x = getMausFeld(feldgroesse)

        #Geklicktes Feld markieren
        if feld[y][x].isPlayer() and len(feld[y][x].getZüge()) > 0:
            if letzteMarkiert != None:
                letzteMarkiert.makeClicked(False)
                for n in letzteNachbarn:
                    n.makeNachbar(False)
            letzteMarkiert = feld[y][x]
            feld[y][x].makeClicked(True)

            #Nachbarn markieren
            for zug in feld[y][x].getZüge():
                zug.makeNachbar(True)
                letzteNachbarn.append(zug)

#Auswertung der Mausposition
def getMausFeld(feldgroesse):
    x, y = pygame.mouse.get_pos()
    field_size = WEITE // feldgroesse
    derzeitigesX = x // field_size  
    derzeitigesY = y // field_size
    return derzeitigesY, derzeitigesX

#Funktion zum Zeichnen der Oberfläche
def draw(feld, feldgroesse):

    feldWeite = WEITE // feldgroesse
    feldHoehe = HOEHE // feldgroesse

    screen.fill((255,255,255))

    for y in range(feldgroesse):
        for x in range(feldgroesse):

            #Feldfarbe
            feldFarbe = WHITE if feld[y][x].isWhite() else BLACK
            if feld[y][x].isClicked():
                feldFarbe = GRAU
            pygame.draw.rect(screen,feldFarbe,(x*feldWeite, y*feldHoehe, feldWeite, feldHoehe))

            #Spielfigur
            if feld[y][x].isComputer():
                spielfigur = figurBlau
                screen.blit(spielfigur,(x*feldWeite, y*feldHoehe))
            elif feld[y][x].isPlayer():
                spielfigur = figurGruen
                screen.blit(spielfigur,(x*feldWeite, y*feldHoehe))

            #Zug möglich
            if len(feld[y][x].getZüge()) > 0:
                #Rechteck um Feld zeichnen
                pygame.draw.line(screen,LINIENFARBE,(x*feldWeite+LINIENDICKE//2, y*feldHoehe+LINIENDICKE//2),(x*feldWeite+feldWeite-LINIENDICKE//2, y*feldHoehe+LINIENDICKE//2), LINIENDICKE)
                pygame.draw.line(screen,LINIENFARBE,(x*feldWeite+feldWeite-LINIENDICKE//2, y*feldHoehe),(x*feldWeite+feldWeite-LINIENDICKE//2, y*feldHoehe+feldHoehe+LINIENDICKE//2), LINIENDICKE)
                pygame.draw.line(screen,LINIENFARBE,(x*feldWeite+LINIENDICKE//2, y*feldHoehe+feldHoehe-LINIENDICKE//2),(x*feldWeite+feldWeite-LINIENDICKE//2, y*feldHoehe+feldHoehe-LINIENDICKE//2), LINIENDICKE)
                pygame.draw.line(screen,LINIENFARBE,(x*feldWeite+LINIENDICKE//2, y*feldHoehe),(x*feldWeite+LINIENDICKE//2, y*feldHoehe+feldHoehe+LINIENDICKE//2), LINIENDICKE)

            #Nachbarn markieren
            if feld[y][x].isNachbar():
                pygame.draw.circle(screen,GRAU,(x*feldWeite+feldWeite//2, y*feldHoehe+feldHoehe//2), feldWeite//6)

    pygame.display.update()

    events(feldgroesse, feld)
