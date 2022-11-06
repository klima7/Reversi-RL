import time
import signal
from abc import ABC, abstractmethod
from multiprocessing.pool import ThreadPool
from itertools import count

import pygame
from tqdm import tqdm

from game_state import GameState
from environment import Environment
from board import Color
from exceptions import DomainException


class Gameplay(ABC):

    def __init__(self, size, delay, backend):
        self._size = size
        self._delay = delay
        self._backend = backend

        self._game_state = GameState.create_initial(size, backend)
        self._env = Environment(size, backend)

        self._player_black = None
        self._player_white = None

    def set_players(self, player_black, player_white):
        self._player_black = player_black
        self._player_white = player_white

        if self._player_white is not None:
            self._player_white.initialize(self._env)
        if self._player_black is not None:
            self._player_black.initialize(self._env)

    def swap_players(self):
        self._player_black, self._player_white = self._player_white, self._player_black

    @property
    def _current_player(self):
        return self._player_white if self._game_state.turn == Color.WHITE else self._player_black

    @property
    def _current_state(self):
        return self._env.cvt_board_to_state(self._game_state.board_view)

    def _get_winner(self):
        winner_color = self._game_state.get_winner()
        if winner_color == Color.WHITE:
            return self._player_white
        elif winner_color == Color.BLACK:
            return self._player_black
        else:
            return None

    @abstractmethod
    def play(self):
        pass

    def reset(self):
        self._game_state = GameState.create_initial(self._size, self._backend)

    def dispose(self):
        pass


class NoGuiGameplay(Gameplay):

    def set_players(self, player_black, player_white):
        if None in [player_black, player_white]:
            raise DomainException('Human players are not allowed in gameplays without GUI')
        super().set_players(player_black, player_white)

    def play(self):
        while not self._game_state.is_finished():
            action = self._current_player.get_action(self._current_state, self._env)
            self._game_state.make_move(action)

        return self._get_winner()


