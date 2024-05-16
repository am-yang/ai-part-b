from minimax.program import Agent, generate_node
from minimax.minimax_basic import init_children
from minimax.moves import get_random_initial_action, possible_actions, RED, BLUE
from referee.game import PlayerColor
import numpy as np
import time
import hashlib


# start = time.perf_counter()

board = np.zeros((11, 11), dtype=int)
board[6,3] = board[6,4] = board[6,5] = board[6,6] = BLUE
board[6,2] = board[7,2] = board[7,3] = board[7,4] = RED

# board[7,5] = board[7,6] = board[8,5] = board[8,6] = RED
board[2,2] = board[3,2] = board[4,2] = board[5,2] = RED


print(str(len(possible_actions(board, RED))))
# end = time.perf_counter()
# print(end - start)  # will print the elapsed time in seconds