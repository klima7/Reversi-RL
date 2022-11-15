import random

import numpy as np

from . import PassiveAgent, agent
from board import Side


@agent
class ValueApproximationAgent(PassiveAgent):
    NAME = 'value_approx'
    DEFAULT_ALPHA = 0.2
    DEFAULT_EPSILON = 0.25
    DEFAULT_DISCOUNT = 0.99

    def __init__(self, alpha=DEFAULT_ALPHA, epsilon=DEFAULT_EPSILON, discount=DEFAULT_DISCOUNT):
        super().__init__()
        self.__base_alpha = alpha
        self.__base_epsilon = epsilon
        self.__discount = discount
        self.__weights = None

    # ------- aux stuff ------

    @property
    def __alpha(self):
        return self.__base_alpha if self.learn else 0

    @property
    def __epsilon(self):
        return self.__base_epsilon if self.learn else 0

    def get_data_to_save(self):
        return self.__weights

    def set_saved_data(self, data):
        self.__weights = data

    # ------- main stuff ------

    def get_action(self, state):
        possible_actions = self.env.get_possible_actions(state)

        if len(possible_actions) == 0:
            return None

        should_random = random.random() < self.__epsilon

        if should_random:
            return random.choice(possible_actions)
        else:
            return self.__get_best_action(state)

    def update(self, state, action, reward, next_state):
        if not self.learn:
            return

        features = self.__get_features(state, action)

        if self.__weights is None:
            self.__weights = np.random.random((len(features),))

        delta = (reward + self.__discount * self.__get_value(next_state)) - self.__get_qvalue(state, action)
        self.__weights += self.__alpha * delta * features

    def __get_best_action(self, state):
        possible_actions = self.env.get_possible_actions(state)

        if len(possible_actions) == 0:
            return None

        qvalues = [self.__get_qvalue(state, action) for action in possible_actions]
        best_qvalue = max(qvalues)
        best_actions = [action for action, qvalue in zip(possible_actions, qvalues) if qvalue == best_qvalue]
        best_action = random.choice(best_actions)
        return best_action

    def __get_value(self, state):
        possible_actions = self.env.get_possible_actions(state)

        if len(possible_actions) == 0:
            return 0.0

        return max([self.__get_qvalue(state, action) for action in possible_actions])

    def __get_qvalue(self, state, action):
        features = self.__get_features(state, action)
        return self.__weights @ features if self.__weights is not None else 0

    def __get_features(self, state, action):
        simulation = self.env.get_simulation_from_state(state)
        simulation.make_move(action)
        board = simulation.board

        my_features = self.__get_features_for_side(board, Side.ME)
        op_features = self.__get_features_for_side(board, Side.OPPONENT)
        features = [*my_features, *op_features]
        return np.array(features)

    def __get_features_for_side(self, board, side):
        fields_count = np.prod(board.size)
        moves_count = len(board.get_legal_moves(side)) / fields_count
        discs_count = board.get_discs_count(side) / fields_count
        corners_count = self.__get_corner_discs_count(board, side) / fields_count
        edges_count = self.__get_edge_discs_count(board, side) / fields_count
        diagonal_count = self.__get_diagonal_discs_count(board, side) / fields_count
        rings_densities = self.__get_discs_densities_in_rings(board, side)
        return [moves_count, discs_count, corners_count, edges_count, diagonal_count, *rings_densities]

    @staticmethod
    def __get_corner_discs_count(board, side):
        board_array = board.as_numpy_array()
        corners_ix = np.ix_((0, -1), (0, -1))
        corners = board_array[corners_ix]
        return np.sum(corners == side)

    @staticmethod
    def __get_edge_discs_count(board, side):
        board_array = board.as_numpy_array()
        h_edges = board_array[1:-1, (0, -1)]
        v_edges = board_array[(0, -1), 1:-1]
        edges = np.concatenate([h_edges.flatten(), v_edges.flatten()])
        return np.sum(edges == side)

    @staticmethod
    def __get_diagonal_discs_count(board, side):
        diagonal_count = 0

        board_array = board.as_numpy_array()
        while board_array.shape[0] >= 2 and board_array.shape[1] >= 2:
            edges = board_array[np.ix_((0, -1), (0, -1))]
            count = np.sum(edges == side)
            diagonal_count += count
            board_array = board_array[1:-1, 1:-1]

        return diagonal_count

    @staticmethod
    def __get_discs_densities_in_rings(board, side):
        densities = []

        board_array = board.as_numpy_array()
        while board_array.shape[0] >= 2 and board_array.shape[1] >= 2:
            max_count_in_ring = 4 + 2 * (board_array.shape[0] - 2) + 2 * (board_array.shape[1] - 2)
            count_before = np.sum(board_array == side)
            board_array = board_array[1:-1, 1:-1]
            count_after = np.sum(board_array == side)
            count_in_ring = count_before - count_after
            density = count_in_ring / max_count_in_ring
            densities.append(density)

        if board_array.size > 0:
            max_count = np.prod(board_array.shape)
            count = np.sum(board_array == side)
            density = count / max_count
            densities.append(density)

        return densities
