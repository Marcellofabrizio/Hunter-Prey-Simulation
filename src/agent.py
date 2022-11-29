import random

from enum import Enum
from numpy import array

from utils import Colors


def get_array_difference(arr_A, arr_B):
    difference = []

    for a in arr_A:
        for b in arr_B:
            if a == b:
                difference.append(a)

    return difference


class AgentStates(Enum):
    wander = 0
    flee = 1
    hunt = 2
    dead = 4


class Agent():

    def __init__(self, state, pos, move_limit):
        self.state = state
        self.pos = array(pos)
        self.possible_moves = [array([0, 1]), array([0, -1]),
                               array([1, 0]), array([-1, 0])]

        self.dir_vector = random.choice(self.possible_moves)

        self.move_limit = move_limit
        self.move_counter = 0
        self.emotion_quality = 0
        self.emotion_intensity = 0
        self.emotion_quality_hi_limit = 3
        self.emotion_intensity_hi_limit = 3
        self.emotion_quality_lo_limit = self.emotion_quality_hi_limit*-1
        self.emotion_intensity_lo_limit = self.emotion_intensity_hi_limit*-1

    @property
    def alive(self):
        return self.state != AgentStates.dead

    def move(self):
        pass

    def color(self):
        if self.state == AgentStates.flee:
            return Colors.YELLOW
        elif self.state == AgentStates.hunt:
            return Colors.RED

    def get_close_agents(self, radius):
        close_agents = []
        for i in range(-1*radius, radius+1, 1):
            for j in range(-1*radius, radius+1, 1):
                if i != 0 and j != 0:
                    agent = self.world.get_env_value(
                        (self.pos[0]+i, self.pos[1]+j))

                    if agent != None:
                        close_agents.append(agent)

        return close_agents

    def update_emotions(self):
        pass


class Hunter(Agent):

    def __init__(self, state, pos, move_limit):
        super().__init__(state, pos, move_limit)
        self.radius = 3

    def color(self):
        if self.state == AgentStates.wander:
            return Colors.BLUE
        else:
            return super().color()

    def move(self):

        new_pos = self.pos + self.dir_vector

        if self.state == AgentStates.hunt:
            traces = []
            for move in self.possible_moves:
                pos = self.pos + move
                traces.append(
                    {
                        "trace": self.world.get_trace_value(pos),
                        "pos": pos
                    })
            traces.sort(key=lambda x: x["trace"], reverse=True)
            most_recent_trace = traces[0]
            if most_recent_trace["trace"] > 0:
                new_pos = most_recent_trace["pos"]
            else:
                new_dir = random.choice(self.possible_moves)
                new_pos = self.pos + new_dir

        else:
            if self.move_counter >= self.move_limit: 
                self.dir_vector = random.choice(self.possible_moves)
                self.move_counter = 0
                
            new_pos = self.pos + self.dir_vector

        if not self.world.is_free(new_pos):
            return False

        self.move_counter += 1
        self.pos = self.world.get_env_pos(new_pos)
        self.check_surroundings()

        return True

    def check_surroundings(self):
        close_agents = self.get_close_agents(self.radius)

        if len(close_agents) > 0:
            hunters = list(
                filter(lambda a: isinstance(a, Hunter), close_agents))
            preys = list(filter(lambda a: isinstance(a, Prey), close_agents))

            if len(preys) == 0:
                self.emotion_intensity -= 1

            for agent in preys:
                if any(agent.dir_vector*-1 == self.dir_vector):
                    self.dir_vector = agent.dir_vector
                else:
                    self.dir_vector = agent.dir_vector*-1

                self.emotion_quality = self.emotion_quality_lo_limit
                self.emotion_intensity = self.emotion_intensity_hi_limit

        if self.emotion_intensity > 0:
            self.state = AgentStates.hunt

        if self.emotion_intensity == 0:
            self.state = AgentStates.wander


class Prey(Agent):

    def __init__(self, state, pos, move_limit):
        super().__init__(state, pos, move_limit)
        self.radius = 3
        self.death_radius = 3
        self.no_pred_count = 0
        self.no_pred_limit = 5

    def color(self):
        if self.state == AgentStates.wander:
            return Colors.GREEN
        else:
            return super().color()

    def move(self):
        new_pos = self.pos + self.dir_vector

        if self.state != AgentStates.flee:
            if self.move_counter >= self.move_limit:
                self.dir_vector = random.choice(self.possible_moves)
                self.move_counter = 0

            new_pos = self.pos + self.dir_vector

        if not self.world.is_free(new_pos):
            return False

        self.move_counter += 1
        self.pos = self.world.get_env_pos(new_pos)
        self.check_surroundings()
        return True

    def check_surroundings(self):
        close_agents = self.get_close_agents(self.radius)
        preys = list(filter(lambda a: isinstance(a, Prey), close_agents))
        hunters = list(
            filter(lambda a: isinstance(a, Hunter), close_agents))


        if len(hunters) > 3:
            self.state = AgentStates.dead
            self.world.kill_agent(self)
            return
        
        elif len(hunters) == 0:
            self.no_pred_count = min(self.no_pred_count+1, self.no_pred_limit)

        else:
            self.no_pred_count = 0

        for agent in hunters:
            self.emotion_quality = self.emotion_quality_lo_limit
            self.emotion_intensity = self.emotion_intensity_hi_limit
            if any(agent.dir_vector*-1 == self.dir_vector):
                self.dir_vector = agent.dir_vector
            else:
                self.dir_vector = agent.dir_vector*-1

        for agent in preys:
            if agent.state == AgentStates.flee:
                self.emotion_quality = max(
                    self.emotion_quality-1, self.emotion_quality_lo_limit)
                self.emotion_intensity = min(
                    self.emotion_intensity+1, self.emotion_intensity_hi_limit)
            else:
                self.emotion_quality = max(
                    self.emotion_quality+1, self.emotion_quality_hi_limit)

        if self.no_pred_count == self.no_pred_limit:
            self.emotion_quality = 1
            self.emotion_intensity = 1

        if self.emotion_quality < 0:
            self.state = AgentStates.flee

        if self.emotion_quality >= 1:
            self.state = AgentStates.wander
