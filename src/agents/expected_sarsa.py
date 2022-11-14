from . import agent, SarsaAgent


@agent
class ExpectedSarsaAgent(SarsaAgent):

    NAME = 'exp_sarsa'
    DEFAULT_ALPHA = 0.2
    DEFAULT_EPSILON = 0.25
    DEFAULT_DISCOUNT = 0.99

    def __init__(self, alpha=DEFAULT_ALPHA, epsilon=DEFAULT_EPSILON, discount=DEFAULT_DISCOUNT):
        super().__init__(alpha, epsilon, discount)

    def _get_value(self, state):
        possible_actions = self.get_possible_actions(state)

        if len(possible_actions) == 0:
            return 0.0

        value = 0
        for action in possible_actions:
            prob = self.__get_action_prob_following_strategy(state, action)
            q = self._get_qvalue(state, action)
            value += prob * q

        return value

    def __get_action_prob_following_strategy(self, state, action):
        possible_actions = self.get_possible_actions(state)
        best_action = self._get_best_action(state)
        if action == best_action:
            return 1 - self._epsilon + self._epsilon / len(possible_actions)
        else:
            return self._epsilon / len(possible_actions)
