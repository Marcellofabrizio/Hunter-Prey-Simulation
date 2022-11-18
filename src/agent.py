import random

from enum import Enum
from numpy import array

from utils import Colors

class AgentStates(Enum):
    wander = 0
    flee = 1
    hunt = 2


class Agent():

    def __init__(self, life, state, pos):
        self.life = life
        self.state = state
        self.pos = array(pos)
        self.possible_moves = [array([0,1]), array([0,-1]), 
                               array([1,0]), array([-1,0])]
        self.dir_vector = random.choice(self.possible_moves)

    def move(self):
        print(self.dir_vector)
        new_pos = self.pos + self.dir_vector
        if self.world.is_free(new_pos):
            x, y = new_pos
            self.pos = array([x%self.world.w, y%self.world.h])
            return
        else:
            new_dir = random.choice(self.possible_moves)
            while (new_dir==self.dir_vector).all() == True:
                new_dir = random.choice(self.possible_moves)
            self.dir_vector = new_dir
            self.move()

    def color(self):
        if self.state == AgentStates.flee:
            return Colors.YELLOW
        elif self.state == AgentStates.hunt:
            return Colors.RED

class Hunter(Agent):

    def __init__(self, life, state, pos):
      super().__init__(life,state,pos)  

    def color(self):
        if self.state == AgentStates.wander:
            return Colors.BLUE
        else:
            return super().color()

class Prey(Agent):

    def __init__(self, life, state, pos):
      super().__init__(life,state,pos)  

    def color(self):
        if self.state == AgentStates.wander:
            return Colors.GREEN
        else:
            return super().color()

