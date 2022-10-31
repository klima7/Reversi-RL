import random

from . import Agent, agent
from environment import Environment


@agent('random')
class RandomAgent(Agent):

    def take_action(self, env: Environment):
        state = env.get_current_state()
        actions = env.get_possible_actions(state)
        return random.choice(actions)
