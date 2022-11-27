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

    def __init__(self, life, state, pos, move_limit):
        self.life = life
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
        new_pos = self.pos + self.dir_vector

        self.check_surroundings()

        if not self.world.is_free(new_pos):
            return

        if self.move_counter < self.move_limit or self.state != AgentStates.wander:

            if self.state == AgentStates.hunt:
                traces = []
                for move in self.possible_moves:
                    pos = self.pos + move
                    traces.append(
                        {
                            "trace": self.world.get_trace_value(pos),
                            "pos": pos
                        })

                traces.sort(key=lambda x: x["trace"])
                most_recent_trace = traces[0]
                if most_recent_trace["trace"] > 0:
                    new_pos = most_recent_trace["pos"]

            else:
                self.world.set_trace_value(new_pos,10)

            self.pos = self.world.get_env_pos(new_pos)
            self.move_counter += 1
            return

        elif self.move_counter >= self.move_limit and self.state == AgentStates.wander:
            new_dir = random.choice(self.possible_moves)
            new_pos = self.pos + new_dir
            self.move_counter = 0
            if not self.world.is_free(new_pos):
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

    def get_close_agents(self, radius):
        close_agents = []
        for i in range(-1*radius, radius+1, 1):
            for j in range(-1*radius, radius+1, 1):
                if i != 0 and j != 0:
                    agent = self.world.get_env_value(
                        (i+self.pos[0], j+self.pos[1]))

                    if agent != None:
                        close_agents.append(agent)

        return close_agents

    def update_emotions(self):
        pass


class Hunter(Agent):

    def __init__(self, life, state, pos, move_limit):
        super().__init__(life, state, pos, move_limit)
        self.radius = 3

    def color(self):
        if self.state == AgentStates.wander:
            return Colors.BLUE
        else:
            return super().color()

    def check_surroundings(self):
        close_agents = self.get_close_agents(self.radius)

        if len(close_agents) > 0:
            hunters = list(
                filter(lambda a: isinstance(a, Hunter), close_agents))
            preys = list(filter(lambda a: isinstance(a, Prey), close_agents))

            if len(preys) == 0:
                self.emotion_intensity -= 1

            for agent in close_agents:
                if isinstance(agent, Prey) and agent.state != AgentStates.dead:

                    if any(agent.dir_vector*-1 == self.dir_vector):
                        self.dir_vector = agent.dir_vector
                    else:
                        self.dir_vector = agent.dir_vector*-1

                    self.emotion_quality = self.emotion_quality_lo_limit
                    self.emotion_intensity = self.emotion_intensity_hi_limit
                    self.state = AgentStates.hunt

        if self.emotion_intensity == 0:
            self.state = AgentStates.wander


class Prey(Agent):

    def __init__(self, life, state, pos, move_limit):
        super().__init__(life, state, pos, move_limit)
        self.radius = 3
        self.death_radius = 3

    def color(self):
        if self.state == AgentStates.wander:
            return Colors.GREEN
        else:
            return super().color()

    def check_surroundings(self):
        close_agents = self.get_close_agents(self.radius)

        if len(close_agents) > 0 and self.alive:
            preys = list(filter(lambda a: isinstance(a, Prey), close_agents))
            hunters = list(
                filter(lambda a: isinstance(a, Hunter), close_agents))

            if len(hunters) > 2:
                self.state = AgentStates.dead
                self.world.kill_agent(self)

            for agent in close_agents:
                if isinstance(agent, Hunter):

                    if any(agent.dir_vector*-1 == self.dir_vector):
                        self.dir_vector = agent.dir_vector
                    else:
                        self.dir_vector = agent.dir_vector*-1

                elif isinstance(agent, Prey):
                    if agent.state == AgentStates.flee:
                        self.emotion_quality = max(
                            self.emotion_quality-1, self.emotion_quality_lo_limit)
                        self.emotion_intensity = min(
                            self.emotion_intensity+1, self.emotion_intensity_hi_limit)

            if self.emotion_quality < 0:
                self.state = AgentStates.flee
