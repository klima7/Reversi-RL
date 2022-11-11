from abc import ABC, abstractmethod
import pickle
from pathlib import Path


class Agent(ABC):
    """ Base agent class """

    NAME = None

    def __init__(self):
        self.learn = True

        # aux variables - used to track agent by gameplay class
        self.last_action = None
        self.last_state = None

    # ---------- primary methods to create derived agents ------------

    @abstractmethod
    def get_action(self, state):
        """ Called every time agent should make a decision """
        pass

    def initialize(self):
        """ Called once before all games """
        pass

    def before_gameplay(self):
        """ Called before every game """
        pass

    def after_gameplay(self):
        """ Called after every game """
        pass

    def update(self, state, action, reward, next_state):
        """ Called after opponent move to notify about last action reward """
        pass

    # -------- methods to enable agents to persist data ----------

    def get_data_to_save(self):
        """ Should return data which needs to be persisted """
        return None

    def set_saved_data(self, data):
        """ Should initialize agent with previously persisted data """
        pass

    # ----- methods not intended to use in derived classes -------

    def load_data(self, path):
        """ Initialize agent with data stored given file """
        path = Path(path)
        if path.exists():
            print(f'Loading {self.NAME} agent data...')
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.set_saved_data(data)

    def save_data(self, path):
        """ Saves agent data in given file """
        print(f'Saving {self.NAME} agent data...')
        data_to_save = self.get_data_to_save()
        if data_to_save is None:
            return
        with open(path, 'wb') as f:
            return pickle.dump(data_to_save, f)


class PassiveAgent(Agent, ABC):
    """ Agent which knows everything about environment """

    def __init__(self):
        super().__init__()
        self.env = None


class ActiveAgent(Agent, ABC):
    """ Agent which does not know environment, only possible move in given state """

    def __init__(self):
        super().__init__()
        self.get_possible_actions = None
