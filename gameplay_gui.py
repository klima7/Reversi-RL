import pygame
import time

from game_state import GameState
from environment import Environment
from values import Color


class GameplayGui:

    FIELD_SIZE = 100
    DISC_SIZE = 80

    def __init__(self, size, player_white, player_black):
        self.game_state = GameState(size)

        self.player_white = player_white
        self.player_black = player_black

        self.env_white = Environment(self.game_state, Color.WHITE)
        self.env_black = Environment(self.game_state, Color.BLACK)

        self.screen = None

    def play(self):
        self.__init_pygame()
        self.__main_loop()
        pygame.quit()
        return self.game_state.get_winner()

        # while not self.game_state.is_finished():
        #     player = self.player_white if self.game_state.turn_color == Color.WHITE else self.player_black
        #     env = self.env_white if self.game_state.turn_color == Color.WHITE else self.env_black
        #     action = player.take_action(env)
        #     self.game_state.make_move(action)
        #
        # return self.game_state.get_winner()

    def __init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode([self.game_state.size * self.FIELD_SIZE, self.game_state.size * self.FIELD_SIZE])

    def __main_loop(self):
        self.__update_screen()
        time.sleep(1)
        while not self.game_state.is_finished():
            player = self.player_white if self.game_state.turn_color == Color.WHITE else self.player_black
            env = self.env_white if self.game_state.turn_color == Color.WHITE else self.env_black
            action = player.take_action(env)
            self.game_state.make_move(action)
            self.__update_screen()
            time.sleep(1)

    def __update_screen(self):
        self.__draw_board()
        self.__draw_discs()
        pygame.display.flip()

    def __draw_board(self):
        self.screen.fill((0, 128, 0))
        for i in range(1, self.game_state.size):
            pygame.draw.line(self.screen, (0, 0, 0), (i*self.FIELD_SIZE, 0), (i*self.FIELD_SIZE, self.game_state.size * self.FIELD_SIZE), width=3)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i*self.FIELD_SIZE), (self.game_state.size * self.FIELD_SIZE, i*self.FIELD_SIZE), width=3)

    def __draw_discs(self):
        disc_center_offset = self.FIELD_SIZE // 2
        for y in range(self.game_state.size):
            for x in range(self.game_state.size):
                disc_color = self.game_state.board[y, x]
                color = (255, 255, 255) if disc_color == Color.WHITE else (0, 0, 0)
                pos = (x * self.FIELD_SIZE + disc_center_offset, y * self.FIELD_SIZE + disc_center_offset)
                pygame.draw.circle(self.screen, color, pos, self.DISC_SIZE // 2)
