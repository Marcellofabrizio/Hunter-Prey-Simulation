import random
import argparse

from world import World
from agent import *

def main(agents):

    world = World()

    for agent in agents:
        world.add_agent(agent)

    world.start_world()

def create_agents(num_hunters, num_preys, move_limit, points):

    agents = []

    for h in range(num_hunters):
        point = random.choice(points)
        points.remove(point)

        hunter = Hunter(AgentStates.wander, point, move_limit)
        agents.append(hunter)

    for p in range(num_preys):
        point = random.choice(points)
        points.remove(point)

        prey = Prey(AgentStates.wander, point, move_limit)
        agents.append(prey)

    return agents

def generate_random_points(rows, cols, num_hunters, num_preys):

    random_points = []

    for _ in range(num_hunters+10):
        random_point = (random.randint(0,cols), random.randint(0,rows))
        if not random_point in random_points:
            random_points.append(random_point)

    for _ in range(num_preys+10):
        random_point = (random.randint(0,cols), random.randint(0,rows))
        if not random_point in random_points:
            random_points.append(random_point)

    return random_points

parser = argparse.ArgumentParser(description="Hunter prey simulation.")

parser.add_argument("-H", "--hunters", default='4')
parser.add_argument("-P", "--preys", default='1')
parser.add_argument("-M", "--moveLimit", default='10')

args = parser.parse_args()
print(args)

num_hunters = int(args.__dict__["hunters"])
num_preys = int(args.__dict__["preys"])
move_limit = int(args.__dict__["moveLimit"])

random_points = generate_random_points(20,20, num_hunters, num_preys)
agents = create_agents(num_hunters, num_preys, move_limit, random_points)

main(agents)
