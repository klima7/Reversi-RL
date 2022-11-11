from board import Board, Side
from simulation import Simulation


class Environment:

    WIN_REWARD = 1000
    LOST_REWARD = -1000
    DRAW_REWARD = 0

    def __init__(self, size, backend):
        self.__size = size
        self.__backend = backend

    def get_all_states(self):
        return self.__backend.get_all_possible_boards_numbers()

    def get_possible_actions(self, state):
        simulation = self.get_simulation_from_state(state)
        return simulation.get_moves()

    def get_next_states(self, state, action):
        simulation = self.get_simulation_from_state(state)
        simulation.make_move(action)

        next_states = set()
        simulations = {simulation.copy()}

        while simulations:
            simulation = simulations.pop()
            if simulation.turn == Side.ME or simulation.is_finished():
                next_state = self.cvt_board_to_state(simulation.board)
                next_states.add(next_state)
            elif simulation.turn == Side.OPPONENT:
                for move in simulation.get_moves():
                    simulations.add(simulation.copy().make_move(move))

        probability = 1 / len(next_states)
        return {next_state: probability for next_state in next_states}

    def get_reward(self, state, action, next_state):
        simulation = self.get_simulation_from_state(next_state)
        winner = simulation.get_winner()
        if winner == Side.ME:
            return self.WIN_REWARD
        elif winner == Side.OPPONENT:
            return self.LOST_REWARD
        elif winner == Side.ANY:
            return self.DRAW_REWARD
        return 0

    # auxiliary methods

    def get_simulation_from_state(self, state):
        board = self.cvt_state_to_board(state)
        return Simulation(board, Side.ME, self.__backend)

    def get_simulation_from_position(self, position):
        return Simulation.create_from_number(self.__size, position, self.__backend)

    def cvt_board_to_state(self, board):
        return board.number

    def cvt_state_to_board(self, state):
        return Board.create_from_number(state, self.__size)
