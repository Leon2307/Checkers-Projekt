import pygame
import zuege.ausfuehren as zuege
import gui.variablen as var
import sys

bereitsGedrueckt = False

# Checkt ob die Maus gedrueckt wurde


def mausGedrueckt(feld, feldgroesse, spieler, h):
    global bereitsGedrueckt

    var.resetting = False

    # mausGedrueckt(feld, feldgroesse)
    if pygame.mouse.get_pressed()[0]:
        y, x = getMausFeld(feldgroesse)
        zuege.zugAusfuehren(feld, spieler, y, x, h)
        checkReset(h)
        checkMinMax(h)
        checkZugZurueck(h)
    else:
        bereitsGedrueckt = False


# Checken ob das Feld durch klicken auf die Krone zurueckgesetzt wurde
def checkReset(h):
    global bereitsGedrueckt

    x, y = pygame.mouse.get_pos()
    if x > var.GAMEWEITE and x < var.GAMEWEITE + var.SEITENWEITE \
            and y > 0 and y < var.SEITENWEITE and not bereitsGedrueckt:
        var.resetting = True
        h.resetFeld()
        bereitsGedrueckt = True


# Checken ob ein Zug durch klicken des zurueck Buttons zurueck gegangen wird
def checkZugZurueck(h):
    global bereitsGedrueckt

    x, y = pygame.mouse.get_pos()
    if x > var.GAMEWEITE+var.SEITENWEITE//3 and x < var.GAMEWEITE + var.SEITENWEITE - var.SEITENWEITE//3 \
            and y > var.GAMEHOEHE//1.45 and y < var.GAMEHOEHE//1.45 + int(var.SEITENWEITE*0.15) and not bereitsGedrueckt:
        h.zugZurueck()
        bereitsGedrueckt = True


# Checkt ob der Minimaxknopf gedrueckt wurde
def checkMinMax(h):
    global bereitsGedrueckt

    x, y = pygame.mouse.get_pos()

    # Checkt ob Minimax Blau gedrueckt wurde und schaltet um
    if x > var.GAMEWEITE and x < var.GAMEWEITE + int(var.SEITENWEITE*0.4) \
            and y > var.GAMEHOEHE//2.5 and y < var.GAMEHOEHE//2.5 + int(var.SEITENWEITE*0.15) and not bereitsGedrueckt:
        h.wechselMiniMaxOnBlau()
        bereitsGedrueckt = True
        return

    # Checkt ob Minimax Gruen gedrueckt wurde und schaltet um
    elif x > var.GAMEWEITE and x < var.GAMEWEITE + int(var.SEITENWEITE*0.4) \
            and y > var.GAMEHOEHE//1.3 and y < var.GAMEHOEHE//1.3 + int(var.SEITENWEITE*0.15) and not bereitsGedrueckt:
        h.wechselMiniMaxOnGruen()
        bereitsGedrueckt = True
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
