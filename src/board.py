import numpy as np


class Color:
    WHITE = 1
    BLACK = -1
    ANY = 0


class Side:
    ME = 1
    OPPONENT = -1
    ANY = 0


def create_board(size):
    board = np.zeros(size, dtype=np.byte)
    center_y, center_x = np.array(size) // 2 - 1
    board[center_y][center_x] = board[center_y+1][center_x+1] = Color.WHITE
    board[center_y+1][center_x] = board[center_y][center_x+1] = Color.BLACK
    return board


def convert_to_rel_board(abs_board, my_color):
    if my_color == Color.WHITE:
        return np.array(abs_board)
    else:
        return -abs_board


def convert_to_abs_board(rel_board, my_color):
    if my_color == Color.WHITE:
        return np.array(rel_board)
    else:
        return -rel_board


def convert_to_number(board):
    number = 0
    tmp = board.flatten() + 1
    for elem in tmp:
        number <<= 2
        number |= int(elem)
    return number


def get_positions_to_reverse(board, position, color):
    directions = [np.array([i, j]) for i in [-1, 0, 1] for j in [-1, 0, 1] if not (i == 0 and j == 0)]
    discs_to_reverse = []

    for direction in directions:
        discs = get_positions_to_reverse_in_direction(board, position, color, direction)
        discs_to_reverse.extend(discs)

    return np.array(discs_to_reverse).reshape(-1, 2).astype(np.int_)


def get_positions_to_reverse_in_direction(board, position, color, direction):
    discs = []
    position = np.array(position) + direction
    while is_valid_position(board, position):
        value = board[position[0], position[1]]
        if value == 0:
            return []
        elif value == color:
            return discs
        else:
            discs.append(np.copy(position))
        position += direction
    return []


def is_valid_position(board, position):
    return 0 <= position[0] < board.shape[0] and 0 <= position[1] < board.shape[1]


def get_legal_moves(board, color):
    empty_positions = np.column_stack(np.nonzero(board == Color.ANY))
    legal_position = [position for position in empty_positions if len(get_positions_to_reverse(board, position, color)) > 0]
    return np.array(legal_position).reshape(-1, 2).astype(np.int_)


def is_legal_move(board, position, color):
    return is_valid_position(board, position) and \
           board[position[0], position[1]] == Side.ANY and \
           len(get_positions_to_reverse(board, position, color)) > 0


def get_board_after_move(board, position, color):
    if not is_legal_move(board, position, color):
        raise Exception('Tried to perform illegal move')
    new_board = np.array(board)
    new_board[position[0], position[1]] = color
    reverse_positions = get_positions_to_reverse(new_board, position, color)
    new_board[reverse_positions[:, 0], reverse_positions[:, 1]] = color
    return new_board


def is_finished(board):
    return is_board_full(board) or no_one_has_moves(board)


def is_board_full(board):
    return np.all(board != Color.ANY)


def no_one_has_moves(board):
    return len(get_legal_moves(board, Color.WHITE)) == 0 and len(get_legal_moves(board, Color.BLACK)) == 0


def get_winner(board):
    return np.sign(np.sum(board))
