import pygame
import zuege.ausfuehren as zuege
import gui.variablen as var
import sys

# Checkt ob die Maus gedrückt wurde
def mausGedrueckt(feld, feldgroesse, spieler, h):
    global letzteMarkiert, letzteNachbarn, resetting

    resetting = False

    # mausGedrueckt(feld, feldgroesse)
    if pygame.mouse.get_pressed()[0]:
        y, x = getMausFeld(feldgroesse)
        zuege.zugAusfuehren(feld, spieler, y, x, h)
        checkReset(h)


# Checken ob das Feld durch klicken auf die Krone zurückgesetzt wurde
def checkReset(h):
    global resetting

    x, y = pygame.mouse.get_pos()
    if x > var.GAMEWEITE and x < var.GAMEWEITE + var.SEITENWEITE \
            and y > 0 and y < var.SEITENWEITE:
        resetting = True
        h.resetFeld()


# Kontrolliert Abbruchbedingung (schließen des Fensters)
def events(feldgroesse, feld):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# Auswertung der Mausposition
def getMausFeld(feldgroesse):

    x, y = pygame.mouse.get_pos()
    field_size = var.GAMEWEITE // feldgroesse
    derzeitigesX = x // field_size
    derzeitigesY = y // field_size

    return derzeitigesY, derzeitigesX
