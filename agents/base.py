from abc import ABC, abstractmethod


class Agent(ABC):

    def __init__(self, knowledge, learn):
        self._knowledge = knowledge
        self._learn = learn

    def initialize(self, env):
        pass

    @abstractmethod
    def take_action(self, env):
        pass
