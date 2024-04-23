# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, Coord, Vector2, Direction, BOARD_N


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
        match self._color:
            case PlayerColor.RED:
                print("Testing: RED is playing a PLACE action")
                return PlaceAction(
                    Coord(3, 3), 
                    Coord(3, 4), 
                    Coord(4, 3), 
                    Coord(4, 4)
                )
            case PlayerColor.BLUE:
                print("Testing: BLUE is playing a PLACE action")
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

        # Here we are just printing out the PlaceAction coordinates for
        # demonstration purposes. You should replace this with your own logic
        # to update your agent's internal game state representation.
        print(f"Testing: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")


TETROMINOES = [
        # I shape
        [Vector2(0,0), Vector2(0,1), Vector2(0,2), Vector2(0,3)],
        [Vector2(0,-1), Vector2(0,0), Vector2(0,1), Vector2(0,2)],
        [Vector2(0,-2), Vector2(0,-1), Vector2(0,0), Vector2(0,1)],
        [Vector2(0,-3), Vector2(0,-2), Vector2(0,-1), Vector2(0,0)],

        [Vector2(0,0), Vector2(1,0), Vector2(2,0), Vector2(3,0)],
        [Vector2(-1,0), Vector2(0,0), Vector2(1,0), Vector2(2,0)],
        [Vector2(-2,0), Vector2(-1,0), Vector2(0,0), Vector2(1,0)],
        [Vector2(-3,0), Vector2(-2,0), Vector2(-1,0), Vector2(0,0)],

        # O shape
        [Vector2(0,0), Vector2(0,1), Vector2(1,0), Vector2(1,1)],
        [Vector2(0,-1), Vector2(0,0), Vector2(1,0), Vector2(1,-1)],
        [Vector2(0,0), Vector2(0,1), Vector2(-1,0), Vector2(-1,1)],
        [Vector2(0,0), Vector2(0,-1), Vector2(-1,0), Vector2(-1,-1)],

        # T shape
        [Vector2(0,0), Vector2(0,1), Vector2(0,2), Vector2(1,1)],
        [Vector2(0,0), Vector2(0,1), Vector2(1,0), Vector2(0,-1)],
        [Vector2(0,0), Vector2(0,-1), Vector2(1,-1), Vector2(0,-2)],
        [Vector2(0,0), Vector2(-1,0), Vector2(-1,-1), Vector2(-1,-2)],

        [Vector2(0,0), Vector2(-1,1), Vector2(0,1), Vector2(1,1)],
        [Vector2(0,0), Vector2(1,0), Vector2(2,0), Vector2(1,-1)],
        [Vector2(0,0), Vector2(1,0), Vector2(0,-1), Vector2(-1,0)],
        [Vector2(0,0), Vector2(-1,0), Vector2(-2,0), Vector2(-1,-1)],

        [Vector2(0,0), Vector2(0,1), Vector2(0,2), Vector2(-1,1)],
        [Vector2(0,0), Vector2(1,0), Vector2(1,1), Vector2(1,-1)],
        [Vector2(0,0), Vector2(0,1), Vector2(0,-1), Vector2(-1,0)],
        [Vector2(0,0), Vector2(0,-1), Vector2(0,-2), Vector2(-1,-1)],

        [Vector2(0,0), Vector2(1,0), Vector2(2,0), Vector2(1,1)],
        [Vector2(0,0), Vector2(1,0), Vector2(0,1), Vector2(-1,0)],
        [Vector2(0,0), Vector2(-1,-1), Vector2(0,-1), Vector2(1,-1)],
        [Vector2(0,0), Vector2(-1,0), Vector2(-2,0), Vector2(-1,1)],

        # J shape 
        [Vector2(0,0), Vector2(0,1), Vector2(-1,1), Vector2(-2,1)],
        [Vector2(0,0), Vector2(1,0), Vector2(2,0), Vector2(2,-1)],
        [Vector2(0,0), Vector2(1,0), Vector2(1,-1), Vector2(-1,0)],
        [Vector2(0,0), Vector2(-1,0), Vector2(-2,0), Vector2(0,-1)],

        [Vector2(0,0), Vector2(1,0), Vector2(1,1), Vector2(1,2)],
        [Vector2(0,0), Vector2(0,1), Vector2(0,2), Vector2(-1,0)],
        [Vector2(0,0), Vector2(0,1), Vector2(0,-1), Vector2(-1,-1)],
        [Vector2(0,0), Vector2(0,-1), Vector2(0,-2), Vector2(-1,-2)],

        [Vector2(0,0), Vector2(0,1), Vector2(1,0), Vector2(2,0)],
        [Vector2(0,0), Vector2(0,-1), Vector2(1,-1), Vector2(2,-1)],
        [Vector2(0,0), Vector2(1,0), Vector2(-1,0), Vector2(-1,1)],
        [Vector2(0,0), Vector2(-1,0), Vector2(-2,0), Vector2(-2,1)],

        [Vector2(0,0), Vector2(0,1), Vector2(0,2), Vector2(1,2)],
        [Vector2(0,0), Vector2(0,1), Vector2(1,1), Vector2(0,-1)],
        [Vector2(0,0), Vector2(1,0), Vector2(0,-1), Vector2(0,-2)],
        [Vector2(0,0), Vector2(-1,0), Vector2(-1,-1), Vector2(-1,-2)],

        # L shape 
        [Vector2(0,0), Vector2(1,0), Vector2(2,0), Vector2(2,1)],
        [Vector2(0,0), Vector2(1,0), Vector2(1,1), Vector2(-1,0)],
        [Vector2(0,0), Vector2(0,1), Vector2(-1,0), Vector2(-2,0)],
        [Vector2(0,0), Vector2(0,-1), Vector2(-1,-1), Vector2(-2,-1)],

        [Vector2(0,0), Vector2(0,1), Vector2(0,2), Vector2(1,0)],
        [Vector2(0,0), Vector2(0,1), Vector2(0,-1), Vector2(1,-1)],
        [Vector2(0,0), Vector2(0,-1), Vector2(0,-2), Vector2(1,-2)],
        [Vector2(0,0), Vector2(-1,0), Vector2(-1,1), Vector2(-1,2)],

        [Vector2(0,0), Vector2(0,1), Vector2(1,1), Vector2(2,1)],
        [Vector2(0,0), Vector2(1,0), Vector2(2,0), Vector2(0,-1)],
        [Vector2(0,0), Vector2(1,0), Vector2(-1,0), Vector2(-1,-1)],
        [Vector2(0,0), Vector2(-1,0), Vector2(-2,0), Vector2(-2,-1)],

        [Vector2(0,0), Vector2(0,1), Vector2(0,2), Vector2(-1,2)],
        [Vector2(0,0), Vector2(0,1), Vector2(0,-1), Vector2(-1,1)],
        [Vector2(0,0), Vector2(0,-1), Vector2(0,-2), Vector2(-1,0)],
        [Vector2(0,0), Vector2(1,0), Vector2(1,-2), Vector2(1,-1)],

        # Z shape
        [Vector2(0,0), Vector2(0,1), Vector2(1,1), Vector2(1,2)],
        [Vector2(0,0), Vector2(1,0), Vector2(1,1), Vector2(0,-1)],
        [Vector2(0,0), Vector2(0,1), Vector2(-1,0), Vector2(-1,-1)],
        [Vector2(0,0), Vector2(0,-1), Vector2(-1,-1), Vector2(-1,-2)],

        [Vector2(0,0), Vector2(1,0), Vector2(0,1), Vector2(-1,1)],
        [Vector2(0,0), Vector2(1,0), Vector2(1,-1), Vector2(2,-1)],
        [Vector2(0,0), Vector2(-1,0), Vector2(0,-1), Vector2(1,-1)],
        [Vector2(0,0), Vector2(-1,0), Vector2(-1,1), Vector2(-2,1)],

        # S shape
        [Vector2(0,0), Vector2(0,1), Vector2(-1,1), Vector2(-1,2)],
        [Vector2(0,0), Vector2(0,1), Vector2(1,0), Vector2(1,-1)],
        [Vector2(0,0), Vector2(0,-1), Vector2(1,-1), Vector2(1,-2)],
        [Vector2(0,0), Vector2(0,-1), Vector2(-1,0), Vector2(-1,1)],

        [Vector2(0,0), Vector2(1,0), Vector2(1,1), Vector2(2,1)],
        [Vector2(0,0), Vector2(1,0), Vector2(0,-1), Vector2(-1,-1)],
        [Vector2(0,0), Vector2(0,1), Vector2(1,1), Vector2(-1,0)],
        [Vector2(0,0), Vector2(-1,0), Vector2(-1,-1), Vector2(-2,-1)]  
    ]

