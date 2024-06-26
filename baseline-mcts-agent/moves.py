import numpy as np
from copy import deepcopy
from random import choice, randint
from referee.game import PlaceAction, PlayerColor
from referee.game.coord import Coord


# Initialise board
TETROMINOES: list[list[tuple[int, int]]] = [
        # I shape
        [(0,0), (0,1), (0,2), (0,3)],[(0,-1), (0,0), (0,1), (0,2)], [(0,-2), (0,-1), (0,0), (0,1)], [(0,-3), (0,-2), (0,-1), (0,0)],

        [(0,0), (1,0), (2,0), (3,0)], [(-1,0), (0,0), (1,0), (2,0)],[(-2,0), (-1,0), (0,0), (1,0)],[(-3,0), (-2,0), (-1,0), (0,0)],

        # O shape
        [(0,0), (0,1), (1,0), (1,1)],[(0,-1), (0,0), (1,-1), (1,0)],[(-1,0), (-1,1), (0,0), (0,1)],[(-1,-1), (-1,0), (0,-1), (0,0)],

        # T shape
        [(0,0), (0,1), (0,2), (1,1)],[(0,-1), (0,0), (0,1), (1,0)],[(0,-2), (0,-1), (0,0), (1,-1)],[(-1,-2), (-1,-1), (-1,0), (0,0)],

        [(0,0), (-1,1), (0,1), (1,1)],[(0,0), (1,0), (2,0), (1,-1)],[(0,0), (1,0), (0,-1), (-1,0)],[(0,0), (-1,0), (-2,0), (-1,-1)],

        [(0,0), (0,1), (0,2), (-1,1)],[(0,0), (1,0), (1,1), (1,-1)],[(0,0), (0,1), (0,-1), (-1,0)],[(0,0), (0,-1), (0,-2), (-1,-1)],

        [(0,0), (1,0), (2,0), (1,1)],[(0,0), (1,0), (0,1), (-1,0)],[(0,0), (-1,-1), (0,-1), (1,-1)],[(0,0), (-1,0), (-2,0), (-1,1)],

        # J shape 
        [(0,0), (0,1), (-1,1), (-2,1)],[(0,0), (1,0), (2,0), (2,-1)],[(0,0), (1,0), (1,-1), (-1,0)],[(0,0), (-1,0), (-2,0), (0,-1)],

        [(0,0), (1,0), (1,1), (1,2)],[(0,0), (0,1), (0,2), (-1,0)],[(0,0), (0,1), (0,-1), (-1,-1)],[(0,0), (0,-1), (0,-2), (-1,-2)],

        [(0,0), (0,1), (1,0), (2,0)],[(0,0), (0,-1), (1,-1), (2,-1)],[(0,0), (1,0), (-1,0), (-1,1)],[(0,0), (-1,0), (-2,0), (-2,1)],

        [(0,0), (0,1), (0,2), (1,2)],[(0,0), (0,1), (1,1), (0,-1)],[(0,0), (1,0), (0,-1), (0,-2)],[(0,0), (-1,0), (-1,-1), (-1,-2)],

        # L shape 
        [(0,0), (1,0), (2,0), (2,1)],[(0,0), (1,0), (1,1), (-1,0)],[(0,0), (0,1), (-1,0), (-2,0)],[(0,0), (0,-1), (-1,-1), (-2,-1)],

        [(0,0), (0,1), (0,2), (1,0)],[(0,0), (0,1), (0,-1), (1,-1)],[(0,0), (0,-1), (0,-2), (1,-2)],[(0,0), (-1,0), (-1,1), (-1,2)],

        [(0,0), (0,1), (1,1), (2,1)],[(0,0), (1,0), (2,0), (0,-1)],[(0,0), (1,0), (-1,0), (-1,-1)],[(0,0), (-1,0), (-2,0), (-2,-1)],

        [(0,0), (0,1), (0,2), (-1,2)],[(0,0), (0,1), (0,-1), (-1,1)],[(0,0), (0,-1), (0,-2), (-1,0)],[(0,0), (1,0), (1,-2), (1,-1)],

        # Z shape
        [(0,0), (0,1), (1,1), (1,2)],[(0,0), (1,0), (1,1), (0,-1)],[(0,0), (0,1), (-1,0), (-1,-1)],[(0,0), (0,-1), (-1,-1), (-1,-2)],

        [(0,0), (1,0), (0,1), (-1,1)],[(0,0), (1,0), (1,-1), (2,-1)],[(0,0), (-1,0), (0,-1), (1,-1)],[(0,0), (-1,0), (-1,1), (-2,1)],

        # S shape
        [(0,0), (0,1), (-1,1), (-1,2)],[(0,0), (0,1), (1,0), (1,-1)],[(0,0), (0,-1), (1,-1), (1,-2)],[(0,0), (0,-1), (-1,0), (-1,1)],

        [(0,0), (1,0), (1,1), (2,1)],[(0,0), (1,0), (0,-1), (-1,-1)],[(0,0), (0,1), (1,1), (-1,0)],[(0,0), (-1,0), (-1,-1), (-2,-1)]  
    ]

