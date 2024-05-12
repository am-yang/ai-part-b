from minimax.program import Agent
from referee.game import PlayerColor
import numpy as np

agent = Agent(PlayerColor.RED)

agent.board = np.zeros((11, 11), dtype=int)
agent.board[4,3] = agent.board[5,3] = agent.board[6,3] = agent.board[6,4] = 1
agent.board[6,5] = agent.board[7,5] = agent.board[8,4] = agent.board[8,5] = 2
agent.total_moves = 3
agent.action()
