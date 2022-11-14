from collections import defaultdict
import random

from . import ActiveAgent, agent


@agent
class DoubleQLearningAgent(ActiveAgent):

    NAME = 'dq_learning'
    DEFAULT_ALPHA = 0.2
    DEFAULT_EPSILON = 0.25
    DEFAULT_DISCOUNT = 0.99

    def __init__(self, alpha=DEFAULT_ALPHA, epsilon=DEFAULT_EPSILON, discount=DEFAULT_DISCOUNT):
        super().__init__()
        self.__base_alpha = alpha
        self.__base_epsilon = epsilon
        self.__discount = discount
        self.__qvalues1 = defaultdict(_default_dict_factory)
        self.__qvalues2 = defaultdict(_default_dict_factory)

    # ------- aux stuff ------

    @property
    def __alpha(self):
        return self.__base_alpha if self.learn else 0

    @property
    def __epsilon(self):
        return self.__base_epsilon if self.learn else 0

    def __get_qvalue(self, state, action):
        return self.__qvalues1[state][action] + self.__qvalues2[state][action]

    def get_data_to_save(self):
        return [self.__qvalues1, self.__qvalues2]

    def set_saved_data(self, data):
        self.__qvalues1 = data[0]
        self.__qvalues2 = data[1]

    # ------- main stuff ------

    def get_action(self, state):
        possible_actions = self.get_possible_actions(state)

        if len(possible_actions) == 0:
            return None

        should_random = random.random() < self.__epsilon

        if should_random:
            return random.choice(possible_actions)
        else:
            return self.__get_best_action(state)

    def update(self, state, action, reward, next_state):
        qa, qb = random.choice([
            [self.__qvalues1, self.__qvalues2],
            [self.__qvalues2, self.__qvalues1]
        ])

        expr = reward + self.__discount * self.__get_value(qa, qb, next_state)
        qa[state][action] = (1 - self.__alpha) * qa[state][action] + self.__alpha * expr

    def __get_value(self, qa, qb, state):
        possible_actions = self.get_possible_actions(state)

        if len(possible_actions) == 0:
            return 0.0

        actions_values = [qa[state][action] for action in possible_actions]
        max_action_value = max(actions_values)
        best_actions = [action for action, value in zip(possible_actions, actions_values) if value == max_action_value]
        best_action = random.choice(best_actions)

        return qb[state][best_action]

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
