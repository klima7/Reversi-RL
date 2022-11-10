from abc import ABC, abstractmethod
import _pickle as pickle
from pathlib import Path


class Agent(ABC):

    NAME = None

    def __init__(self):
        self.learn = True

    def initialize(self):
        pass

    def before_gameplay(self):
        pass

    def after_gameplay(self):
        pass

    @abstractmethod
    def get_action(self, state):
        pass

    def get_data_to_save(self):
        return None

    def set_saved_data(self, data):
        pass

    def load_data(self, path):
        path = Path(path)
        if path.exists():
            print(f'Loading {self.NAME} agent data...')
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.set_saved_data(data)

    def save_data(self, path):
        print(f'Saving {self.NAME} agent data...')
        data_to_save = self.get_data_to_save()
        if data_to_save is None:
            return
        with open(path, 'wb') as f:
            return pickle.dump(data_to_save, f)


class PassiveAgent(Agent, ABC):

    def __init__(self):
        super().__init__()
        self.env = None


class ActiveAgent(Agent, ABC):

    def __init__(self):
        super().__init__()
        self.get_possible_actions = None

        # aux variables for game engine
        self._last_action = None
        self._last_state = None

    def update(self, state, action, reward, next_state):
        pass
