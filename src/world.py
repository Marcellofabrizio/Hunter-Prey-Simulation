import pygame
import itertools

SCREEN_SIZE = 500

class Colors():
    WHITE = (255,255,255)
    BLACK = (  0,  0,  0)

class World():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Hunter-Prey")

        self.rows = 20
        self.cols = 20
        self.size = 30
        self.piece_size = 15
        self.w = self.size * self.cols
        self.h = self.size * self.rows
        self.screen = pygame.display.set_mode((self.w, self.h))

    def draw_screen(self):
        scale = 20

        cell_count = SCREEN_SIZE//scale

    def row_lines(self):
        half_size = self.size//2

        for y in range(half_size, self.h - half_size + self.size, self.size):
            yield (half_size, y), (self.w-half_size, y)

    def col_lines(self):
        half_size = self.size//2

        for x in range(half_size, self.w - half_size + self.size, self.size):
            yield (x, half_size), (x, self.h-half_size)

    def draw_lines(self):
        lines = itertools.chain(self.row_lines(), self.col_lines())

        for start, end in lines:
            pygame.draw.line(self.screen, Colors.BLACK, start, end, 3)

    def draw_background(self):
        rect = pygame.Rect(0, 0, self.w, self.h)
        pygame.draw.rect(self.screen, Colors.WHITE, rect)

    def draw_board(self):
        self.draw_background()
        self.draw_lines()
        pygame.display.update()

    def start_world(self):
        self.draw_board()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
