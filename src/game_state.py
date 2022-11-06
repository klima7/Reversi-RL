from board import Board, Color


class GameState:

    def __init__(self, board, turn, backend):
        self.board = board
        self.turn = turn
        self.backend = backend

    def __hash__(self):
        turn_bit = 1 if self.turn == Color.BLACK else 0
        return self.board.number << 1 | turn_bit

    def __eq__(self, other):
        return self.board.number == other.board.number and self.turn == other.turn

    @staticmethod
    def create_initial(size, backend):
        board = Board.create_initial(size)
        return GameState(board, Color.BLACK, backend)

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
        return GameState(self.board.copy(), self.turn, self.backend)

    def get_moves(self):
        return self.backend.get_moves(self.board, self.turn)

    def make_move(self, move):
        self.board, self.turn = self.backend.make_move(self.board, self.turn, move)
        return self

    def get_winner(self):
        return self.backend.get_winner(self.board)

    def is_finished(self):
        return self.get_winner() is not None
