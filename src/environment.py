from abc import ABC, abstractmethod
from copy import deepcopy
from pathlib import Path
import pickle

import board as board_tools
from board import Side
from game_state import GameState


class Environment(ABC):

    WIN_REWARD = 1000
    LOST_REWARD = -1000
    DRAW_REWARD = 0

    def __init__(self, game_state, color):
        self._game_state = game_state
        self._color = color

    def get_current_state(self):
        rel_board = board_tools.convert_to_rel_board(self._game_state.board, self._color)
        return board_tools.convert_to_number(rel_board)

    def perform_action(self, action):
        if self._color != self._game_state.turn_color:
            raise Exception('Player tried to perform action outside of his turn')
        move = self._cvt_action_to_move(action)
        self._game_state.make_move(move)

    @abstractmethod
    def get_all_states(self):
        pass

    @abstractmethod
    def get_possible_actions(self, state):
        pass

    @abstractmethod
    def get_next_states(self, state, action):
        pass

    @abstractmethod
    def get_reward(self, state, action, next_state):
        pass

    def _cvt_move_to_action(self, move):
        return move[0] * self._game_state.size[1] + move[1]

    def _cvt_action_to_move(self, action):
        return divmod(action, self._game_state.size[1])

    def _generate_all_rel_boards(self):
        rel_boards_numbers = set()
        game_states = [deepcopy(self._game_state)]
        game_states_numbers = set()

        while game_states:
            game_state = game_states.pop(0)

            game_state_number = game_state.to_number()
            if game_state_number in game_states_numbers:
                continue
            game_states_numbers.add(game_state_number)

            rel_board = board_tools.convert_to_rel_board(game_state.board, game_state.turn_color)
            rel_board_number = board_tools.convert_to_number(rel_board)
            if rel_board_number not in rel_boards_numbers:
                yield rel_board
                rel_boards_numbers.add(rel_board_number)
            if board_tools.is_finished(rel_board):
                rel_board = board_tools.convert_to_rel_board(game_state.board, -game_state.turn_color)
                yield rel_board
                rel_boards_numbers.add(rel_board_number)

            legal_moves = game_state.get_moves()
            for legal_move in legal_moves:
                next_game_state = deepcopy(game_state)
                next_game_state.make_move(legal_move)
                game_states.append(next_game_state)


class LiveEnvironment(Environment):

    def get_all_states(self):
        for rel_board in self._generate_all_rel_boards():
            yield board_tools.convert_to_number(rel_board)

    def get_possible_actions(self, state):
        board = board_tools.retrieve_from_number(state, self._game_state.size)
        game_state = GameState(board, Side.ME)
        moves = game_state.get_moves()
        actions = tuple(self._cvt_move_to_action(move) for move in moves)
        return actions

    def get_next_states(self, state, action):
        board = board_tools.retrieve_from_number(state, self._game_state.size)
        move = self._cvt_action_to_move(action)

        game_state = GameState(board, Side.ME)
        game_state.make_move(move)

        next_states = set()
        game_states = [deepcopy(game_state)]

        while game_states:
            game_state = game_states.pop()
            if game_state.turn_color == Side.ME or game_state.is_finished():
                next_states.add(board_tools.convert_to_number(game_state.board))
            elif game_state.turn_color == Side.OPPONENT:
                for op_move in game_state.get_moves():
                    possible_game_state = deepcopy(game_state)
                    possible_game_state.make_move(op_move)
                    game_states.append(possible_game_state)

        probability = 1 / len(next_states)
        return {next_state: probability for next_state in next_states}

    def get_reward(self, state, action, next_state):
        next_board = board_tools.retrieve_from_number(next_state, self._game_state.size)
        if board_tools.is_finished(next_board):
            winner = board_tools.get_winner(next_board)
            if winner == Side.ME:
                return self.WIN_REWARD
            elif winner == Side.OPPONENT:
                return self.LOST_REWARD
            elif winner == Side.ANY:
                return self.DRAW_REWARD
        return 0


class PreparedEnvironment(Environment):

    def __init__(self, game_state, color):
        super().__init__(game_state, color)
        self.__file_location = self.__get_file_location()
        self.__generate_data_if_needed()
        self.__data = self.__load_data()

    def get_all_states(self):
        return list(self.__transitions.keys())

    def get_possible_actions(self, state):
        return list(self.__transitions[state].keys())

    def get_next_states(self, state, action):
        op_has_moves, temp_state = self.__transitions[state][action]

        if not op_has_moves:
            return {temp_state: 1.0}
        else:
            next_states = list(map(lambda e: e[1], self.__transitions[temp_state].values()))
            probability = 1 / len(next_states)
            return {next_state: probability for next_state in next_states}

    def get_reward(self, state, action, next_state):
        if next_state in self.__terminal_states[Side.ME]:
            return self.WIN_REWARD
        elif next_state in self.__terminal_states[Side.OPPONENT]:
            return self.LOST_REWARD
        elif next_state in self.__terminal_states[Side.ANY]:
            return self.DRAW_REWARD
        return 0

    @property
    def __transitions(self):
        return self.__data['transitions']

    @property
    def __terminal_states(self):
        return self.__data['terminal_states']

    def __get_file_location(self):
        root_path = Path(__file__).parent.parent
        filename = f'{self._game_state.size[0]}x{self._game_state.size[1]}_env.pickle'
        return root_path / 'res' / filename

    def __generate_data_if_needed(self):
        if not self.__file_location.exists():
            print('Preparing environment...')
            data = self.__generate__data()
            with open(self.__file_location, 'wb') as f:
                pickle.dump(data, f)

    def __load_data(self):
        print('Loading prepared environment...')
        with open(self.__file_location, 'rb') as f:
            return pickle.load(f)

    def __generate__data(self):
        all_rel_boards = list(self._generate_all_rel_boards())
        return {
            'transitions': self.__create_transitions(all_rel_boards),
            'terminal_states': self.__get_terminal_states(all_rel_boards),
        }

    def __create_transitions(self, rel_boards):
        data = {}
        for rel_board in rel_boards:
            state = board_tools.convert_to_number(rel_board)
            state_dict = {}
            moves = board_tools.get_legal_moves(rel_board, Side.ME)
            for move in moves:
                next_rel_board = board_tools.get_board_after_move(rel_board, move, Side.ME)
                op_moves = board_tools.get_legal_moves(next_rel_board, Side.OPPONENT)

                op_has_moves = len(op_moves) > 0
                final_board = -next_rel_board if op_has_moves else next_rel_board

                next_state = board_tools.convert_to_number(final_board)
                state_dict[self._cvt_move_to_action(move)] = (op_has_moves, next_state)

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
            state = board_tools.convert_to_number(rel_board)
            if board_tools.is_finished(rel_board):
                winner = board_tools.get_winner(rel_board)
                terminal_states[winner].add(state)

        return terminal_states
