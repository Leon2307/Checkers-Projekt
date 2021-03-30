import pygame

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
# Grün
figurGruenBild = pygame.image.load("images/steinGruen.png")
figurGruen = pygame.transform.scale(
    figurGruenBild, (GAMEWEITE//8, GAMEHOEHE//8))

# Blau
figurBlauBild = pygame.image.load("images/steinBlau.png")
figurBlau = pygame.transform.scale(figurBlauBild, (GAMEWEITE//8, GAMEHOEHE//8))

# Dame Grün
dameGruenBild = pygame.image.load("images/dameGruen.png")
dameGruen = pygame.transform.scale(dameGruenBild, (GAMEWEITE//8, GAMEHOEHE//8))

# Dame Blau
dameBlauBild = pygame.image.load("images/dameBlau.png")
dameBlau = pygame.transform.scale(dameBlauBild, (GAMEWEITE//8, GAMEHOEHE//8))


teiler = 4

# Figuren Seitenfenster (Transparent)
# Grün
figurGruenTrans = pygame.image.load("images/steinGruenTrans.png")
figurGruenSeite = pygame.transform.scale(
    figurGruenBild, (SEITENWEITE//teiler, SEITENWEITE//teiler))
figurGruenTransSeite = pygame.transform.scale(
    figurGruenTrans, (SEITENWEITE//teiler, SEITENWEITE//teiler))

# Blau
figurBlauSeite = pygame.transform.scale(
    figurBlauBild, (SEITENWEITE//teiler, SEITENWEITE//teiler))
figurBlauTrans = pygame.image.load("images/steinBlauTrans.png")
figurBlauTransSeite = pygame.transform.scale(
    figurBlauTrans, (SEITENWEITE//teiler, SEITENWEITE//teiler))

# Dame-Bild (Gold)
dameBild = pygame.image.load('images/dameFigur.png')
dameBild = pygame.transform.scale(dameBild, (SEITENWEITE, SEITENWEITE))
dameBildGold = pygame.image.load('images/dameFigurGold.png')
dameBildGold = pygame.transform.scale(dameBildGold, (SEITENWEITE, SEITENWEITE))


# Sieger-Bild
# Grün
gruenSieger = pygame.image.load("images/gruenGewonnen.png")
gruenSieger = pygame.transform.scale(
    gruenSieger, (SEITENWEITE, int(SEITENWEITE*0.3)))

# Blau
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

# Resetting => angeben ob das Spielfeld gerade resettet wird und damit keinen Gewinner anzeigen
resetting = False