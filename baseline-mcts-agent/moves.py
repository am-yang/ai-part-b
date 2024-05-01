# Source file which contains all helper functions that allow
# us to generate all (valid) moves at a given turn 

from referee.game import PlayerColor, PlaceAction, Coord, Direction
from referee.game.constants import BOARD_N 
from referee.game.coord import Vector2

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
MAX_DEPTH = 150
FIRST_MOVES = 2

def all_possible_moves(
    board: dict[Coord, PlayerColor],
    depth: int,
    color: PlayerColor
) -> list[PlaceAction]:
    '''
    Function to compute list of next possible actions from current state
    '''
        
    actions: list[PlaceAction] = []

    is_first_moves = depth <= FIRST_MOVES

    # Traverse empty cells ADJACENT to a red cell
    for row in range(int(BOARD_N)):
        for column in range(int(BOARD_N)):
            curr_cell = Coord(row, column)
            # First moves can be anywhere (not constrained to adjacent tile)
            if is_first_moves:
                actions += generate_tetrominoes(curr_cell, board)
                continue
            if board.get(curr_cell) == color:
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
    move: PlaceAction,
    player: PlayerColor
) -> dict[Coord, PlayerColor]: 
    '''
    Helper function to update board with new action, and clear rows/columns if necessary
    '''
    new_board = {key: value for key, value in board.items()}

    new_board[move.c1] = new_board[move.c2] = new_board[move.c3] = new_board[move.c4] = player
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

def is_terminal_state(
    board: dict[Coord, PlayerColor],
    color: PlayerColor,
    depth: int
) -> bool:
    if depth == MAX_DEPTH:
        return True
    
    if depth <= FIRST_MOVES:
        return False
    
    # Traverse empty cells ADJACENT to a red cell
    for row in range(int(BOARD_N)):
        for column in range(int(BOARD_N)):
            curr_cell = Coord(row, column)
            if board.get(curr_cell) == color:
                # Generating all adjacent cells to the red cell
                left = curr_cell.__add__(Direction.Left)
                right = curr_cell.__add__(Direction.Right)
                up = curr_cell.__add__(Direction.Up)
                down = curr_cell.__add__(Direction.Down)
                # If adjacent cell is empty, generate all possible tetrominoes that can be placed over it
                if left not in board:
                    if moves_on_cell(left, board):
                        return False
                if right not in board:
                    if moves_on_cell(right, board):
                        return False
                if up not in board:
                    if moves_on_cell(up, board):
                        return False
                if down not in board:
                    if moves_on_cell(down, board):
                        return False
    return True

def moves_on_cell(
    cell: Coord,
    board: dict[Coord, PlayerColor]
) -> bool:
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
            return True

    return False


def count_colors(
    board: dict[Coord, PlayerColor],
    color: PlayerColor
) -> int:
    count = 0
    for key in board:
        if board[key] == color:
            count += 1
    
    return count