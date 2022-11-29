from world import World
from agent import *

def main():

    move_limit = 5

    world = World()
    hunter1 = Hunter(20, AgentStates.wander, (10,10), move_limit)
    hunter2 = Hunter(20, AgentStates.wander, (15,5), move_limit)
    hunter3 = Hunter(20, AgentStates.wander, (15,6), move_limit)
    hunter4 = Hunter(20, AgentStates.wander, (16,6), move_limit)
    hunter5 = Hunter(20, AgentStates.wander, (17,6), move_limit)
    hunter6 = Hunter(20, AgentStates.wander, (18,6), move_limit)
    hunter7 = Hunter(20, AgentStates.wander, (19,6), move_limit)
    hunter8 = Hunter(20, AgentStates.wander, (1 ,7), move_limit)
    prey1 = Prey(20, AgentStates.wander, (5,5), move_limit)
    prey2 = Prey(20, AgentStates.wander, (7,7), move_limit)
    prey3 = Prey(20, AgentStates.wander, (7,8), move_limit)
    prey4 = Prey(20, AgentStates.wander, (7,9), move_limit)

    world.add_agent(hunter1)
    world.add_agent(hunter2)
    world.add_agent(hunter3)
    world.add_agent(hunter4)
    world.add_agent(hunter5)
    world.add_agent(hunter6)
    # world.add_agent(hunter7)
    # world.add_agent(hunter8)
    world.add_agent(prey1)
    world.add_agent(prey2)
    # world.add_agent(prey3)
    # world.add_agent(prey4)
    world.start_world()

main()
