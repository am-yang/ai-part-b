# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction
from .moves import apply_move, get_random_action, get_random_initial_action, convert_to_tuple_list
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
        self.player_tiles: list[tuple[int, int]] = [] # ALSO NEW


    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """
        if self.total_moves == 1:
            return get_random_initial_action(self.board)
        
        
        if self.total_moves == 2:
            return get_random_action(self.board, self._color, self.opponent_tiles, self.player_tiles, True)
        
        if self.total_moves <= 3:
            return get_random_action(self.board, self._color, self.opponent_tiles, self.player_tiles)


    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after an agent has taken their
        turn. You should use it to update the agent's internal game state. 
        """

        place_action: PlaceAction = action

        apply_move(board=self.board, place_action=place_action, color=color)
        self.total_moves += 1

        # Currently placing opponent tetromino
        if self._color != color:
            self.opponent_tiles += convert_to_tuple_list(action)
        else: 
            self.player_tiles += convert_to_tuple_list(action)


