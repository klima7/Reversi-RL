from abc import ABC, abstractmethod
import pickle
from pathlib import Path


class Agent(ABC):

    NAME = None

    def __init__(self, size, learn):
        self.size = size
        self.learn = learn
        self.knowledge = self.__get_knowledge()
        self.save_knowledge()

    def __get_knowledge_path(self):
        root_path = Path(__file__).parent.parent.parent
        filename = f'{self.size[0]}x{self.size[1]}_{self.NAME}.pickle'
        return root_path / 'res' / filename

    def __get_knowledge(self):
        path = self.__get_knowledge_path()
        if not path.exists():
            return {}
        with open(path, 'rb') as f:
            return pickle.load(f)

    def save_knowledge(self):
        if len(self.knowledge.keys()) == 0:
            return
        path = self.__get_knowledge_path()
        with open(path, 'wb') as f:
            return pickle.dump(self.knowledge, f)

    def initialize(self, env):
        pass

    @abstractmethod
    def get_action(self, env):
        pass
