from copy import deepcopy
from pathlib import Path
import pickle

import board as board
from board import Side


class Environment:

    WIN_REWARD = 1000
    LOST_REWARD = -1000
    DRAW_REWARD = 0

    def __init__(self, game_state, color):
        self.__game_state = game_state
        self.__color = color
        self.__file_location = self.__get_file_location()

        self.__generate_data_if_needed()
        self.__data = self.__load_data()

    @property
    def __transitions(self):
        return self.__data['transitions']

    @property
    def __terminal_states(self):
        return self.__data['terminal_states']

    def get_current_state(self):
        rel_board = board.convert_to_rel_board(self.__game_state.board, self.__color)
        return board.convert_to_number(rel_board)

    def get_all_states(self):
        return list(self.__transitions.keys())

    def get_possible_actions(self, state):
        return list(self.__transitions[state].keys())

    def get_next_states(self, temp_state, action):
        op_has_moves, temp_state = self.__transitions[temp_state][action]

        if not op_has_moves:
            return {temp_state: 1.0}
        else:
            next_states = list(map(lambda e: e[1], self.__transitions[temp_state].values()))
            probability = 1 / len(next_states)
            return {next_state: probability for next_state in next_states}

    def perform_action(self, action):
        if self.__color != self.__game_state.turn_color:
            raise Exception('Player tried to perform action outside of his turn')

        move = divmod(action, self.__game_state.size[1])
        self.__game_state.make_move(move)

    def get_reward(self, state, action, next_state):
        if next_state in self.__terminal_states[Side.ME]:
            return self.WIN_REWARD
        elif next_state in self.__terminal_states[Side.OPPONENT]:
            return self.LOST_REWARD
        elif next_state in self.__terminal_states[Side.ANY]:
            return self.DRAW_REWARD
        return 0

    def __cvt_move_to_action(self, move):
        return move[0] * self.__game_state.size[1] + move[1]

    def __cvt_action_to_move(self, action):
        return divmod(action, self.__game_state.size[1])

    def __get_file_location(self):
        root_path = Path(__file__).parent.parent
        filename = f'{self.__game_state.size[0]}x{self.__game_state.size[1]}_env.pickle'
        return root_path / 'res' / filename

    def __generate_data_if_needed(self):
        if not self.__file_location.exists():
            print('Generating environment...')
            data = self.__generate__data()
            with open(self.__file_location, 'wb') as f:
                pickle.dump(data, f)

    def __load_data(self):
        print('Loading environment...')
        with open(self.__file_location, 'rb') as f:
            return pickle.load(f)

    def __generate__data(self):
        all_rel_boards = self.__generate_all_rel_boards()
        return {
            'transitions': self.__create_transitions(all_rel_boards),
            'terminal_states': self.__get_terminal_states(all_rel_boards),
        }

    def __create_transitions(self, rel_boards):
        data = {}
        for rel_board in rel_boards:
            state = board.convert_to_number(rel_board)
            state_dict = {}
            moves = board.get_legal_moves(rel_board, Side.ME)
            for move in moves:
                next_rel_board = board.get_board_after_move(rel_board, move, Side.ME)
                op_moves = board.get_legal_moves(next_rel_board, Side.OPPONENT)

                op_has_moves = len(op_moves) > 0
                final_board = -next_rel_board if op_has_moves else next_rel_board

                next_state = board.convert_to_number(final_board)
                state_dict[self.__cvt_move_to_action(move)] = (op_has_moves, next_state)

            data[state] = state_dict
        return data

    @staticmethod
    def __get_terminal_states(rel_boards):
        terminal_states = {
            Side.ME: set(),
            Side.OPPONENT: set(),
            Side.ANY: set()
        }

        for rel_board in rel_boards:
            state = board.convert_to_number(rel_board)
            if board.is_finished(rel_board):
                winner = board.get_winner(rel_board)
                terminal_states[winner].add(state)

        return terminal_states

    def __generate_all_rel_boards(self):
        rel_boards = []
        rel_boards_numbers = set()

        game_states = [deepcopy(self.__game_state)]
        game_states_numbers = set()

        while game_states:
            game_state = game_states.pop(0)

            game_state_number = game_state.to_number()
            if game_state_number in game_states_numbers:
                continue
            game_states_numbers.add(game_state_number)

            rel_board = board.convert_to_rel_board(game_state.board, game_state.turn_color)
            rel_board_number = board.convert_to_number(rel_board)
            if rel_board_number not in rel_boards_numbers:
                rel_boards.append(rel_board)
                rel_boards_numbers.add(rel_board_number)

            legal_moves = game_state.get_moves()
            for legal_move in legal_moves:
                next_game_state = deepcopy(game_state)
                next_game_state.make_move(legal_move)
                game_states.append(next_game_state)

        return rel_boards
