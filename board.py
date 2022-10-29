import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from values import PlayerSide


def create_initial(size):
    board = np.zeros((size, size), dtype=np.byte)
    center = size // 2 - 1
    board[center][center] = PlayerSide.ME
    board[center+1][center+1] = PlayerSide.ME
    board[center+1][center] = PlayerSide.OPPONENT
    board[center][center+1] = PlayerSide.OPPONENT
    return board


def inverse(board):
    return 1 - board


def get_positions_to_reverse(board, position):
    directions = [np.array([i, j]) for i in [-1, 0, 1] for j in [-1, 0, 1] if not (i == 0 and j == 0)]
    discs_to_reverse = []

    for direction in directions:
        discs = __get_positions_to_reverse_in_direction(board, position, direction)
        discs_to_reverse.extend(discs)
    return np.array(discs_to_reverse)


def __get_positions_to_reverse_in_direction(board, position, direction):
    discs = []
    position = np.array(position) + direction
    while is_valid_position(board, position):
        value = board[position[0], position[1]]
        if value == PlayerSide.NO_ONE:
            return []
        elif value == PlayerSide.OPPONENT:
            discs.append(np.copy(position))
        elif value == PlayerSide.ME:
            return discs
        position += direction
    return []


def is_valid_position(board, position):
    return np.all(position >= 0) and np.all(position < board.shape[0])


def get_legal_moves(board):
    empty_positions = np.column_stack(np.nonzero(board == 0))
    legal_position = [position for position in empty_positions if len(get_positions_to_reverse(board, position)) > 0]
    return np.array(legal_position)


def is_legal_move(board, position):
    return is_valid_position(board, position) and \
           board[position[0], position[1]] == PlayerSide.NO_ONE and \
           len(get_positions_to_reverse(board, position)) > 0


def get_board_after_move(board, position):
    if not is_legal_move(board, position):
        raise Exception("Illegal move was requested")
    new_board = np.array(board)
    new_board[position[0], position[1]] = PlayerSide.ME
    reverse_positions = get_positions_to_reverse(board, position)
    new_board[reverse_positions[:, 0], reverse_positions[:, 1]] = PlayerSide.ME
    return new_board


def is_finished(board):
    return is_board_full(board) or no_one_has_moves(board)


def is_board_full(board):
    return np.all(board != PlayerSide.NO_ONE)


def no_one_has_moves(board):
    return len(get_legal_moves(board)) == 0 and len(get_legal_moves(inverse(board))) == 0


def get_winner(board):
    return np.sign(np.sum(board))


def plot(board, title=None):
    cmap = ListedColormap(["black", "green", "white"], name='board', N=None)
    plt.matshow(board, cmap=cmap)
    plt.title(title)
    plt.show()
