from world import World
from agent import *

def main():
    world = World()
    hunter1 = Hunter(20, AgentStates.wander, (10,10))
    hunter2 = Hunter(20, AgentStates.wander, (15,5))
    prey1 = Prey(20, AgentStates.wander, (5,5))
    world.add_agent(hunter1)
    world.add_agent(hunter2)
    world.add_agent(prey1)
    world.start_world()

main()
