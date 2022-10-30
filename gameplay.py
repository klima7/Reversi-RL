from abc import ABC, abstractmethod
from multiprocessing.pool import ThreadPool

import pygame

from game_state import GameState
from environment import Environment
from values import Color


class Gameplay(ABC):

    def __init__(self, size, player_white, player_black):
        self.game_state = GameState(size)

        self.player_white = player_white
        self.player_black = player_black

        self.env_white = Environment(self.game_state, Color.WHITE)
        self.env_black = Environment(self.game_state, Color.BLACK)

    @property
    def _player(self):
        return self.player_white if self.game_state.turn_color == Color.WHITE else self.player_black

    @property
    def _env(self):
        return self.env_white if self.game_state.turn_color == Color.WHITE else self.env_black

    @abstractmethod
    def play(self):
        pass


class NoGuiGameplay(Gameplay):
    ...


class GuiGameplay(Gameplay):

    FIELD_SIZE = 100
    DISC_SIZE = 80

    def __init__(self, size, player_white, player_black):
        super().__init__(size, player_white, player_black)

        self.running = True
        self.screen = None
        self.pool = ThreadPool(1)
        self.task = None

    def play(self):
        self.__init_gui()

        while not self.game_state.is_finished() and self.running:
            self.__collect_events()
            self.__update()
            self.__draw_screen()

        self.__dispose_gui()
        return self.game_state.get_winner()

    def __init_gui(self):
        pygame.init()
        self.screen = pygame.display.set_mode([self.game_state.size * self.FIELD_SIZE, self.game_state.size * self.FIELD_SIZE])
        pygame.display.set_caption('Reversi')

    def __dispose_gui(self):
        pygame.quit()
        self.screen = None
        self.clock = None

    def __collect_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def __draw_screen(self):
        self.__draw_board()
        self.__draw_discs()
        pygame.display.flip()

    def __draw_board(self):
        self.screen.fill((0, 128, 0))
        pygame.draw.rect(self.screen, (0, 150, 0), (0, 0, self.game_state.size * self.FIELD_SIZE, self.game_state.size * self.FIELD_SIZE), width=3)
        for i in range(1, self.game_state.size):
            pygame.draw.line(self.screen, (0, 150, 0), (i*self.FIELD_SIZE, 0), (i*self.FIELD_SIZE, self.game_state.size * self.FIELD_SIZE), width=3)
            pygame.draw.line(self.screen, (0, 150, 0), (0, i*self.FIELD_SIZE), (self.game_state.size * self.FIELD_SIZE, i*self.FIELD_SIZE), width=3)

    def __draw_discs(self):
        possible_moves = self.game_state.get_moves()
        disc_center_offset = self.FIELD_SIZE // 2
        for y in range(self.game_state.size):
            for x in range(self.game_state.size):
                disc_color = self.game_state.board[y, x]
                pos = (x * self.FIELD_SIZE + disc_center_offset, y * self.FIELD_SIZE + disc_center_offset)
                if disc_color == Color.ANY and (y, x) in possible_moves:
                    color = [255, 255, 255] if self.game_state.turn_color == Color.WHITE else [0, 0, 0]
                    pygame.draw.circle(self.screen, color, pos, self.DISC_SIZE // 2, width=3)
                elif disc_color != Color.ANY:
                    color = [255, 255, 255] if disc_color == Color.WHITE else [0, 0, 0]
                    pygame.draw.circle(self.screen, color, pos, self.DISC_SIZE // 2)

    def __update(self):
        action = self.__get_action_from_player(self._player)
        if action is not None:
            self.game_state.make_move(action)

    def __get_action_from_player(self, player):
        if player is None:
            return self.__get_action_from_real_player()
        else:
            return self.__get_action_from_artificial_player(player)

    def __get_action_from_artificial_player(self, player):
        if self.task is None:
            self.task = self.pool.apply_async(lambda player, env: player.take_action(env), [player, self._env])

        if self.task.ready():
            action = self.task.get()
            self.task = None
            return action

        return None

    def __get_action_from_real_player(self):
        possible_moves = self.game_state.get_moves()
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            mouse_pos = pygame.mouse.get_pos()
            move_pos = (mouse_pos[1] // self.FIELD_SIZE, mouse_pos[0] // self.FIELD_SIZE)
            if move_pos in possible_moves:
                return move_pos
            return None
        return None
