import board_tools as bt

from values import Color


class GameState:

    def __init__(self, size):
        self.size = size
        self.board = bt.create_abs_board(size)
        self.turn_color = Color.BLACK

    def get_state(self):
        pass

    def perform_action(self, position):
        pass

    def is_finished(self):
        pass

    def get_winner(self):
        pass
