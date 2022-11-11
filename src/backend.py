from abc import ABC, abstractmethod
import pickle

from simulation import Simulation
from board import Side, Board


class Backend(ABC):

    def __init__(self, size):
        self._size = size

    @abstractmethod
    def get_all_possible_boards_numbers(self):
        pass

    @abstractmethod
    def get_moves(self, board, turn):
        pass

    @abstractmethod
    def make_move(self, board, turn, move):
        pass

    @abstractmethod
    def get_winner(self, board):
        pass

    def _generate_all_possible_boards(self):
        boards = set()
        simulations = {Simulation.create_initial(self._size, LiveBackend(self._size))}

        while simulations:
            simulation = simulations.pop()

            if simulation in simulations:
                continue

            if simulation.is_finished():
                boards.update([simulation.board_view, simulation.opposite_board_view])
            else:
                boards.add(simulation.board_view)

            for move in simulation.get_moves():
                next_simulation = simulation.copy().make_move(move)
                simulations.add(next_simulation)

        return boards


class LiveBackend(Backend):

    def __init__(self, size):
        super().__init__(size)
        self.__boards_numbers = None

    def get_all_possible_boards_numbers(self):
        if self.__boards_numbers is None:
            self.__boards_numbers = tuple(board.number for board in self._generate_all_possible_boards())
        return self.__boards_numbers

    def get_moves(self, board, turn):
        moves_array = board.get_legal_moves(turn)
        return tuple(map(tuple, moves_array))

    def make_move(self, board, turn, move):
        new_board = board.make_move(move, turn)
        new_turn = -turn if board.has_any_moves(-turn) else turn
        return new_board, new_turn

    def get_winner(self, board):
        if board.is_finished():
            return board.get_winner()
        return None


class PreparedBackend(Backend):

    def __init__(self, size, path):
        super().__init__(size)
        self.__path = path
        self.__data = self.__load_or_prepare_data()
        print(f'Game has {len(self.__data)} possible states')

    def get_all_possible_boards_numbers(self):
        return tuple(self.__data.keys())

    def get_moves(self, board, turn):
        relative_board = board.to_relative(turn)
        return tuple(self.__data[relative_board.number][0].keys())

    def make_move(self, board, turn, move):
        relative_board = board.to_relative(turn)
        is_turn_change, next_relative_board_number = self.__data[relative_board.number][0][move]
        next_board = Board.create_from_number(next_relative_board_number, self._size).to_absolute(turn)
        next_turn = -turn if is_turn_change else turn
        return next_board, next_turn

    def get_winner(self, board):
        number = board.number
        if number not in self.__data:
            return None
        return self.__data[board.number][1]

    def __load_or_prepare_data(self):
        if self.__data_file_exists():
            print('Loading prepared data...')
            return self.__load_data()
        else:
            print('Preparing data...')
            data = self.__prepare_data()
            self.__save_data(data)
            return data

    def __data_file_exists(self):
        return self.__path.exists()

    def __load_data(self):
        with open(self.__path, 'rb') as f:
            return pickle.load(f)

    def __save_data(self, transitions):
        with open(self.__path, 'wb') as f:
            pickle.dump(transitions, f)

    def __prepare_data(self):
        data = {}

        for board in self._generate_all_possible_boards():
            simulation = Simulation(board, Side.ME, LiveBackend(self._size))
            moves = simulation.get_moves()
            moves_dict = {move: self.__get_move_result(simulation, move) for move in moves}
            winner = simulation.get_winner() if simulation.is_finished() else None
            data[board.number] = [moves_dict, winner]

        return data

    @staticmethod
    def __get_move_result(simulation, move):
        next_simulation = simulation.copy().make_move(move)
        is_turn_change = next_simulation.turn == Side.OPPONENT
        next_board = next_simulation.board.to_relative(Side.ME)
        return is_turn_change, next_board.number
