import board_tools as bt


class Environment:

    def __init__(self, size):
        pass

    def get_all_states(self):
        pass    # write yourself

    def get_possible_actions(self, state):
        return bt.get_legal_moves(state)

    def get_next_states(self, state, action):
        pass

    def get_reward(self, state, action, next_state):
        pass    # write yourself
