from abc import ABC, abstractmethod
import _pickle as pickle
from pathlib import Path


class Agent(ABC):

    NAME = None

    def __init__(self):
        self._learn = True

    def get_data_to_save(self):
        return None

    def set_saved_data(self, data):
        pass

    def load_data(self, path):
        path = Path(path)
        if path.exists():
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.set_saved_data(data)

    def save_data(self, path):
        data_to_save = self.get_data_to_save()
        if data_to_save is None:
            return
        with open(path, 'wb') as f:
            return pickle.dump(data_to_save, f)

    def set_learn(self, learn):
        self._learn = learn


class PassiveAgent(Agent):

    def __init__(self):
        super().__init__()
        self.env = None

    def initialize(self):
        pass

    @abstractmethod
    def get_action(self, state):
        pass


class ActiveAgent(Agent):

    def __init__(self):
        super().__init__()
        self.get_possible_actions = None

        self._last_action = None
        self._last_state = None

    @abstractmethod
    def get_action(self, state):
        pass

    def update(self, state, action, reward, next_state):
        pass

    def reset(self):
        pass
