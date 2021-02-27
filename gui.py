import pygame
import sys

WEITE = 1000
HOEHE = 1000

BLACK = (32,32,32)
WHITE = (255,255,255)

#Spielfiguren
figurGruen = pygame.image.load("images/steinGruen.png")
figurGruen = pygame.transform.scale(figurGruen, (WEITE//8, HOEHE//8))
figurBlau = pygame.image.load("images/steinBlau.png")
figurBlau = pygame.transform.scale(figurBlau, (WEITE//8, HOEHE//8))

#Fenster initialisieren
pygame.init()
screen = pygame.display.set_mode((WEITE, HOEHE))
pygame.display.set_caption("Checkers") 

def quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def draw(feld, feldgroesse):

    feldWeite = WEITE // feldgroesse
    feldHoehe = HOEHE // feldgroesse

    screen.fill((255,255,255))

    for y in range(feldgroesse):
        for x in range(feldgroesse):

            #Feldfarbe
            feldFarbe = WHITE if feld[y][x].isWhite() else BLACK
            pygame.draw.rect(screen,feldFarbe,(x*feldWeite, y*feldHoehe, feldWeite, feldHoehe))

            #Spielfigur
            if feld[y][x].isComputer():
                spielfigur = figurBlau
                screen.blit(spielfigur,(x*feldWeite, y*feldHoehe))
            elif feld[y][x].isPlayer():
                spielfigur = figurGruen
                screen.blit(spielfigur,(x*feldWeite, y*feldHoehe))

    pygame.display.update()

    quit()
