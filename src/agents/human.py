from . import Agent, agent
from environment import Environment


@agent
class HumanAgent(Agent):

    NAME = 'human'

    def get_action(self, env: Environment):
        pass

    def save_knowledge(self):
        pass
