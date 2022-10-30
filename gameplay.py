from game_state import GameState
from environment import Environment
from values import Color


class Gameplay:

    def __init__(self, size, player_white, player_black):
        self.game_state = GameState(size)

        self.player_white = player_white
        self.player_black = player_black

        self.env_white = Environment(self.game_state, Color.WHITE)
        self.env_black = Environment(self.game_state, Color.BLACK)

    def play(self):
        while not self.game_state.is_finished():
            player = self.player_white if self.game_state.turn_color == Color.WHITE else self.player_black
            env = self.env_white if self.game_state.turn_color == Color.WHITE else self.env_black
            action = player.take_action(env)
            self.game_state.make_move(action)

        return self.game_state.get_winner()