ADJACENT: list[tuple[int, int]] = [(1, 0), (-1, 0), (0, 1), (0, -1)]
BOARD_DIMENSION = 11
MAX_BOARD_INDEX = 10
CELLS = 4
RED = 1
BLUE = 2
VACANT = 0

reached_opponent = False


def generate_tetrominoes(
    board: np.ndarray,
    cell_row: int, 
    cell_col: int
) -> list[list[tuple[int, int]]]:
    possible_actions = []
    for shape in TETROMINOES:
        tetromino = []
        for row, col in shape:
            new_row, new_col = get_cell_coords(row + cell_row, col + cell_col)
            if board[new_row, new_col] != VACANT:
                break
            tetromino.append((new_row, new_col))

        if len(tetromino) == CELLS:
            sorted_tetromino = sorted(tetromino)
            possible_actions.append(sorted_tetromino)
    
    return possible_actions


def get_remaining_empty_tiles(
    opponent_tiles: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    
    return [(row, col) for row in range(BOARD_DIMENSION) for col in range(BOARD_DIMENSION) if (row, col) not in opponent_tiles]



def possible_actions(
    board:np.ndarray, 
    player_tiles: list[tuple[int, int]]
) -> list[list[tuple[int, int]]]:
    '''
    Function that takes two args, a board representation, and the current player, 
    and outputs the list of posisble actions the current player can take
    '''
    actions = []
    empty_adjacent_tiles: list[tuple[int, int]] = get_empty_adjacent_tiles(board, player_tiles)
    for tile in empty_adjacent_tiles:
        actions += generate_tetrominoes(board, tile[0], tile[1])
    
    unique_actions: list[list[tuple[int, int]]] = [list(action) for action in set(tuple(action) for action in actions)]

    return unique_actions
   


def get_cell_coords(row: int, col: int) -> tuple[int, int]:

    new_row = row % BOARD_DIMENSION
    new_col = col % BOARD_DIMENSION

    return new_row, new_col



def apply_move(
    board: np.ndarray, 
    color: PlayerColor=None, 
    place_action: PlaceAction=None, 
    make_copy: bool = False, 
    place_action_list: list[tuple[int, int]] = None,
    color_int: int = 0
) -> np.ndarray:

    board_ref = deepcopy(board) if make_copy else board # make copy of board if necessary

    player = color_int
    if color:
        player = RED if color == PlayerColor.RED else BLUE

    action_as_list = convert_to_tuple_list(place_action) if place_action_list is None else place_action_list

    rows = [rows for rows, _ in action_as_list]
    cols = [cols for _, cols in action_as_list]

    board_ref[action_as_list[0][0], action_as_list[0][1]] = board_ref[action_as_list[1][0], action_as_list[1][1]] = \
        board_ref[action_as_list[2][0], action_as_list[2][1]] = board_ref[action_as_list[3][0], action_as_list[3][1]] = player

    # Now make sure each row/col that is fully filled up, is cleared out 
    clear_out_row = []
    clear_out_col = []
    count_zeroes = 0
    for row in rows:
        count_zeroes = np.count_nonzero(board_ref[row, :] == VACANT)
        if count_zeroes == 0:
            clear_out_row.append(row)

    for col in cols:
        count_zeroes = np.count_nonzero(board_ref[:, col] == VACANT)
        if count_zeroes == 0:
            clear_out_col.append(col)

    # Now clear out rows and columns
    for row in clear_out_row:
        board_ref[row, :] = VACANT

    for col in clear_out_col:
        board_ref[:, col] = VACANT

    return board_ref
    

def convert_to_tuple_list(
    place_action: PlaceAction
) -> list[tuple[int, int]]:
    
    cell1 = (place_action.c1.r, place_action.c1.c)
    cell2 = (place_action.c2.r, place_action.c2.c)
    cell3 = (place_action.c3.r, place_action.c3.c)
    cell4 = (place_action.c4.r, place_action.c4.c)

    return [cell1, cell2, cell3, cell4]

def convert_to_place_action(
    action: list[tuple[int, int]]
) -> PlaceAction:
    coord1 = Coord(action[0][0], action[0][1])
    coord2 = Coord(action[1][0], action[1][1])
    coord3 = Coord(action[2][0], action[2][1])
    coord4 = Coord(action[3][0], action[3][1])

    return PlaceAction(coord1, coord2, coord3, coord4)



def get_empty_adjacent_tiles(
    board: np.ndarray, 
    player_tiles: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    
    empty_adjacent: list[tuple[int, int]] = []
    for (row, col) in player_tiles:
        for adjacent in ADJACENT:
            new_row, new_col = get_cell_coords(row + adjacent[0], col + adjacent[1])
            # Adjacent tile must be empty 
            if board[new_row, new_col] == VACANT:
                empty_adjacent.append((new_row, new_col))
    
    return list(set(empty_adjacent))


def get_random_initial_action(board:np.ndarray) -> PlaceAction:

    x = randint(0, 9)
    y = randint(0, 9)
    relative_positions: list[tuple[int, int]] = choice(TETROMINOES)

    temp: list[tuple[int, int]] = []

    for position in relative_positions:
        new_row, new_col = get_cell_coords(x + position[0], y + position[1])
        temp.append((new_row, new_col))

    # If there are conflicts, shift the entire randomly generated tetromino 4 cells to the right
    position_index = 0
    if (board[temp[0][0], temp[0][1]] != VACANT) or (board[temp[1][0], temp[1][1]] != VACANT) or \
        (board[temp[2][0], temp[2][1]] != VACANT) or (board[temp[3][0], temp[3][1]] != VACANT):
        for position in temp:
            temp_row, temp_col = get_cell_coords(position[0] + CELLS, position[1])
            temp[position_index] = (temp_row, temp_col)
            position_index += 1

    return convert_to_place_action(temp)

def render(board: np.ndarray, use_color: bool=False, use_unicode: bool=False) -> str:
    """
    FOR DEBUGGING
    Returns a visualisation of the game board as a multiline string, with
    optional ANSI color codes and Unicode characters (if applicable).
    """
    def apply_ansi(str, bold=True, color=None):
        bold_code = "\033[1m" if bold else ""
        color_code = ""
        if color == "r":
            color_code = "\033[31m"
        if color == "b":
            color_code = "\033[34m"
        return f"{bold_code}{color_code}{str}\033[0m"

    output = ""
    for r in range(11):
        for c in range(11):
            if board[r, c] != 0:
                color: PlayerColor = PlayerColor.RED if board[r,c] == RED else PlayerColor.BLUE
                color = "r" if color == PlayerColor.RED else "b"
                text = f"{color}"
                if use_color:
                    output += apply_ansi(text, color=color, bold=False)
                else:
                    output += text
            else:
                output += "."
            output += " "
        output += "\n"
    return output