CELLS = 4
PATH_COST = 1
ROW = 'r'
COLUMN = 'c'

def all_possible_moves(
    board: dict[Coord, PlayerColor]
) -> list[PlaceAction]:
    '''
    Function to compute list of next possible actions from current state
    '''
        
    actions: list[PlaceAction] = []

    # Traverse empty cells ADJACENT to a red cell
    for row in range(int(BOARD_N)):
        for column in range(int(BOARD_N)):
            curr_cell = Coord(row, column)
            if board.get(curr_cell) == PlayerColor.RED:
                # Generating all adjacent cells to the red cell
                left = curr_cell.__add__(Direction.Left)
                right = curr_cell.__add__(Direction.Right)
                up = curr_cell.__add__(Direction.Up)
                down = curr_cell.__add__(Direction.Down)
                # If adjacent cell is empty, generate all possible tetrominoes that can be placed over it
                if left not in board:
                    actions += generate_tetrominoes(left, board)
                if right not in board:
                    actions += generate_tetrominoes(right, board)
                if up not in board:
                    actions += generate_tetrominoes(up, board)
                if down not in board:
                    actions += generate_tetrominoes(down, board)
    
    # Ensure that generated actions are unique
    return list(set(actions))

def generate_tetrominoes(
    cell: Coord,
    board: dict[Coord, PlayerColor]
) -> list[PlaceAction]:
    '''
    Helper function (of all_possible_moves) which helps us find all possible tetrominoes that can be placed over a given coordinate
    '''
    actions = []
    for tetromino in TETROMINOES:
        place_action = []
        for relative_position in tetromino: 
            # Generate tetromino cell 
            tetromino_cell = cell.__add__(relative_position)
            # If a cell in our tetromino is occupied, this shape is not applicable
            if tetromino_cell in board:
                break
            else:
                place_action.append(tetromino_cell)
        # If all cells of the tetromino are unoccupied, this is a valid move
        if len(place_action) == CELLS:
            # Sort coordinates based on row and column index (helps us to identify duplicate PLACE actions) 
            place_action.sort(key=lambda coord: (coord.r, coord.c))
            actions.append(PlaceAction(place_action[0], place_action[1], place_action[2], place_action[3]))

    return actions

def apply_move(
    board: dict[Coord, PlayerColor],
    move: PlaceAction
) -> dict[Coord, PlayerColor]: 
    '''
    Helper function to update board with new action, and clear rows/columns if necessary
    '''
    new_board = {key: value for key, value in board.items()}

    new_board[move.c1] = new_board[move.c2] = new_board[move.c3] = new_board[move.c4] = PlayerColor.RED
    count_row = 0
    count_column = 0
    clear_rows = []
    clear_columns = []
    # Check if a row/column needs to be cleared
    for row in range(int(BOARD_N)):
        count_row = 0
        count_column = 0
        for column in range(int(BOARD_N)):
            if Coord(row, column) in new_board:
                count_row += 1
            if Coord(column, row) in new_board:
                count_column += 1
        if count_row == BOARD_N:
            clear_rows.append(row)
        if count_column == BOARD_N:
            clear_columns.append(row)

    for row in clear_rows:
        new_board = {coord: player for coord, player in new_board.items() if coord.r != row}
    for column in clear_columns:
        new_board = {coord: player for coord, player in new_board.items() if coord.c != column}

    return new_board