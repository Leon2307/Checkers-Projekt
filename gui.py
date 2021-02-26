import pygame

WIDTH = 1000
HEIGHT = 1000

BLACK = (32,32,32)
WHITE = (255,255,255)

def initWindow():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers")
    print("init")

def draw(feld, feldgroesse):
    pass