import board_tools
import numpy as np
import board_tools as bt

b = bt.create_board(8)
bt.plot(b)
print(bt.get_legal_moves(b))
# b[2, 4] = 1

b2 = bt.get_board_after_move(b, np.array([2, 4]))
bt.plot(b2)

