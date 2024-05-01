# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, Coord
from .moves import apply_move, generate_random_action
from .minimax_basic import minimax, MiniMaxNode

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
        self.board: dict[Coord, PlayerColor] = {} # internal game state of agent
        self.total_moves: int = 1
        self.minimax_tree = None

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """
        # to speed up search, we will make first move of agent arbitrary
        if self.total_moves <= 2:
            return generate_random_action(self.board)
        
        previous_player_colour = None
        if self._color == PlayerColor.BLUE:
            previous_player_colour = PlayerColor.RED
        else: 
            previous_player_colour = PlayerColor.BLUE
        
        node =  minimax(MiniMaxNode(previous_player_colour, self.board, self.total_moves - 1, self._color))

        return node.parent_action
        

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after an agent has taken their
        turn. You should use it to update the agent's internal game state. 
        """

        place_action: PlaceAction = action
        self.board = apply_move(self.board, place_action, color)
        self.total_moves += 1


    # Additional helper functions defined below
        

