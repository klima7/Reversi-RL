from abc import ABC, abstractmethod
import _pickle as pickle
from pathlib import Path


class Agent(ABC):

    NAME = None

    def __init__(self, size, learn):
        self.__size = size
        self.__data_path = self.__get_data_path()

        self.learn = learn
        self.data = self.__get_data()

    def initialize(self, env):
        pass

    @abstractmethod
    def get_action(self, env):
        pass

    def save_data(self):
        if self.data is None:
            return
        with open(self.__data_path, 'wb') as f:
            return pickle.dump(self.data, f)

    def __get_data_path(self):
        root_path = Path(__file__).parent.parent.parent
        filename = f'{self.__size[0]}x{self.__size[1]}_{self.NAME}.pickle'
        return root_path / 'res' / filename

    def __get_data(self):
        if not self.__data_path.exists():
            return None
        with open(self.__data_path, 'rb') as f:
            return pickle.load(f)
