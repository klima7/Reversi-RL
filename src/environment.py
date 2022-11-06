from board import Board, Side
from game_state import GameState


class Environment:

    WIN_REWARD = 1000
    LOST_REWARD = -1000
    DRAW_REWARD = 0

    def __init__(self, size, backend):
        self.__size = size
        self.__backend = backend

    def get_all_states(self):
        return self.__backend.get_all_possible_boards_numbers()

    def get_possible_actions(self, state):
        game_state = self.__cvt_state_to_game_state(state)
        return game_state.get_moves()

    def get_next_states(self, state, action):
        game_state = self.__cvt_state_to_game_state(state)
        game_state.make_move(action)

        next_states = set()
        game_states = {game_state.copy()}

        while game_states:
            game_state = game_states.pop()
            if game_state.turn == Side.ME or game_state.is_finished():
                next_state = self.cvt_board_to_state(game_state.board)
                next_states.add(next_state)
            elif game_state.turn == Side.OPPONENT:
                for move in game_state.get_moves():
                    game_states.add(game_state.copy().make_move(move))

        probability = 1 / len(next_states)
        return {next_state: probability for next_state in next_states}

    def get_reward(self, state, action, next_state):
        game_state = self.__cvt_state_to_game_state(next_state)
        winner = game_state.get_winner()
        if winner == Side.ME:
            return self.WIN_REWARD
        elif winner == Side.OPPONENT:
            return self.LOST_REWARD
        elif winner == Side.ANY:
            return self.DRAW_REWARD
        return 0

    def cvt_board_to_state(self, board):
        return board.number

    def cvt_state_to_board(self, state):
        return Board.create_from_number(state, self.__size)

    def __cvt_state_to_game_state(self, state):
        board = self.cvt_state_to_board(state)
        return GameState(board, Side.ME, self.__backend)
