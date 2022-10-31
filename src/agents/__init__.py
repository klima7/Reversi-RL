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


agents = {}


def agent(name):
    def decorator(cls):
        if name in agents.keys():
            raise Exception(f'Agent name was already taken: {name}')
        cls.agent_name = name
        agents[name] = cls
        return cls
    return decorator


from .random import RandomAgent
