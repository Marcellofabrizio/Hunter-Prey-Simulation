import pygame
import itertools
import numpy as np

from utils import Colors

SCREEN_SIZE = 500
FPS = 3


class World():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Hunter-Prey")
        self.fpsClock = pygame.time.Clock()

        self.rows = 20
        self.cols = 20
        self.size = 30
        self.piece_size = 15
        self.line_size = 2
        self.w = self.size * self.cols
        self.h = self.size * self.rows
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.agents = list()
        self.env_array = np.array(
            [[None for i in range(self.rows)] for j in range(self.cols)])
        self.trace_array = np.array(
            [[0 for i in range(self.rows)] for j in range(self.cols)])

    @property
    def alive_agents(self):
        return [a for a in self.agents if a.alive]

    def draw_screen(self):
        scale = 20

        cell_count = SCREEN_SIZE//scale

    def row_lines(self):
        half_size = self.size//2

        for y in range(0, self.h + self.size, self.size):
            yield (0, y), (self.w, y)

    def col_lines(self):
        half_size = self.size//2

        for x in range(0, self.w + self.size, self.size):
            yield (x, 0), (x, self.h)

    def draw_lines(self):
        lines = itertools.chain(self.row_lines(), self.col_lines())

        for start, end in lines:
            pygame.draw.line(self.screen, Colors.BLACK,
                             start, end, self.line_size)

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

            self.move_agents()
            self.draw_agents()
            self.fpsClock.tick(FPS)

    def move_agents(self):
        for agent in self.alive_agents:
            prev_pos = agent.pos
            agent.move()
            x, y = (prev_pos[0] * self.size,
                    prev_pos[1] * self.size)

            new_env_x, new_env_y = self.get_env_pos(agent.pos)
            old_env_x, old_env_y = self.get_env_pos(prev_pos)
            self.env_array[new_env_x, new_env_y] = agent
            self.env_array[old_env_x, old_env_y] = None

            pygame.draw.rect(self.screen, Colors.WHITE, (x+self.line_size, y+self.line_size,
                                                         self.size-self.line_size, self.size-self.line_size))
            
        self.decrease_traces()

    def draw_agents(self):
        for agent in self.alive_agents:
            x, y = (agent.pos[0] * self.size,
                    agent.pos[1] * self.size)
            pygame.draw.rect(self.screen, agent.color(), (x+self.line_size, y+self.line_size,
                                                          self.size-self.line_size, self.size-self.line_size))

        pygame.display.update()

    def decrease_traces(self):
        for x in range(0, self.cols):
            for y in range(0, self.rows):
                if self.trace_array[x, y] > 0:
                    self.trace_array[x, y] = self.trace_array[x, y] - 1

    def kill_agent(self, agent):
        self.env_array[agent.pos] = None
        self.agents = self.alive_agents

    def add_agent(self, agent):
        agent.world = self
        self.agents.append(agent)

    def is_free(self, pos):
        x, y = self.get_env_pos(pos)
        return self.env_array[x, y] == None

    def get_env_value(self, pos):
        x, y = self.get_env_pos(pos)
        return self.env_array[x, y]

    def get_env_pos(self, pos):
        x, y = pos
        return np.array([x % self.cols, y % self.rows])

    def get_trace_value(self, pos):
        x, y = self.get_env_pos(pos)
        return self.trace_array[x, y]

    def set_trace_value(self, pos, value):
        x, y = self.get_env_pos(pos)
        self.trace_array[x, y] = value
        print(self.trace_array)
