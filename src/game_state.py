import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import board
from board import Color


class GameState:

    def __init__(self, size):
        self.size = size
        self.board = board.create_board(size)
        self.turn_color = Color.BLACK

        # aux
        self.last_move = None

    def __hash__(self):
        return self.to_number()

    def reset(self):
        self.board = board.create_board(self.size)
        self.turn_color = Color.BLACK

    def get_moves(self):
        moves_array = board.get_legal_moves(self.board, self.turn_color)
        moves_tuple = tuple(map(tuple, moves_array))
        return moves_tuple

    def make_move(self, move):
        legal_moves = board.get_legal_moves(self.board, self.turn_color)
        if move not in legal_moves:
            raise Exception('Illegal move was requested')

        self.board = board.get_board_after_move(self.board, move, self.turn_color)
        self.last_move = move
        self.__change_turn()

    def is_finished(self):
        return board.is_finished(self.board)

    def get_winner(self):
        return board.get_winner(self.board)

    def __change_turn(self):
        if len(board.get_legal_moves(self.board, -self.turn_color)) > 0:
            self.turn_color = -self.turn_color

    def plot(self, title=None):
        cmap = ListedColormap(["black", "green", "white"], name='board', N=None)
        plt.matshow(self.board, cmap=cmap)
        plt.title(title)
        plt.show()

    def to_number(self):
        board_number = board.convert_to_number(self.board)
        turn_bit = 1 if self.turn_color == Color.BLACK else 0
        return board_number << 1 | turn_bit
