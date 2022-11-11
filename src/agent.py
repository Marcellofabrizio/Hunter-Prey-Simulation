import random

from enum import Enum
from numpy import array

class AgentStates(Enum):
    idle = 0
    flight = 1
    hunt = 2


class Agent():

    def __init__(self, life, state, pos):
        self.life = life
        self.state = state
        self.pos = array(pos)
        self.dir_vector = array([0,0])
        self.possible_moves = [array([0,1]), array([0,-1]), 
                               array([1,0]), array([-1,0])]

    def move(self):
        new_pos = self.pos + self.dir_vector
        if self.can_move(new_pos):
            self.pos = new_pos
        else:
            new_dir = random.choise(self.possible_moves)
            while new_dir == self.dir_vector:
                new_dir = random.choise(self.possible_moves)
            self.dir_vector = new_dir
            self.move()

    def can_move(self, pos):
        pass
