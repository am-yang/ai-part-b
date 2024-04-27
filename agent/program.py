# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, Coord
from .moves import apply_move, all_possible_moves

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
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED")
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """
        # Below we have hardcoded two actions to be played depending on whether
        # the agent is playing as BLUE or RED. Obviously this won't work beyond
        # the initial moves of the game, so you should use some game playing
        # technique(s) to determine the best action to take.
        if not self.board.get(Coord(3, 3)):
            action: Action = PlaceAction(Coord(3, 3), Coord(3, 4), Coord(4, 3), Coord(4, 4))
            self.update(color=self._color, action=action, referee=referee) # updating internal game state via function
            return PlaceAction(
                Coord(3, 3), 
                Coord(3, 4), 
                Coord(4, 3), 
                Coord(4, 4)
            )
        else:
            action: Action = PlaceAction(Coord(2, 3), Coord(2, 4), Coord(2, 5), Coord(2, 6))
            self.update(color=self._color, action=action, referee=referee)
            return PlaceAction(
                Coord(2, 3), 
                Coord(2, 4), 
                Coord(2, 5), 
                Coord(2, 6)
            )


    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after an agent has taken their
        turn. You should use it to update the agent's internal game state. 
        """

        # There is only one action type, PlaceAction
        place_action: PlaceAction = action
        c1, c2, c3, c4 = place_action.coords

        self.board[c1] = self.board[c2] = self.board[c3] = self.board[c4] = color

        # Here we are just printing out the PlaceAction coordinates for
        # demonstration purposes. You should replace this with your own logic
        # to update your agent's internal game state representation.
        print(f"Testing: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")
