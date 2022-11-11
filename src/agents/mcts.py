import math
import random
from collections import defaultdict

from . import PassiveAgent, agent
from board import Side


@agent
class MctsAgent(PassiveAgent):

    NAME = 'mcts'
    DEFAULT_C = 2

    def __init__(self, c=DEFAULT_C):
        super().__init__()
        self.__base_c = c
        self.__positions_stats = defaultdict(self._default_dict_factory)

    # ------- aux stuff ------

    @staticmethod
    def _default_dict_factory():
        return [0, 0]

    def get_data_to_save(self):
        print(f'There is {len(self.__positions_stats)} nodes in MCTS tree')
        return self.__positions_stats

    def set_saved_data(self, data):
        self.__positions_stats = data
        print(f'There is {len(self.__positions_stats)} nodes in MCTS tree')

    @property
    def __c(self):
        return self.__base_c if self.learn else 0

    def __get_position_total(self, position):
        return self.__positions_stats[position][0]

    def __get_position_visits(self, position):
        return self.__positions_stats[position][1]

    def __get_position_value(self, position):
        total = self.__positions_stats[position][0]
        visits = self.__positions_stats[position][1]
        return total / visits

    def __update_position(self, position, reward):
        self.__positions_stats[position][0] += reward
        self.__positions_stats[position][1] += 1

    def __is_position_known(self, position):
        return self.__get_position_visits(position) > 0

    def __ucb(self, parent_position, child_position):
        parent_n = self.__get_position_visits(parent_position)
        child_n = self.__get_position_visits(child_position)

        if parent_n == 0 or child_n == 0:
            return 0

        exploitation = self.__get_position_value(child_position)
        exploration = math.sqrt(math.log(parent_n) / child_n)
        ucb = exploitation + self.__c * exploration
        return ucb

    # ------- main stuff ------

    def get_action(self, state):
        position = self.env.get_game_state_from_state(state).number

        if self.learn:
            self.__learn(position)

        return self.__select_move(position)

    def __learn(self, root_position):
        path = self.__select_path(root_position)

        if len(path) == 0:
            reward = self.__rollout(root_position)
            self.__update_position(root_position, reward)
        else:
            self.__expand(path)
            reward = self.__rollout(path[-1])
            self.__backpropagate(path, reward)

    def __select_path(self, root_position):
        game_state = self.env.get_game_state_from_position(root_position)
        path = []

        while self.__is_position_known(game_state.number):
            path.append(game_state.number)

            if game_state.is_finished():
                break

            move = self.__select_move(game_state.number)
            game_state.make_move(move)

        return path

    def __select_move(self, position):
        game_state = self.env.get_game_state_from_position(position)
        moves = game_state.get_moves()
        positions = [game_state.copy().make_move(move).number for move in moves]

        if self.learn:
            undiscovered_moves = [move for move, position in zip(moves, positions) if not self.__is_position_known(position)]
            if len(undiscovered_moves) > 0:
                return random.choice(undiscovered_moves)

        ucb_values = [self.__ucb(game_state.number, position) for position in positions]
        max_ucb_value = max(ucb_values)
        best_moves = [move for move, ucb_value in zip(moves, ucb_values) if ucb_value == max_ucb_value]
        best_move = random.choice(best_moves)
        return best_move

    def __expand(self, path):
        game_state = self.env.get_game_state_from_position(path[-1])
        if game_state.is_finished():
            return

        possible_moves = game_state.get_moves()
        move = random.choice(possible_moves)
        game_state.make_move(move)
        new_position = game_state.number
        path.append(new_position)

    def __rollout(self, position):
        game_state = self.env.get_game_state_from_position(position)
        while not game_state.is_finished:
            possible_moves = game_state.get_moves()
            move = random.choice(possible_moves)
            game_state.make_move(move)

        winner = game_state.get_winner()
        reward = 1 if winner == Side.ME else (-1 if winner == Side.OPPONENT else 0)
        return reward

    def __backpropagate(self, path, reward):
        for position in path:
            self.__update_position(position, reward)
