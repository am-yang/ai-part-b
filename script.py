from minimax.program import Agent, generate_node
from minimax.minimax_basic import init_children
from minimax.moves import get_random_initial_action
from referee.game import PlayerColor
import numpy as np
import time
import hashlib


start = time.perf_counter()

agent = Agent(PlayerColor.RED)
agent.board[6,5] = agent.board[7,5] = agent.board[8,4] = agent.board[8,5] = 2
agent.board[4,3] = agent.board[5,3] = agent.board[6,3] = agent.board[6,4] = 1

agent.tree = generate_node(agent)
agent.tree.children = init_children(agent.tree)
print(str(len(agent.tree.children)))
end = time.perf_counter()
print(end - start)  # will print the elapsed time in seconds