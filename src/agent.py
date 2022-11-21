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

        self.emotion_quality = 0
        self.emotion_intensity = 0
        self.move_counter = 0

    def move(self):
        new_pos = self.pos + self.dir_vector
        if self.move_counter < 10 or (self.world.is_free(new_pos) and self.state != AgentStates.wander):
            print(self.state)
            self.pos = self.world.get_env_pos(new_pos)
            self.move_counter += 1
            return

        elif self.move_counter >= 10 and self.state == AgentStates.wander:
            new_dir = random.choice(self.possible_moves)
            new_pos = self.pos + new_dir
            self.move_counter = 0
            if not self.world.is_free(new_pos):
                return 

        self.dir_vector = new_dir
        self.pos = self.world.get_env_pos(new_pos)
        self.move_counter += 1

    def color(self):
        if self.state == AgentStates.flee:
            return Colors.YELLOW
        elif self.state == AgentStates.hunt:
            return Colors.RED

    def update_emotions(self):
        pass

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

