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
from agents import HumanAgent


class Gameplay(ABC):

    def __init__(self, size, delay):
        self.size = size
        self.game_state = GameState(size)

        self.env_white = Environment(self.game_state, Color.WHITE)
        self.env_black = Environment(self.game_state, Color.BLACK)

        self.delay = delay

        self.player_black = None
        self.player_white = None

    def set_players(self, player_black, player_white):
        self.player_black = player_black
        self.player_white = player_white

    def swap_players(self):
        self.set_players(self.player_white, self.player_black)

    @property
    def _player(self):
        return self.player_white if self.game_state.turn_color == Color.WHITE else self.player_black

    @property
    def _env(self):
        return self.env_white if self.game_state.turn_color == Color.WHITE else self.env_black

    def _get_winner(self):
        winner_color = self.game_state.get_winner()
        if winner_color == Color.WHITE:
            return self.player_white
        elif winner_color == Color.BLACK:
            return self.player_black
        else:
            return None

    @abstractmethod
    def play(self):
        pass

    def reset(self):
        self.game_state.reset()

    def dispose(self):
        pass


class NoGuiGameplay(Gameplay):

    def play(self):
        while not self.game_state.is_finished():
            action = self._player.get_action(self._env)
            self.game_state.make_move(action)

        return self._get_winner()


class GuiGameplay(Gameplay):

    FIELD_SIZE = 100
    DISC_SIZE = 80

    def __init__(self, size, delay=0):
        super().__init__(size, delay)

        self.running = True
        self.screen = None
        self.pool = ThreadPool(1)
        self.task = None
        self.last_move = None

    def play(self):
        self.__init_gui_if_needed()
        self.__update_window_title()

        while not self.game_state.is_finished() and self.running:
            self.__collect_events()
            self.__update()
            self.__draw_screen()

        return self._get_winner()

    def dispose(self):
        self.__dispose_gui()

    def __init_gui_if_needed(self):
        if not pygame.get_init():
            pygame.init()
            self.screen = pygame.display.set_mode([self.size[1] * self.FIELD_SIZE, self.size[0] * self.FIELD_SIZE])

    def __update_window_title(self):
        white_name = self.__get_player_name(self.player_white)
        black_name = self.__get_player_name(self.player_black)
        pygame.display.set_caption(f'Reversi {self.size[0]}x{self.size[1]} | White: {white_name} | Black: {black_name}')

    def __dispose_gui(self):
        pygame.quit()
        self.screen = None

    @staticmethod
    def __get_player_name(player):
        if player is None:
            return 'human'
        else:
            return player.agent_name

    def __collect_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                signal.raise_signal(signal.SIGINT)

    def __draw_screen(self):
        self.__draw_board()
        self.__draw_discs()
        self.__draw_last_move()
        pygame.display.flip()

    def __draw_board(self):
        self.screen.fill((0, 128, 0))
        pygame.draw.rect(self.screen, (0, 150, 0), (0, 0, self.size[1] * self.FIELD_SIZE, self.size[0] * self.FIELD_SIZE), width=3)
        for y in range(1, self.size[0]):
            pygame.draw.line(self.screen, (0, 150, 0), (0, y*self.FIELD_SIZE), (self.size[1] * self.FIELD_SIZE, y*self.FIELD_SIZE), width=3)
        for x in range(1, self.size[1]):
            pygame.draw.line(self.screen, (0, 150, 0), (x*self.FIELD_SIZE, 0), (x*self.FIELD_SIZE, self.size[0] * self.FIELD_SIZE), width=3)

    def __draw_discs(self):
        possible_moves = self.game_state.get_moves()
        disc_center_offset = self.FIELD_SIZE // 2
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                disc_color = self.game_state.board[y, x]
                pos = (x * self.FIELD_SIZE + disc_center_offset, y * self.FIELD_SIZE + disc_center_offset)
                if disc_color == Color.ANY and (y, x) in possible_moves:
                    color = [255, 255, 255] if self.game_state.turn_color == Color.WHITE else [0, 0, 0]
                    pygame.draw.circle(self.screen, color, pos, self.DISC_SIZE // 2, width=3)
                elif disc_color != Color.ANY:
                    color = [255, 255, 255] if disc_color == Color.WHITE else [0, 0, 0]
                    pygame.draw.circle(self.screen, color, pos, self.DISC_SIZE // 2)

    def __draw_last_move(self):
        if self.last_move is not None:
            y, x = self.last_move
            x_pos, y_pos = x*self.FIELD_SIZE+self.FIELD_SIZE//2, y*self.FIELD_SIZE+self.FIELD_SIZE//2
            pygame.draw.line(self.screen, (255, 0, 0), (x_pos, 0), (x_pos, self.size[0] * self.FIELD_SIZE), width=2)
            pygame.draw.line(self.screen, (255, 0, 0), (0, y_pos), (self.size[1] * self.FIELD_SIZE, y_pos), width=2)

    def __update(self):
        action = self.__get_action_from_player(self._player)
        if action is not None:
            self.game_state.make_move(action)
            self.last_move = action

    def __get_action_from_player(self, player):
        if isinstance(player, HumanAgent):
            return self.__get_action_from_real_player()
        else:
            return self.__get_action_from_artificial_player(player)

    def __get_action_from_artificial_player(self, player):
        if self.task is None:
            self.task = self.pool.apply_async(GuiGameplay._thread_to_get_action, [player, self._env, self.delay])

        if self.task.ready():
            action = self.task.get()
            self.task = None
            return action

        return None

    @staticmethod
    def _thread_to_get_action(player, env, delay):
        start_time = time.time()
        action = player.get_action(env)
        duration = time.time() - start_time

        sleep_time = delay - duration
        if sleep_time > 0:
            time.sleep(sleep_time)

        return action

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

        for play_number in tqdm_iterator:
            self.__play_once()
            tqdm_iterator.set_postfix_str(f'Wins: {self.results[0]}/{self.results[1]}/{self.results[2]}')

            if play_number % 100 == 0:
                self.__save_agents_knowledge()

            if self.interrupted:
                break

        self.__save_agents_knowledge()

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

    def __save_agents_knowledge(self):
        self.player1.save_knowledge()
        self.player2.save_knowledge()