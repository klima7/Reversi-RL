import board_tools as bt

from values import Side


class Environment:

    def __init__(self, size):
        pass

    def get_all_states(self):
        pass  # write yourself

    def get_possible_actions(self, state):
        return bt.get_legal_moves(state)

    def get_next_states(self, state, action):
        base_state = bt.inverted(bt.get_board_after_move(state, action))
        opponent_actions = bt.get_legal_moves(base_state)
        next_states = {}
        for opponent_action in opponent_actions:
            next_state = bt.inverted(bt.get_board_after_move(base_state, opponent_action))
            next_states[next_state] = 1 / len(opponent_actions)
        return next_states

    def get_reward(self, state, action, next_state):
        if bt.is_finished(next_state):
            winner = bt.get_winner(next_state)
            if winner == Side.ME:
                return 1000
            elif winner == Side.OPPONENT:
                return -1000
            else:
                return 0
        else:
            return 0
