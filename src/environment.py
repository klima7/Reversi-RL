from abc import ABC, abstractmethod
from pathlib import Path
import pickle

from board import Board, Side
from game_state import GameState


class Environment(ABC):

    WIN_REWARD = 1000
    LOST_REWARD = -1000
    DRAW_REWARD = 0

    def __init__(self, size):
        self.size = size

    @abstractmethod
    def get_all_states(self):
        pass

    @abstractmethod
    def get_possible_actions(self, state):
        pass

    @abstractmethod
    def get_next_states(self, state, action):
        pass

    @abstractmethod
    def get_reward(self, state, action, next_state):
        pass

    def _cvt_move_to_action(self, move):
        return move[0] * self.size[1] + move[1]

    def _cvt_action_to_move(self, action):
        return divmod(action, self.size[1])

    def _get_all_possible_boards(self):
        boards = set()
        game_states = {GameState.create_initial(self.size)}

        while game_states:
            game_state = game_states.pop()

            if game_state in game_states:
                continue

            if game_state.is_finished():
                boards.update([game_state.board_view, game_state.opposite_board_view])
            else:
                boards.add(game_state.board_view)

            for move in game_state.get_moves():
                next_game_state = game_state.copy().make_move(move)
                game_states.add(next_game_state)

        return boards


class LiveEnvironment(Environment):

    def __init__(self, size):
        super().__init__(size)
        self.__all_states = None

    def get_all_states(self):
        if self.__all_states is None:
            self.__all_states = {board.number for board in self._get_all_possible_boards()}
        return self.__all_states

    def get_possible_actions(self, state):
        game_state = self.__get_game_state_from_state(state)
        return tuple(self._cvt_move_to_action(move) for move in game_state.get_moves())

    def get_next_states(self, state, action):
        game_state = self.__get_game_state_from_state(state)
        game_state.make_move(self._cvt_action_to_move(action))

        next_states = set()
        game_states = {game_state.copy()}

        while game_states:
            game_state = game_states.pop()
            if game_state.turn == Side.ME or game_state.is_finished():
                next_states.add(game_state.board.number)
            elif game_state.turn == Side.OPPONENT:
                for move in game_state.get_moves():
                    game_states.add(game_state.copy().make_move(move))

        probability = 1 / len(next_states)
        return {next_state: probability for next_state in next_states}

    def get_reward(self, state, action, next_state):
        game_state = self.__get_game_state_from_state(next_state)
        if game_state.is_finished():
            winner = game_state.get_winner()
            if winner == Side.ME:
                return self.WIN_REWARD
            elif winner == Side.OPPONENT:
                return self.LOST_REWARD
            elif winner == Side.ANY:
                return self.DRAW_REWARD
        return 0

    def __get_game_state_from_state(self, state):
        board = Board.create_from_number(state, self.size)
        return GameState(board, Side.ME)


class PreparedEnvironment(Environment):

    def __init__(self, size):
        super().__init__(size)

        self.__transitions = None
        self.__terminal_states = None

        self.__preparation()

    def get_all_states(self):
        return list(self.__transitions.keys())

    def get_possible_actions(self, state):
        return list(self.__transitions[state].keys())

    def get_next_states(self, state, action):
        op_has_moves, temp_state = self.__transitions[state][action]

        if not op_has_moves:
            return {temp_state: 1.0}
        else:
            next_states = list(map(lambda e: e[1], self.__transitions[temp_state].values()))
            probability = 1 / len(next_states)
            return {next_state: probability for next_state in next_states}

    def get_reward(self, state, action, next_state):
        if next_state in self.__terminal_states[Side.ME]:
            return self.WIN_REWARD
        elif next_state in self.__terminal_states[Side.OPPONENT]:
            return self.LOST_REWARD
        elif next_state in self.__terminal_states[Side.ANY]:
            return self.DRAW_REWARD
        return 0

    def __preparation(self):
        if self.__is_already_prepared():
            self.__load_prepared()
        else:
            self.__prepare()
            self.__save_prepared()

    def __is_already_prepared(self):
        return self.__get_file_location().exists()

    def __load_prepared(self):
        with open(self.__get_file_location(), 'rb') as f:
            self.__terminal_states = pickle.load(f)
            self.__transitions = pickle.load(f)

    def __prepare(self):
        all_boards = list(self._get_all_possible_boards())
        self.__transitions = self.__get_transitions(all_boards)
        self.__terminal_states = self.__get_terminal_states(all_boards)

    def __save_prepared(self):
        with open(self.__get_file_location(), 'wb') as f:
            pickle.dump(self.__transitions, f)
            pickle.dump(self.__terminal_states, f)

    def __get_transitions(self, boards):
        transitions = {}

        for board in boards:
            moves = board.get_legal_moves(Side.ME)
            actions_dict = {self.__get_move_outcome(board, move) for move in moves}
            transitions[board.number] = actions_dict

        return transitions

    def __get_move_outcome(self, board: Board, move):
        tmp_board = board.copy().make_move(move, Side.ME)

        if tmp_board.has_any_moves(Side.OPPONENT)

        tmp_board = board_tools.get_board_after_move(board, move, Side.ME)
        op_moves = board_tools.get_legal_moves(next_rel_board, Side.OPPONENT)

        op_has_moves = len(op_moves) > 0
        final_board = -next_rel_board if op_has_moves else next_rel_board

        next_state = board_tools.convert_to_number(final_board)
        state_dict[self._cvt_move_to_action(move)] = (op_has_moves, next_state)

    @staticmethod
    def __get_terminal_states(boards):
        terminal_states = {
            Side.ME: set(),
            Side.OPPONENT: set(),
            Side.ANY: set()
        }

        for board in boards:
            if board.is_finished():
                winner = board.get_winner()
                terminal_states[winner].add(board.number)

        return terminal_states

    def __get_file_location(self):
        root_path = Path(__file__).parent.parent
        filename = f'{self.size[0]}x{self.size[1]}_env.pickle'
        return root_path / 'res' / filename
