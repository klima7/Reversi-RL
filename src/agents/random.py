import random

from . import PassiveAgent, agent


@agent
class RandomAgent(PassiveAgent):

    NAME = 'random'

    def get_action(self, state):
        actions = self.env.get_possible_actions(state)
        return random.choice(actions)
