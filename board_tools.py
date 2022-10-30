import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from values import Side, Color


def create_abs_board(size):
    board = np.zeros((size, size), dtype=np.byte)
    center = size // 2 - 1
    board[center][center] = board[center+1][center+1] = Color.WHITE
    board[center+1][center] = board[center][center+1] = Color.BLACK
    return board


def convert_to_rel_board(abs_board, my_color):
    if my_color == Color.WHITE:
        return np.array(abs_board)
    else:
        return inverted(abs_board)


def convert_to_abs_board(rel_board, my_color):
    if my_color == Color.WHITE:
        return np.array(rel_board)
    else:
        return inverted(rel_board)


def inverted(board):
    return 1 - board


def get_positions_to_reverse(rel_board, position):
    directions = [np.array([i, j]) for i in [-1, 0, 1] for j in [-1, 0, 1] if not (i == 0 and j == 0)]
    discs_to_reverse = []

    for direction in directions:
        discs = get_positions_to_reverse_in_direction(rel_board, position, direction)
        discs_to_reverse.extend(discs)
    return np.array(discs_to_reverse)


def get_positions_to_reverse_in_direction(rel_board, position, direction):
    discs = []
    position = np.array(position) + direction
    while is_valid_position(rel_board, position):
        value = rel_board[position[0], position[1]]
        if value == Side.ANY:
            return []
        elif value == Side.OPPONENT:
            discs.append(np.copy(position))
        elif value == Side.ME:
            return discs
        position += direction
    return []


def is_valid_position(any_board, position):
    return np.all(position >= 0) and np.all(position < any_board.shape[0])


def get_legal_moves(rel_board):
    empty_positions = np.column_stack(np.nonzero(rel_board == 0))
    legal_position = [position for position in empty_positions if len(get_positions_to_reverse(rel_board, position)) > 0]
    return np.array(legal_position)


def is_legal_move(rel_board, position):
    return is_valid_position(rel_board, position) and \
           rel_board[position[0], position[1]] == Side.ANY and \
           len(get_positions_to_reverse(rel_board, position)) > 0


def get_board_after_move(rel_board, position):
    if not is_legal_move(rel_board, position):
        raise Exception("Illegal move was requested")
    new_rel_board = np.array(rel_board)
    new_rel_board[position[0], position[1]] = Side.ME
    reverse_positions = get_positions_to_reverse(rel_board, position)
    new_rel_board[reverse_positions[:, 0], reverse_positions[:, 1]] = Side.ME
    return new_rel_board


def is_finished(rel_board):
    return is_board_full(rel_board) or no_one_has_moves(rel_board)


def is_board_full(any_board):
    return np.all(any_board != Side.ANY)


def no_one_has_moves(rel_board):
    return len(get_legal_moves(rel_board)) == 0 and len(get_legal_moves(inverted(rel_board))) == 0


def get_winner(rel_board):
    return np.sign(np.sum(rel_board))


def plot(abs_board, title=None):
    cmap = ListedColormap(["black", "green", "white"], name='board', N=None)
    plt.matshow(abs_board, cmap=cmap)
    plt.title(title)
    plt.show()
