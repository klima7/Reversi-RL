import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import board
from board import Color


class GameState:

    def __init__(self, size):
        self.size = size
        self.board = board.create_board(size)
        self.turn_color = Color.BLACK

    def get_moves(self):
        moves_array = board.get_legal_moves(self.board, self.turn_color)
        moves_tuple = tuple(map(tuple, moves_array))
        return moves_tuple

    def make_move(self, move):
        legal_actions = board.get_legal_moves(self.board, self.turn_color)
        if move not in legal_actions:
            raise Exception('Illegal action was requested')

        self.board = board.get_board_after_move(self.board, move, self.turn_color)
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
