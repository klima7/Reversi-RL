import board_tools as bt

from values import Color, Side


class GameState:

    def __init__(self, size):
        self.size = size
        self.board = bt.create_abs_board(size)
        self.turn_color = Color.BLACK

    def get_state(self):
        return bt.convert_to_rel_board(self.board, self.turn_color)

    def perform_action(self, position):
        rel_board = bt.convert_to_rel_board(self.board, self.turn_color)
        new_rel_board = bt.get_board_after_move(rel_board, position)
        self.board = bt.convert_to_abs_board(new_rel_board, self.turn_color)
        self.turn_color = 1 - self.turn_color

    def is_finished(self):
        return bt.is_finished(self.board)

    def get_winner(self):
        rel_board = bt.convert_to_rel_board(self.board, Color.WHITE)
        winner = bt.get_winner(rel_board)
        if winner == Side.ME:
            return Color.WHITE
        elif winner == Side.OPPONENT:
            return Color.BLACK
        else:
            return Color.ANY
