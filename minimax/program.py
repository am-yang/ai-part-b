# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction
from .moves import apply_move, get_random_initial_action, convert_to_tuple_list, RED, BLUE, possible_actions, convert_to_place_action, render
from .minimax_basic import get_minimax_action, MiniMaxNode, init_children
from random import choice
import numpy as np
import hashlib


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
        # Storing the tree so that we don't create the children that we have already created
        self.tree: MiniMaxNode = None

    def action(self, **referee: dict) -> Action:
        # First two moves of the game are arbitrary 
        if self.total_moves == 1:
            return get_random_initial_action(self.board)
        
        elif self.total_moves == 2:
            opponent_color = BLUE if self.color_int == RED else RED
            return get_random_initial_action(self.board, opponent_color, False)
        
        # Moves from step 3 onwards are all minimax-generated        
        elif self.total_moves == 3:
            if self.tree and self.tree.children:
                # Convert board to hash and see if we have already generated it
                board_to_bytes = self.board.tobytes()
                board_hash = hashlib.md5(board_to_bytes).hexdigest()
                # Convert each child board to hash and compare with current board state
                for child in self.tree.children:
                    child_board_to_bytes = child.state.tobytes()
                    child_board_hash = hashlib.md5(child_board_to_bytes).hexdigest()
                    # If found, this means we have a whole tree already generated (don't need to create a new one)
                    if board_hash == child_board_hash:
                        self.tree = child
                        break
            else:
                self.tree = generate_node(self)
            
            self.tree = get_minimax_action(self.tree)
            return convert_to_place_action(self.tree.parent_action)


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
