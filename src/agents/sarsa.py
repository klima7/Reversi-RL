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
        self.__planned_action = None
        self._qvalues = defaultdict(_default_dict_factory)

    # ------- aux stuff ------

    @property
    def _alpha(self):
        return self.__base_alpha if self.learn else 0

    @property
    def _epsilon(self):
        return self.__base_epsilon if self.learn else 0

    def _get_qvalue(self, state, action):
        return self._qvalues[state][action]

    def _set_qvalue(self, state, action, value):
        self._qvalues[state][action] = value

    def get_data_to_save(self):
        return self._qvalues

    def set_saved_data(self, data):
        self._qvalues = data

    # ------- main stuff ------

    def before_gameplay(self):
        self.__planned_action = None

    def get_action(self, state):
        if self.__planned_action is None:
            return self._get_new_action(state)
        else:
            return self.__planned_action

    def update(self, state, action, reward, next_state):
        self.__planned_action = self._get_new_action(next_state)

        expr = reward + self.__discount * self._get_value(next_state)
        new_qvalue = (1 - self._alpha) * self._get_qvalue(state, action) + self._alpha * expr
        self._set_qvalue(state, action, new_qvalue)

    def _get_value(self, state):
        possible_actions = self.get_possible_actions(state)

        if len(possible_actions) == 0:
            return 0.0

        return max([self._get_qvalue(state, action) for action in possible_actions])

    def _get_new_action(self, state):
        possible_actions = self.get_possible_actions(state)

        if len(possible_actions) == 0:
            return None

        should_random = random.random() < self._epsilon

        if should_random:
            return random.choice(possible_actions)
        else:
            return self._get_best_action(state)

    def _get_best_action(self, state):
        possible_actions = self.get_possible_actions(state)

        if len(possible_actions) == 0:
            return None

        qvalues = [self._get_qvalue(state, action) for action in possible_actions]
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
