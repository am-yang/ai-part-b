import numpy as np
from random import choice, randint
from copy import deepcopy

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
CELLS = 4
RED = 1
BLUE = 2
VACANT = 0

def possible_actions(board:np.ndarray, color:int) -> list[list[tuple[int, int]]]:
    '''
    Function that takes two args, a board representation, and the current player, 
    and outputs the list of posisble actions the current player can take
    '''
    children = []
    empty_adjacent_tiles: list[tuple[int, int]] = get_empty_adjacent_tiles(board, color)
    for tile in empty_adjacent_tiles:
        children += generate_tetrominoes(board, tile[0], tile[1])
    
    unique_children = [list(child) for child in set(tuple(child) for child in children)]

    return unique_children


def get_cell_coords(row: int, col: int) -> tuple[int, int]:

    new_row = row % BOARD_DIMENSION
    new_col = col % BOARD_DIMENSION

    return new_row, new_col


def generate_tetrominoes(board: np.ndarray, cell_row: int, cell_col: int) -> list[list[tuple[int, int]]]:
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


def get_empty_adjacent_tiles(board: np.ndarray, color: int) -> list[tuple[int, int]]:
    
    empty_adjacent: list[tuple[int, int]] = []
    for row in range(BOARD_DIMENSION):
        for col in range(BOARD_DIMENSION):
            # if current tile is not occupied by our player
            if board[row, col] != color:
                continue
            # now check if adjacent tiles are free
            for adjacent in ADJACENT:
                new_row, new_col = get_cell_coords(row + adjacent[0], col + adjacent[1])
                # Adjacent tile must be empty 
                if board[new_row, new_col] == VACANT:
                    empty_adjacent.append((new_row, new_col))
    return list(set(empty_adjacent))


def apply_move(board: np.ndarray, place_action: list[tuple[int, int]], color: int, make_copy: bool = False) -> np.ndarray:

    board_ref = deepcopy(board) if make_copy else board # make copy of board if necessary

    board_ref[place_action[0][0], place_action[0][1]] = board_ref[place_action[1][0], place_action[1][1]] = \
        board_ref[place_action[2][0], place_action[2][1]] = board_ref[place_action[3][0], place_action[3][1]] = color

    return board_ref
    


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
                color = "r" if board[r,c] == RED else "b"
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


board = np.zeros((11, 11), dtype=int)
board[3,1] = board[3,2] = board[4,1] = board[5,1] = RED

possible = sorted(possible_actions(board, RED))
print(str(len(possible)))

list_of_boards: list[np.ndarray] = []
for action in possible:
    temp = apply_move(board, action, RED, True)
    print(render(temp))

