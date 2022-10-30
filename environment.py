import board_tools as bt


class Environment:

    def __init__(self, game_state, color):
        self.game_state = game_state
        self.color = color

    def get_current_state(self):
        return bt.convert_to_rel_board(self.game_state.board, self.color)

    def get_all_states(self):
        pass  # write yourself

    def get_possible_actions(self, state):
        board = bt.convert_to_abs_board(state, self.color)
        return bt.get_legal_moves(board, self.color)

    def get_next_states(self, state, action):
        board1 = bt.convert_to_abs_board(state, self.color)
        board2 = bt.get_board_after_move(board1, action, self.color)
        opponent_actions = bt.get_legal_moves(board2, -self.color)
        next_states = {}
        for opponent_action in opponent_actions:
            board3 = bt.get_board_after_move(board2, opponent_action, -self.color)
            next_states[board3] = 1 / len(opponent_actions)
        return next_states

    def get_reward(self, state, action, next_state):
        next_board = bt.convert_to_abs_board(state, self.color)
        if bt.is_finished(next_board):
            winner = bt.get_winner(next_board)
            if winner == self.color:
                return 1000
            elif winner == -self.color:
                return -1000
            else:
                return 0
        else:
            return 0
