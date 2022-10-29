import board_tools as bt


def generate_all_states(size):
    all_states = []
    current_states = [bt.create_board(4)]

    while current_states:
        current_state = current_states.pop(0)
        moves = bt.get_legal_moves(current_state)


