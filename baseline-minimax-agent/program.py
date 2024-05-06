# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction
from .moves import apply_move, get_random_initial_action, convert_to_tuple_list
from .minimax_basic import get_minimax_action
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
        self.total_moves: int = 1
        self.board = np.zeros((11, 11), dtype=int)
        self.opponent_tiles: list[tuple[int, int]] = [] # NEW
        self.player_tiles: list[tuple[int, int]] = [] # Also new

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """
        if self.total_moves <= 2:
            return get_random_initial_action(self.board)

        return get_minimax_action(self.board, self.total_moves, self._color, self.opponent_tiles, self.player_tiles)


    def update(self, color: PlayerColor, action: Action, **referee: dict):

        place_action: PlaceAction = action
        if self._color != color:
            self.opponent_tiles += convert_to_tuple_list(action)
        else:
            self.player_tiles += convert_to_tuple_list(action)

        self.total_moves += 1
        self.board = apply_move(
            board=self.board, 
            color=color, 
            place_action=place_action, 
            place_action_list=None, 
            color_as_int=None, 
            opponent_tiles=self.opponent_tiles, 
            player_tiles=self.player_tiles
        )


