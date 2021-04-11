import pygame
import zuege.ausfuehren as zuege
import gui.variablen as var
import sys

minMaxGedrueckt = False

# Checkt ob die Maus gedrueckt wurde
def mausGedrueckt(feld, feldgroesse, spieler, h):
    global minMaxGedrueckt

    var.resetting = False

    # mausGedrueckt(feld, feldgroesse)
    if pygame.mouse.get_pressed()[0]:
        y, x = getMausFeld(feldgroesse)
        zuege.zugAusfuehren(feld, spieler, y, x, h)
        checkReset(h)
        checkMinMax(h)
    else:
        minMaxGedrueckt = False


# Checken ob das Feld durch klicken auf die Krone zurueckgesetzt wurde
def checkReset(h):

    x, y = pygame.mouse.get_pos()
    if x > var.GAMEWEITE and x < var.GAMEWEITE + var.SEITENWEITE \
            and y > 0 and y < var.SEITENWEITE:
        var.resetting = True
        h.resetFeld()


# Checkt ob der Minimaxknopf gedrückt wurde
def checkMinMax(h):
    global minMaxGedrueckt

    x, y = pygame.mouse.get_pos()
    
    # Checkt ob Minimax Blau gedrückt wurde und schaltet um
    if x > var.GAMEWEITE and x < var.GAMEWEITE + int(var.SEITENWEITE*0.4) \
        and y > var.GAMEHOEHE//2.5 and y < var.GAMEHOEHE//2.5 + int(var.SEITENWEITE*0.15) and not minMaxGedrueckt:
        h.wechselMiniMaxOnBlau()
        minMaxGedrueckt = True
        return

    # Checkt ob Minimax Gruen gedrückt wurde und schaltet um
    elif x > var.GAMEWEITE and x < var.GAMEWEITE + int(var.SEITENWEITE*0.4) \
        and y > var.GAMEHOEHE//1.3 and y < var.GAMEHOEHE//1.3 + int(var.SEITENWEITE*0.15) and not minMaxGedrueckt:
        h.wechselMiniMaxOnGruen()
        minMaxGedrueckt = True
        return


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
