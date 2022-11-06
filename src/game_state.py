from board import Board, Color


class GameState:

    def __init__(self, board, turn, backend, number=None):
        self.board = board
        self.turn = turn
        self.backend = backend
        self.__number = number

    def __hash__(self):
        return self.number

    def __eq__(self, other):
        return self.number == other.number

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

    @property
    def number(self):
        if self.__number is None:
            self.__number = self.__get_number()
        return self.__number

    def copy(self):
        return GameState(self.board.copy(), self.turn, self.backend, self.__number)

    def reset(self):
        self.board = Board.create_initial(self.size)
        self.turn = Color.BLACK
        self.__number = None

    def get_moves(self):
        return self.backend.get_moves(self.board, self.turn)

    def make_move(self, move):
        self.board, self.turn = self.backend.make_move(self.board, self.turn, move)
        self.__number = None
        return self

    def is_finished(self):
        return self.board.is_finished()

    def get_winner(self):
        return self.board.get_winner()

    def __get_number(self):
        turn_bit = 1 if self.turn == Color.BLACK else 0
        return self.board.number << 1 | turn_bit
