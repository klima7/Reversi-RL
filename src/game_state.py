from board import Board, Color


class GameState:

    def __init__(self, board, turn, backend):
        self.board = board
        self.turn = turn
        self.__backend = backend

    def __hash__(self):
        return self.number

    def __eq__(self, other):
        return self.number == other.number

    @staticmethod
    def create_initial(size, backend):
        board = Board.create_initial(size)
        return GameState(board, Color.BLACK, backend)

    @staticmethod
    def create_from_number(size, number, backend):
        turn_bit = number & 1
        board_number = number >> 1
        board = Board.create_from_number(board_number, size)
        turn = Color.BLACK if turn_bit == 1 else Color.WHITE
        return GameState(board, turn, backend)

    @property
    def number(self):
        turn_bit = 1 if self.turn == Color.BLACK else 0
        return self.board.number << 1 | turn_bit

    @property
    def size(self):
        return self.board.size

    @property
    def board_view(self):
        return self.board.to_relative(self.turn)

    @property
    def opposite_board_view(self):
        return self.board.to_relative(-self.turn)

    def copy(self):
        return GameState(self.board.copy(), self.turn, self.__backend)

    def get_moves(self):
        return self.__backend.get_moves(self.board, self.turn)

    def make_move(self, move):
        self.board, self.turn = self.__backend.make_move(self.board, self.turn, move)
        return self

    def get_winner(self):
        return self.__backend.get_winner(self.board)

    def is_finished(self):
        return self.get_winner() is not None
