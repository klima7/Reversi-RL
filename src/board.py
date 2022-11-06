import numpy as np


class Color:
    WHITE = 1
    BLACK = -1
    ANY = 0


class Side:
    ME = 1
    OPPONENT = -1
    ANY = 0


class Board:

    def __init__(self, board):
        self.__data = board

    def __getitem__(self, item):
        return self.__data[item[0], item[1]]

    def __neg__(self):
        return Board(-self.__data)

    def __hash__(self):
        return self.number

    def __eq__(self, other):
        return self.number == other.number

    def __str__(self):
        return str(self.__data)

    @staticmethod
    def create_initial(size):
        board = np.zeros(size, dtype=np.byte)
        center_y, center_x = np.array(size) // 2 - 1
        board[center_y][center_x] = board[center_y + 1][center_x + 1] = Color.WHITE
        board[center_y + 1][center_x] = board[center_y][center_x + 1] = Color.BLACK
        return Board(board)

    @staticmethod
    def create_from_number(number, size):
        values = []
        shifted_number = number
        for _ in range(size[0] * size[1]):
            value = shifted_number & 0b11
            values.insert(0, value-1)
            shifted_number >>= 2
        return Board(np.array(values).astype(np.int_).reshape(size))

    @property
    def number(self):
        number = 0
        tmp = self.__data.flatten() + 1
        for elem in tmp:
            number <<= 2
            number |= int(elem)
        return number

    @property
    def size(self):
        return self.__data.shape

    def copy(self):
        return Board(np.array(self.__data))

    def to_relative(self, my_color):
        return self.copy() if my_color == Color.WHITE else -self.copy()

    def to_absolute(self, my_color):
        return self.copy() if my_color == Color.WHITE else -self.copy()

    def is_valid_position(self, position):
        return 0 <= position[0] < self.size[0] and 0 <= position[1] < self.size[1]

    def get_legal_moves(self, color):
        empty_positions = np.column_stack(np.nonzero(self.__data == Color.ANY))
        legal_position = [position for position in empty_positions if self.__move_reverses_some_discs(position, color)]
        return np.array(legal_position).reshape(-1, 2).astype(np.int_)

    def make_move(self, position, color):
        if not self.__is_legal_move(position, color):               # TODO: Remove this check when stable to speed up
            raise Exception('Tried to perform illegal move')
        self.__data[position[0], position[1]] = color
        reverse_positions = self.__get_positions_to_reverse(position, color)
        self.__data[reverse_positions[:, 0], reverse_positions[:, 1]] = color
        return self

    def is_finished(self):
        return self.is_full() or self.no_one_has_moves()

    def get_winner(self):
        return np.sign(np.sum(self.__data))

    def is_full(self):
        return np.all(self.__data != Color.ANY)

    def no_one_has_moves(self):
        return not self.has_any_moves(Color.WHITE) and not self.has_any_moves(Color.BLACK)

    def has_any_moves(self, color):
        return len(self.get_legal_moves(color)) > 0

    def __is_legal_move(self, position, color):
        return self.is_valid_position(position) and \
               self.__data[position[0], position[1]] == Side.ANY and \
               self.__move_reverses_some_discs(position, color)

    def __get_positions_to_reverse(self, position, color):
        directions = [np.array([i, j]) for i in [-1, 0, 1] for j in [-1, 0, 1] if not (i == 0 and j == 0)]
        discs_to_reverse = []

        for direction in directions:
            discs = self.__get_positions_to_reverse_in_direction(position, color, direction)
            discs_to_reverse.extend(discs)

        return np.array(discs_to_reverse).reshape(-1, 2).astype(np.int_)

    def __get_positions_to_reverse_in_direction(self, position, color, direction):
        discs = []
        position = np.array(position) + direction
        while self.is_valid_position(position):
            value = self.__data[position[0], position[1]]
            if value == 0:
                return []
            elif value == color:
                return discs
            else:
                discs.append(np.copy(position))
            position += direction
        return []

    def __move_reverses_some_discs(self, position, color):
        return len(self.__get_positions_to_reverse(position, color)) > 0
