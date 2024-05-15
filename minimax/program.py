# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction
from .moves import apply_move, get_random_initial_action, RED, BLUE
from .minimax_basic import get_minimax_action, MiniMaxNode, MAX_TIME
import numpy as np


class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Tetress game events.
    """

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """
        self._color = color
        self.color_int = RED if color == PlayerColor.RED else BLUE
        self.total_moves: int = 1
        self.board = np.zeros((11, 11), dtype=int)
        self.allowed_time: float = MAX_TIME

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """
        if self.total_moves == 1:
            return get_random_initial_action(self.board)
        
        elif self.total_moves == 2:
            opponent_color = BLUE if self.color_int == RED else RED
            return get_random_initial_action(self.board, opponent_color, False)
        
        else:
            action, leftover_time = get_minimax_action(self.board, self.total_moves, self._color, self.allowed_time)
            self.allowed_time = MAX_TIME + leftover_time
            return action


    def update(self, color: PlayerColor, action: Action, **referee: dict):

        place_action: PlaceAction = action
        self.total_moves += 1
        self.board = apply_move(
            board=self.board, 
            color=color, 
            place_action=place_action, 
            place_action_list=None, 
            color_as_int=None
        )



def generate_node(agent: Agent) -> MiniMaxNode:
    print("how many times is this called....")
    # initialise root node
    root_player = agent.color_int
    opponent_player = BLUE if agent.color_int == RED else RED
    root_depth = agent.total_moves - 1
    root_node = MiniMaxNode(
        color=opponent_player, 
        state=agent.board, 
        depth=root_depth, 
        root_colour=root_player
    )
    return root_node