class GuiGameplay(Gameplay):
    FIELD_SIZE = 100
    DISC_SIZE = 80

    WHITE_COLOR = (255, 255, 255)
    BLACK_COLOR = (0, 0, 0)
    MIDDLE_COLOR = (127, 127, 127)
    BOARD_COLOR = (0, 127, 0)
    LINES_COLOR = (0, 150, 0)
    TEXT_COLOR = (0, 0, 0)

    def __init__(self, size, delay, backend):
        super().__init__(size, delay, backend)

        self.__running = True
        self.__screen = None
        self.__turn_font = None
        self.__winner_font = None
        self.__pool = ThreadPool(1)
        self.__task = None
        self.__last_move = None
        self.__pending_move = None
        self.__pending_move_time = None
        self.__finish_time = None

    def play(self):
        self.__init_gui_if_needed()

        while self.__should_run():
            self.__collect_events()
            self.__update()
            self.__draw_screen()

        return self._get_winner()

    def reset(self):
        super().reset()
        self.__running = True
        self.__last_move = None
        self.__pending_move = None
        self.__pending_move_time = None
        self.__finish_time = None

    def dispose(self):
        self.__dispose_gui()

    def __should_run(self):
        in_progress = not self._game_state.is_finished()
        cooldown_not_elapsed = self.__finish_time is not None and self.__finish_time + self._delay > time.time()
        return (in_progress or cooldown_not_elapsed) and self.__running

    def __init_gui_if_needed(self):
        if not pygame.get_init():
            pygame.init()

            screen_width = self._size[1] * self.FIELD_SIZE
            screen_height = self._size[0] * self.FIELD_SIZE + 40
            self.__screen = pygame.display.set_mode([screen_width, screen_height])
            pygame.display.set_caption(f'Reversi {self._size[0]}x{self._size[1]}')

            self.__turn_font = pygame.font.Font(pygame.font.get_default_font(), 20)
            self.__winner_font = pygame.font.Font(pygame.font.get_default_font(), 40)

    def __dispose_gui(self):
        pygame.quit()
        self.__screen = None

    @staticmethod
    def __get_player_name(player):
        if player is None:
            return 'human'
        else:
            return player.agent_name

    def __collect_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                signal.raise_signal(signal.SIGINT)

    def __draw_screen(self):
        if self._game_state.is_finished():
            self.__draw_finish_screen()
        else:
            self.__draw_standard_screen()

        pygame.display.flip()

    def __draw_standard_screen(self):
        self.__draw_board()
        self.__draw_discs()
        self.__draw_last_move()
        self.__draw_turn()

    def __draw_finish_screen(self):
        winner = self._game_state.get_winner()
        text = self.__get_winner_text(winner)
        color = self.__get_winner_color(winner)

        text_surface = self.__winner_font.render(text, True, self.TEXT_COLOR)
        text_pos = (
            (self.__screen.get_width() - text_surface.get_width()) // 2,
            (self.__screen.get_height() - text_surface.get_height()) // 2
        )
        circle_pos = (self.__screen.get_width() // 2, self.__screen.get_height() // 2 + 60)

        self.__screen.fill(self.BOARD_COLOR)
        self.__screen.blit(text_surface, text_pos)
        pygame.draw.circle(self.__screen, color, circle_pos, 20)

    def __get_winner_text(self, winner):
        if winner == Color.BLACK:
            return self.__get_player_name(self._player_black)
        elif winner == Color.WHITE:
            return self.__get_player_name(self._player_white)
        else:
            return 'draw'

    def __get_winner_color(self, winner):
        if winner == Color.BLACK:
            return self.BLACK_COLOR
        elif winner == Color.WHITE:
            return self.WHITE_COLOR
        else:
            return self.MIDDLE_COLOR

    def __draw_board(self):
        self.__screen.fill(self.BOARD_COLOR)
        pygame.draw.rect(self.__screen, self.LINES_COLOR,
                         (0, 0, self._size[1] * self.FIELD_SIZE, self._size[0] * self.FIELD_SIZE), width=3)
        for y in range(1, self._size[0]):
            pygame.draw.line(self.__screen, self.LINES_COLOR, (0, y * self.FIELD_SIZE),
                             (self._size[1] * self.FIELD_SIZE, y * self.FIELD_SIZE), width=3)
        for x in range(1, self._size[1]):
            pygame.draw.line(self.__screen, self.LINES_COLOR, (x * self.FIELD_SIZE, 0),
                             (x * self.FIELD_SIZE, self._size[0] * self.FIELD_SIZE), width=3)

    def __draw_discs(self):
        possible_moves = self._game_state.get_moves()
        disc_center_offset = self.FIELD_SIZE // 2
        for y in range(self._size[0]):
            for x in range(self._size[1]):
                disc_color = self._game_state.board[y, x]
                pos = (x * self.FIELD_SIZE + disc_center_offset, y * self.FIELD_SIZE + disc_center_offset)
                if disc_color == Color.ANY and (y, x) in possible_moves:
                    color = self.WHITE_COLOR if self._game_state.turn == Color.WHITE else self.BLACK_COLOR
                    pygame.draw.circle(self.__screen, color, pos, self.DISC_SIZE // 2, width=3)
                elif disc_color != Color.ANY:
                    color = self.WHITE_COLOR if disc_color == Color.WHITE else self.BLACK_COLOR
                    pygame.draw.circle(self.__screen, color, pos, self.DISC_SIZE // 2)

    def __draw_last_move(self):
        if self.__last_move is not None:
            y, x = self.__last_move
            x_pos, y_pos = x * self.FIELD_SIZE + self.FIELD_SIZE // 2, y * self.FIELD_SIZE + self.FIELD_SIZE // 2
            pygame.draw.line(self.__screen, (255, 0, 0), (x_pos, 0), (x_pos, self._size[0] * self.FIELD_SIZE), width=2)
            pygame.draw.line(self.__screen, (255, 0, 0), (0, y_pos), (self._size[1] * self.FIELD_SIZE, y_pos), width=2)

    def __draw_turn(self):
        color = self.WHITE_COLOR if self._game_state.turn == Color.WHITE else self.BLACK_COLOR
        name = self.__get_player_name(self._current_player)

        pygame.draw.circle(self.__screen, color, (20, self.__screen.get_height() - 21), 11)
        turn_text = self.__turn_font.render(name, True, self.TEXT_COLOR)
        self.__screen.blit(turn_text, (40, self.__screen.get_height() - 30))

    def __update(self):
        if not self._game_state.is_finished():
            self.__execute_move()
            if self._game_state.is_finished():
                self.__finish_time = time.time()

    def __execute_move(self):
        if self.__pending_move is None:
            action = self.__get_move_from_player(self._current_player)
            if action is not None:
                self.__pending_move = action
                self.__pending_move_time = time.time()
                self.__last_move = action

        elif time.time() - self.__pending_move_time > self._delay:
            self._game_state.make_move(self.__pending_move)
            self.__pending_move = None
            self.__pending_move_time = None

    def __get_move_from_player(self, player):
        if player is None:
            return self.__get_move_from_real_player()
        else:
            return self.__get_move_from_artificial_player(player)

    def __get_move_from_artificial_player(self, player):
        if self.__task is None:
            self.__task = self.__pool.apply_async(GuiGameplay.__thread_to_get_action,
                                                  [player, self._current_state, self._env, self._delay])

        if self.__task.ready():
            action = self.__task.get()
            self.__task = None
            return action

        return None

    @staticmethod
    def __thread_to_get_action(player, state, env, delay):
        start_time = time.time()
        action = player.get_action(state, env)
        duration = time.time() - start_time

        sleep_time = delay - duration
        if sleep_time > 0:
            time.sleep(sleep_time)

        return action

    def __get_move_from_real_player(self):
        possible_moves = self._game_state.get_moves()
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            mouse_pos = pygame.mouse.get_pos()
            move_pos = (mouse_pos[1] // self.FIELD_SIZE, mouse_pos[0] // self.FIELD_SIZE)
            if move_pos in possible_moves:
                return move_pos
            return None
        return None


class Tournament:

    def __init__(self, gameplay, number, player1, player2):
        self.gameplay = gameplay
        self.number = number

        self.player1 = player1
        self.player2 = player2

        self.interrupted = False
        self.results = None

    def play(self):
        self.__setup()
        self.__interruptable_play_loop()
        return self.results

    def __setup(self):
        self.gameplay.set_players(self.player1, self.player2)
        self.results = [0, 0, 0]

    def __interruptable_play_loop(self):
        signal.signal(signal.SIGINT, self.__interrupt_handler)
        self.__play_loop()
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    def __interrupt_handler(self, _sigint, _frame):
        self.interrupted = True

    def __play_loop(self):
        iterator = range(self.number) if self.number is not None else count()
        tqdm_iterator = tqdm(iterator, total=self.number, desc='Playing', unit=' play')

        for _ in tqdm_iterator:
            self.__play_once()
            tqdm_iterator.set_postfix_str(f'Wins: {self.results[0]}/{self.results[1]}/{self.results[2]}')

            if self.interrupted:
                break

    def __play_once(self):
        winner = self.gameplay.play()

        if winner is self.player1:
            self.results[0] += 1
        elif winner is self.player2:
            self.results[1] += 1
        else:
            self.results[2] += 1

        self.gameplay.reset()
        self.gameplay.swap_players()
