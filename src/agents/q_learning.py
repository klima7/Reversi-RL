from collections import defaultdict
import random

from . import ActiveAgent, agent


@agent
class SarsaAgent(ActiveAgent):

    NAME = 'sarsa'
    DEFAULT_ALPHA = 0.2
    DEFAULT_EPSILON = 0.25
    DEFAULT_DISCOUNT = 0.99

    def __init__(self, alpha=DEFAULT_ALPHA, epsilon=DEFAULT_EPSILON, discount=DEFAULT_DISCOUNT):
        super().__init__()
        self.__base_alpha = alpha
        self.__base_epsilon = epsilon
        self.__discount = discount
        self.__qvalues = defaultdict(_default_dict_factory)
        self.__planned_action = None

    # ------- aux stuff ------

    @property
    def __alpha(self):
        return self.__base_alpha if self.learn else 0

    @property
    def __epsilon(self):
        return self.__base_epsilon if self.learn else 0

    def __get_qvalue(self, state, action):
        return self.__qvalues[state][action]

    def __set_qvalue(self, state, action, value):
        self.__qvalues[state][action] = value

    def get_data_to_save(self):
        return self.__qvalues

    def set_saved_data(self, data):
        self.__qvalues = data

    def reset(self):
        self.__planned_action = None

    # ------- main stuff ------

    def get_action(self, state):
        if self.__planned_action is None:
            return self.__get_new_action(state)
        else:
            return self.__planned_action

    def update(self, state, action, reward, next_state):
        self.__planned_action = self.__get_new_action(next_state)

        expr = reward + self.__discount * self.__get_value(next_state)
        new_qvalue = (1-self.__alpha) * self.__get_qvalue(state, action) + self.__alpha * expr
        self.__set_qvalue(state, action, new_qvalue)

    def __get_new_action(self, state):
        possible_actions = self.get_possible_actions(state)

        if len(possible_actions) == 0:
            return None

        should_random = random.random() < self.__epsilon

        if should_random:
            return random.choice(possible_actions)
        else:
            return self.__get_best_action(state)

    def __get_value(self, state):
        possible_actions = self.get_possible_actions(state)

        if len(possible_actions) == 0:
            return 0.0

        return max([self.__get_qvalue(state, action) for action in possible_actions])

    def __get_best_action(self, state):
        possible_actions = self.get_possible_actions(state)

        if len(possible_actions) == 0:
            return None

        qvalues = [self.__get_qvalue(state, action) for action in possible_actions]
        best_qvalue = max(qvalues)
        best_actions = [action for action, qvalue in zip(possible_actions, qvalues) if qvalue == best_qvalue]
        best_action = random.choice(best_actions)

        return best_action


# must be standard function, not lambda, to allow pickling
def _default_dict_factory():
    return defaultdict(_zero_factory)


# must be standard function, not lambda, to allow pickling
def _zero_factory():
    return 0
