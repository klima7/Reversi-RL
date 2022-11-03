import board as board_tools
from board import Color


class GameState:

    def __init__(self, *args):

        if len(args) == 1:
            self.board = board_tools.create_board(args[0])
            self.turn_color = Color.BLACK

        elif len(args) == 2:
            self.board, self.turn_color = args

        else:
            raise ValueError('Illegal arguments')

        # aux
        self.last_move = None

    def __hash__(self):
        return self.to_number()

    @property
    def size(self):
        return self.board.shape

    def reset(self):
        self.board = board_tools.create_board(self.size)
        self.turn_color = Color.BLACK

    def get_moves(self):
        moves_array = board_tools.get_legal_moves(self.board, self.turn_color)
        moves_tuple = tuple(map(tuple, moves_array))
        return moves_tuple

    def make_move(self, move):
        legal_moves = board_tools.get_legal_moves(self.board, self.turn_color)
        if move not in legal_moves:
            raise Exception('Illegal move was requested')

        self.board = board_tools.get_board_after_move(self.board, move, self.turn_color)
        self.last_move = move
        self.__change_turn()

    def is_finished(self):
        return board_tools.is_finished(self.board)

    def get_winner(self):
        return board_tools.get_winner(self.board)

    def __change_turn(self):
        if len(board_tools.get_legal_moves(self.board, -self.turn_color)) > 0:
            self.turn_color = -self.turn_color

    def to_number(self):
        board_number = board_tools.convert_to_number(self.board)
        turn_bit = 1 if self.turn_color == Color.BLACK else 0
        return board_number << 1 | turn_bit
