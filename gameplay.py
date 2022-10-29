from game_state import GameState
from environment import Environment

from values import Color


class Gameplay:

    def __init__(self, size, player_white, player_black):
        self.game_state = GameState(size)
        self.environment = Environment(size)
        self.player_white = player_white
        self.player_black = player_black

    def play(self):
        while not self.game_state.is_finished():
            player = self.player_white if self.game_state.turn_color == Color.WHITE else self.player_black
            state = self.game_state.get_state()
            action = player.take_action(self.environment, state)
            self.game_state.perform_action(action)

        return self.game_state.get_winner()
