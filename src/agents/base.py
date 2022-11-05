from abc import ABC, abstractmethod
import _pickle as pickle
from pathlib import Path


class Agent(ABC):

    NAME = None

    def __init__(self, size):
        self._size = size
        self._learn = True
        self.__data_path = self.__get_data_path()

    def initialize(self, env):
        pass

    @abstractmethod
    def get_action(self, state, env):
        pass

    def get_data_to_save(self):
        return None

    def set_saved_data(self, data):
        pass

    def load_data(self):
        if self.__data_path.exists():
            with open(self.__data_path, 'rb') as f:
                data = pickle.load(f)
                self.set_saved_data(data)

    def save_data(self):
        data_to_save = self.get_data_to_save()
        if data_to_save is None:
            return
        with open(self.__data_path, 'wb') as f:
            return pickle.dump(data_to_save, f)

    def set_learn(self, learn):
        self._learn = learn

    def __get_data_path(self):
        root_path = Path(__file__).parent.parent.parent
        filename = f'{self._size[0]}x{self._size[1]}_{self.NAME}.pickle'
        return root_path / 'res' / filename
