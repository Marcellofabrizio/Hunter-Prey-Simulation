import pygame

SCREEN_SIZE = 500

class World():

    def __init__(self):
        pygame.init()
        pigame.display.set_caption("Hunter-Prey")

        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
