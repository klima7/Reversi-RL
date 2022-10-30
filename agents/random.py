import random

from . import Agent
from environment import Environment


class RandomAgent(Agent):

    def take_action(self, env: Environment):
        state = env.get_current_state()
        actions = env.get_possible_actions(state)
        return random.choice(actions)
