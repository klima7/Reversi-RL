from copy import deepcopy
from pathlib import Path
import pickle

import board as board
from board import Color, Side


class Environment:

    def __init__(self, game_state, color):
        self.__game_state = game_state
        self.__color = color

        self.__generate_transitions_if_needed()
        self.__transitions = self.__load_transitions()

    def get_current_state(self):
        b = self.__game_state.board
        rel_b = board.convert_to_rel_board(b, self.__color)
        return board.convert_to_number(rel_b)

    def get_all_states(self):
        return list(self.__transitions.keys())

    def get_possible_actions(self, state):
        return list(self.__transitions[state].keys())

    def get_next_states(self, state, action):
        tmp_state = self.__transitions[state][action][1]
        return map(lambda s: s[1], self.__transitions[tmp_state].values())

    def perform_action(self, action):
        if self.__color != self.__game_state.turn_color:
            raise Exception('Player tried to perform action outside of his turn')
        move = divmod(action, self.__game_state.size[1])
        self.__game_state.make_move(move)

    def get_reward(self, state, action, next_state):
        next_board = board.convert_to_abs_board(state, self.__color)
        if board.is_finished(next_board):
            winner = board.get_winner(next_board)
            if winner == self.__color:
                return 1000
            elif winner == -self.__color:
                return -1000
            else:
                return 0
        else:
            return 0

    def __file_location(self):
        root_path = Path(__file__).parent.parent
        filename = f'{self.__game_state.size[0]}x{self.__game_state.size[1]}_env.pickle'
        return root_path / 'res' / filename

    def __generate_transitions_if_needed(self):
        path = self.__file_location()
        if not path.exists():
            transitions = self.__generate_transitions()
            with open(path, 'wb') as f:
                return pickle.dump(transitions, f)

    def __load_transitions(self):
        path = self.__file_location()
        with open(path, 'rb') as f:
            return pickle.load(f)

    def __generate_transitions(self):
        print('Generating environment data...')
        data = {}
        for rel_board in self.__generate_all_rel_boards():
            state = board.convert_to_number(rel_board)
            state_dict = {}
            moves = board.get_legal_moves(rel_board, Side.ME)
            actions = moves[:, 0] * rel_board.shape[1] + moves[:, 1]
            for move, action in zip(moves, actions):
                me_next_state = board.convert_to_number(board.get_board_after_move(rel_board, move, Side.ME))
                op_next_state = board.convert_to_number(board.get_board_after_move(rel_board, move, Side.OPPONENT))
                state_dict[action] = (me_next_state, op_next_state)
            data[state] = state_dict
        return data

    def __generate_all_rel_boards(self):
        rel_boards = []
        rel_boards_numbers = set()

        for abs_board in self.__generate_all_abs_boards():
            for color in [Color.WHITE, Color.BLACK]:
                rel_board = board.convert_to_rel_board(abs_board, color)
                rel_board_number = board.convert_to_number(rel_board)
                if rel_board_number in rel_boards_numbers:
                    continue
                rel_boards_numbers.add(rel_board_number)
                rel_boards.append(rel_board)

        return rel_boards

    def __generate_all_abs_boards(self):
        abs_boards = []
        game_states = [deepcopy(self.__game_state)]
        game_states_numbers = set()

        while game_states:
            game_state = game_states.pop(0)

            game_state_number = game_state.to_number()
            if game_state_number in game_states_numbers:
                continue

            game_states_numbers.add(game_state_number)
            abs_boards.append(game_state.board)

            legal_moves = game_state.get_moves()
            for legal_move in legal_moves:
                next_game_state = deepcopy(game_state)
                next_game_state.make_move(legal_move)
                game_states.append(next_game_state)

        return abs_boards
