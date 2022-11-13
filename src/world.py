import pygame
import itertools
import numpy as np

from utils import Colors

SCREEN_SIZE = 500

class World():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Hunter-Prey")

        self.rows = 20
        self.cols = 20
        self.size = 30
        self.piece_size = 15
        self.line_size = 2
        self.w = self.size * self.cols
        self.h = self.size * self.rows
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.agents = list()
        self.env_array = np.array([[None for i in range(self.rows)] for j in range(self.cols)])

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
            pygame.draw.line(self.screen, Colors.BLACK, start, end, self.line_size)

    def draw_background(self):
        rect = pygame.Rect(0, 0, self.w, self.h)
        pygame.draw.rect(self.screen, Colors.WHITE, rect)

    def draw_board(self):
        self.draw_background()
        self.draw_lines()
        pygame.display.update()

    def start_world(self):
        self.draw_board()
        print(len(self.agents))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            self.draw_agents()

    def draw_agents(self):
        for agent in self.agents:
            x, y = (agent.pos[0] * self.size + self.size//2, agent.pos[1] * self.size + self.size//2)
            pygame.draw.rect(self.screen, agent.color(), (x+self.line_size, y+self.line_size, 
                                                        self.size-self.line_size, self.size-self.line_size))

        pygame.display.update()

    def add_agent(self, agent):
        agent.world = self
        self.agents.append(agent)

    def is_free(self, pos):
        return self.env_array[pos] != None
