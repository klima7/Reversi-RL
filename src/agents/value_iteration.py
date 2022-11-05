import numpy as np

from . import Agent, agent
from environment import Environment


@agent
class ValueIterAgent(Agent):

    NAME = 'value_iter'

    def initialize(self, env):
        if not self.data:
            print('Learning strategy...')
            self.data, _ = self.__value_iteration(env, 0.95, 1e-4)

    def get_action(self, state, env: Environment):
        return self.data[state]

    @staticmethod
    def __value_iteration(env, gamma, theta):
        V = dict()
        policy = dict()

        for current_state in env.get_all_states():
            V[current_state] = 0
            policy[current_state] = 0

        while True:
            V_prev = dict(V)
            for s in env.get_all_states():
                actions_values = []
                for a in env.get_possible_actions(s):
                    action_value = 0
                    for s_prim, p in env.get_next_states(s, a).items():
                        r = env.get_reward(s, a, s_prim)
                        action_value += p * (r + gamma * V[s_prim])
                    actions_values.append(action_value)

                if actions_values:
                    V[s] = max(actions_values)

            if ValueIterAgent.__should_stop(V, V_prev, theta):
                break

        ValueIterAgent.__policy_improvement(env, policy, V, gamma)

        return policy, V

    @staticmethod
    def __should_stop(V1, V2, theta):
        v1_values = np.array(list(V1.values()))
        v2_values = np.array(list(V2.values()))
        diff = np.abs(v1_values - v2_values)
        min_diff = np.max(diff)
        return min_diff < theta

    @staticmethod
    def __policy_improvement(mdp, policy, value_function, gamma):
        policy_stable = True

        for s in mdp.get_all_states():
            actions = mdp.get_possible_actions(s)

            if len(actions) == 0:
                continue

            actions_values = []

            for a in actions:
                action_value = 0
                for s_prim, p in mdp.get_next_states(s, a).items():
                    r = mdp.get_reward(s, a, s_prim)
                    action_value += p * (r + gamma * value_function[s_prim])
                actions_values.append(action_value)

            best_action_index = np.argmax(actions_values)
            best_action = actions[best_action_index]

            if policy[s] != best_action:
                policy[s] = best_action
                policy_stable = False

        return policy_stable
