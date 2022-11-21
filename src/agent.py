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
        self.possible_moves = [array([0, 1]), array([0, -1]),
                               array([1, 0]), array([-1, 0])]
       
        self.dir_vector = random.choice(self.possible_moves)

        self.move_counter = 0
        self.emotion_quality = 0
        self.emotion_intensity = 0
        self.emotion_quality_limit = 3        
        self.emotion_intensity_limit = 3

    def move(self):
        new_pos = self.pos + self.dir_vector

        self.check_surroundings()

        if not self.world.is_free(new_pos):
            print("Collision avoided")
            return

        if self.move_counter < 10 or self.state != AgentStates.wander:
            self.pos = self.world.get_env_pos(new_pos)
            self.move_counter += 1
            return

        elif self.move_counter >= 10 and self.state == AgentStates.wander:
            new_dir = random.choice(self.possible_moves)
            new_pos = self.pos + new_dir
            self.move_counter = 0
            if not self.world.is_free(new_pos):
                print("Collision avoided")
                return

        self.dir_vector = new_dir
        self.pos = self.world.get_env_pos(new_pos)
        self.move_counter += 1

        self.check_surroundings()

    def color(self):
        if self.state == AgentStates.flee:
            return Colors.YELLOW
        elif self.state == AgentStates.hunt:
            return Colors.RED

    def update_emotions(self):
        pass


class Hunter(Agent):

    def __init__(self, life, state, pos):
        super().__init__(life, state, pos)
        self.surroundings = [array([0, 1]), array([0, -1]),
                               array([1, 0]), array([-1, 0])]

    def color(self):
        if self.state == AgentStates.wander:
            return Colors.BLUE
        else:
            return super().color()

    def check_surroundings(self):
        pass

class Prey(Agent):

    def __init__(self, life, state, pos):
        super().__init__(life, state, pos)

    def color(self):
        if self.state == AgentStates.wander:
            return Colors.GREEN
        else:
            return super().color()

    def check_surroundings(self):
        for i in range(-2, 2, 1):
            for j in range(-2, 2, 1):
                if i != 0 and j != 0:
                    agent = self.world.get_env_value((i+self.pos[0],j+self.pos[1]))
                    
                    if agent == None:
                        continue

                    elif isinstance(agent, Hunter):
                        print("Found hunter")

                        if any(agent.dir_vector*-1 == self.dir_vector):
                            self.dir_vector = agent.dir_vector
                        else:
                            self.dir_vector = agent.dir_vector*-1
                        
                        self.state = AgentStates.flee
