from collections import defaultdict
import random

from . import ActiveAgent, agent


@agent
class SarsaLambdaAgent(ActiveAgent):

    NAME = 'sarsa_lambda'
    DEFAULT_ALPHA = 0.2
    DEFAULT_EPSILON = 0.25
    DEFAULT_DISCOUNT = 0.99
    DEFAULT_LAMBDA = 0.5

    def __init__(
            self,
            alpha=DEFAULT_ALPHA,
            epsilon=DEFAULT_EPSILON,
            discount=DEFAULT_DISCOUNT,
            lambda_value=DEFAULT_LAMBDA
    ):
        super().__init__()
        self.__base_alpha = alpha
        self.__base_epsilon = epsilon
        self.__discount = discount
        self.__lambda_value = lambda_value

        self._qvalues = defaultdict(_default_dict_factory)
        self._evalues = defaultdict(_default_dict_factory)

        self.__planned_action = None
        self.__visited_state_actions = []

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

    def _get_evalue(self, state, action):
        return self._evalues[state][action]

    def _set_evalue(self, state, action, value):
        self._evalues[state][action] = value

    def get_data_to_save(self):
        return self._qvalues

    def set_saved_data(self, data):
        self._qvalues = data

    # ------- main stuff ------

    def before_gameplay(self):
        self._evalues = defaultdict(_default_dict_factory)
        self.__planned_action = None
        self.__visited_state_actions = []

    def get_action(self, state):
        if self.__planned_action is None:
            return self._get_new_action(state)
        else:
            return self.__planned_action

    def update(self, state, action, reward, next_state):
        self.__planned_action = self._get_new_action(next_state)

        delta = reward + self.__discount * self._get_qvalue(next_state, self.__planned_action) - self._get_qvalue(state, action)
        self._update_current_state_action_trace(state, action)
        self._update_past_state_actions(delta)

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

    def _update_current_state_action_trace(self, state, action):
        current_value = self._get_evalue(state, action)
        new_value = current_value + 1
        self._set_evalue(state, action, new_value)
        self.__visited_state_actions.append((state, action))

    def _update_past_state_actions(self, delta):
        for state, action in self.__visited_state_actions:
            e_value = self._get_evalue(state, action)
            q_value = self._get_qvalue(state, action)
            new_qvalue = q_value + self._alpha * delta * e_value
            new_evalue = self.__discount * self._alpha * e_value

            self._set_qvalue(state, action, new_qvalue)
            self._set_evalue(state, action, new_evalue)


# must be standard function, not lambda, to allow pickling
def _default_dict_factory():
    return defaultdict(_zero_factory)


# must be standard function, not lambda, to allow pickling
def _zero_factory():
    return 0
