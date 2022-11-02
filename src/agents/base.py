from abc import ABC, abstractmethod
import pickle
from pathlib import Path


class Agent(ABC):

    NAME = None

    def __init__(self, size, learn):
        self.__size = size
        self.__knowledge_path = self.__get_knowledge_path()

        self.learn = learn
        self.knowledge = self.__get_knowledge()

    def initialize(self, env):
        pass

    @abstractmethod
    def get_action(self, env):
        pass

    def save_knowledge(self):
        if self.knowledge is None:
            return
        with open(self.__knowledge_path, 'wb') as f:
            return pickle.dump(self.knowledge, f)

    def __get_knowledge_path(self):
        root_path = Path(__file__).parent.parent.parent
        filename = f'{self.__size[0]}x{self.__size[1]}_{self.NAME}.pickle'
        return root_path / 'res' / filename

    def __get_knowledge(self):
        if not self.__knowledge_path.exists():
            return None
        with open(self.__knowledge_path, 'rb') as f:
            return pickle.load(f)
