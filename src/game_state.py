from board import Board, Color


class GameState:

    def __init__(self, board, turn, number=None):
        self.board = board
        self.turn = turn
        self.__number = number

    def __hash__(self):
        return self.number

    def __eq__(self, other):
        return self.number == other.number

    @staticmethod
    def create_initial(size):
        board = Board.create_initial(size)
        return GameState(board, Color.BLACK)

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
        return GameState(self.board.copy(), self.turn, number=self.__number)

    def reset(self):
        self.board = Board.create_initial(self.size)
        self.turn = Color.BLACK
        self.__number = None

    def get_moves(self):
        moves_array = self.board.get_legal_moves(self.turn)
        return tuple(map(tuple, moves_array))

    def make_move(self, move):
        self.board = self.board.make_move(move, self.turn)
        self.__change_turn()
        self.__number = None
        return self

    def is_finished(self):
        return self.board.is_finished()

    def get_winner(self):
        return self.board.get_winner()

    def __get_number(self):
        turn_bit = 1 if self.turn == Color.BLACK else 0
        return self.board.number << 1 | turn_bit

    def __change_turn(self):
        if self.board.has_any_moves(-self.turn):
            self.turn = -self.turn
