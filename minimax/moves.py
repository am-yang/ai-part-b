import numpy as np
from random import choice, randint
from referee.game import PlaceAction, PlayerColor
from referee.game.coord import Coord


# Initialise board
TETROMINOES: list[list[tuple[int, int]]] = [
        # I shape
        [(0,0), (0,1), (0,2), (0,3)],[(0,-1), (0,0), (0,1), (0,2)], [(0,-2), (0,-1), (0,0), (0,1)], [(0,-3), (0,-2), (0,-1), (0,0)],

        [(0,0), (1,0), (2,0), (3,0)], [(-1,0), (0,0), (1,0), (2,0)],[(-2,0), (-1,0), (0,0), (1,0)],[(-3,0), (-2,0), (-1,0), (0,0)],

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

        [(0,0), (1,0), (1,1), (2,1)],[(0,0), (1,0), (0,-1), (-1,-1)],[(0,0), (0,1), (1,1), (-1,0)],[(0,0), (-1,0), (-1,-1), (-2,-1)],

        # O shape
        [(0,0), (0,1), (1,0), (1,1)],[(0,-1), (0,0), (1,-1), (1,0)],[(-1,0), (-1,1), (0,0), (0,1)],[(-1,-1), (-1,0), (0,-1), (0,0)],

        # T shape
        [(0,0), (0,1), (0,2), (1,1)],[(0,-1), (0,0), (0,1), (1,0)],[(0,-2), (0,-1), (0,0), (1,-1)],[(-1,-2), (-1,-1), (-1,0), (0,0)],

        [(0,0), (-1,1), (0,1), (1,1)],[(0,0), (1,0), (2,0), (1,-1)],[(0,0), (1,0), (0,-1), (-1,0)],[(0,0), (-1,0), (-2,0), (-1,-1)],

        [(0,0), (0,1), (0,2), (-1,1)],[(0,0), (1,0), (1,1), (1,-1)],[(0,0), (0,1), (0,-1), (-1,0)],[(0,0), (0,-1), (0,-2), (-1,-1)],

        [(0,0), (1,0), (2,0), (1,1)],[(0,0), (1,0), (0,1), (-1,0)],[(0,0), (-1,-1), (0,-1), (1,-1)],[(0,0), (-1,0), (-2,0), (-1,1)]
    ]

ADJACENT: list[tuple[int, int]] = [(1, 0), (-1, 0), (0, 1), (0, -1)]

BOARD_DIMENSION = 11
MAX_BOARD_INDEX = 10
MAX_EMPTY_ADJACENT = 10
CELLS = 4
SHIFT = 5
MAX_DEPTH = 150
RED = 1
BLUE = 2
VACANT = 0
TOO_LARGE_BRANCHING_FACTOR = 100

reached_opponent = False

def get_remaining_empty_tiles(
    opponent_tiles: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    
    return [(row, col) for row in range(BOARD_DIMENSION) for col in range(BOARD_DIMENSION) if (row, col) not in opponent_tiles]

def count_tiles(
    board: np.ndarray, 
    player: int
) -> int:
    count = 0
    for row in range(BOARD_DIMENSION):
        for col in range(BOARD_DIMENSION):
            if board[row, col] == player:
                count += 1
    return count

def possible_actions(
    board:np.ndarray, 
    color:int
) -> list[tuple[list[tuple[int, int]], np.ndarray, int, str]]:
    '''
    Function that takes two args, a board representation, and the current player, 
    and outputs the list of posisble actions the current player can take
    '''
    actions = []
    empty_adjacent_tiles: list[tuple[int, int]] = get_empty_adjacent_tiles(board, color)
    for tile in empty_adjacent_tiles:
        actions += generate_tetrominoes(board, tile[0], tile[1])
    
    unique_actions: list[list[tuple[int, int]]] = [list(action) for action in set(tuple(action) for action in actions)]

    # Group action with a specific ranking (AKA weight). Hence, our ranking list will contain elements of the form: (ranking, action, applied action state)
    children_ranking: list[tuple[tuple[int, int], list[tuple[int, int]], np.ndarray, str]] = []

    for action in unique_actions:
        action_applied_board = apply_move(board=board, place_action=None, color=None, place_action_list=action, color_as_int=color)
        board_as_bytes = action_applied_board.tobytes()
        ranking = rank_child(action, action_applied_board, color)
        children_ranking.append((ranking, action, action_applied_board))

    children_ranking = sorted(children_ranking)

    sorted_actions = [(action, state, -1 * (ranking[0] + ranking[1])) for (ranking, action, state) in children_ranking]
    return sorted_actions


def rank_child(
    action: list[tuple[int, int]], 
    board: np.ndarray, 
    color: int
) -> tuple[int, int]:
    
    '''
    Computes action weight. Action weight will compose of two components:
    #1: Number of player tiles 
    #2: Number of empty cells that are adjacent to player action

    Returns weight and board state
    (multiplied by -1 since we want to prioritise the maximal values, i.e., maximum player tile, maximum free adjacent tiles)
    '''

    count_player_tiles = 0
    free_adjacent_tiles: list[tuple[int, int]] = []

    for row in range(BOARD_DIMENSION):
        for col in range(BOARD_DIMENSION):
            if board[row, col] != color:
                continue
            count_player_tiles += 1
            for adjacent in ADJACENT:
                adjacent_tile = get_cell_coords(row + adjacent[0], col + adjacent[1])
                if board[adjacent_tile[0], adjacent_tile[1]] == VACANT:
                    free_adjacent_tiles.append(adjacent_tile)
    
    return count_player_tiles * -1, len(set(free_adjacent_tiles)) * -1



def get_cell_coords(
    row: int, 
    col: int
) -> tuple[int, int]:

    new_row = row % BOARD_DIMENSION
    new_col = col % BOARD_DIMENSION

    return new_row, new_col


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


def apply_move(
    board: np.ndarray, 
    color: PlayerColor = None, 
    place_action: PlaceAction = None, 
    place_action_list: list[tuple[int, int]] = None,
    color_as_int: int = 0
) -> np.ndarray:

    board_ref = np.copy(board)
    
    player = color_as_int
    if color:
        player = RED if color == PlayerColor.RED else BLUE

    action_as_list = convert_to_tuple_list(place_action) if place_action_list is None else place_action_list

    rows = [rows for rows, _ in action_as_list]
    cols = [cols for _, cols in action_as_list]

    for row, col in action_as_list:
        board_ref[row, col] = player
   
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
    color: int
) -> list[tuple[int, int]]:
    
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


def get_random_initial_action(
    board: np.ndarray,
    opponent_color: int = None,
    first_move: bool = True,
) -> PlaceAction:

    x = randint(0, 10)
    y = randint(0, 10)

    # Choose from pool of tetromino shapes that take up at least 2 rows/columns (exclude the I shape)
    random_position = randint(8, 75)
    relative_positions = TETROMINOES[random_position]

    action: list[tuple[int, int]] = []

    for position in relative_positions:
        new_row, new_col = get_cell_coords(x + position[0], y + position[1])
        action.append((new_row, new_col))

    if first_move:
        return convert_to_place_action(action)
    
    # If there is a clash with exisitng placement, or if it is placed right next to 
    # the opponent: shift action 4 cells down and across
    if (board[action[0][0], action[0][1]] != VACANT) or (board[action[1][0], action[1][1]] != VACANT) or \
        (board[action[2][0], action[2][1]] != VACANT) or (board[action[3][0], action[3][1]] != VACANT) or \
        adjacent_to_opponent(board, action, opponent_color):
        for cell in range(CELLS):
            new_row, new_col = get_cell_coords(action[cell][0] + SHIFT, action[cell][1] + SHIFT)
            action[cell] = (new_row, new_col)

    return convert_to_place_action(action)


def adjacent_to_opponent(
    board: np.ndarray, 
    action: list[tuple[int, int]], 
    opponent_color: int
) -> bool:
    empty_cells: list[tuple[int, int]] = []
    for cell in action:
        for position in ADJACENT:
            row, col = get_cell_coords(cell[0] + position[0], cell[1] + position[1])
            if board[row, col] == opponent_color:
                return True

    return False


def is_terminal_state(
    board: np.ndarray, 
    depth: int, 
    color: int
) -> bool:

    if depth == MAX_DEPTH:
        return True
    
    opponent = BLUE if color == RED else RED
    has_children = check_possible_actions(board, opponent)
    if not has_children:
        return True

    return False


def check_possible_actions(
    board:np.ndarray, 
    color:int
) -> bool:
    '''
    Function that takes two args, a board representation, and the current player, 
    and outputs TRUE if an action can be placed, and FALSE otherwise
    '''

    empty_adjacent_tiles: list[tuple[int, int]] = get_empty_adjacent_tiles(board, color)
    for tile in empty_adjacent_tiles:
        if check_possible_tetrominoes(board, tile[0], tile[1]):
            return True
    
    return False


def check_possible_tetrominoes(
    board: np.ndarray, 
    adjacent_row: int, 
    adjacent_col: int
) -> bool:
    for shape in TETROMINOES:
        tetromino = []
        for row, col in shape:
            new_row, new_col = get_cell_coords(row + adjacent_row, col + adjacent_col)
            if board[new_row, new_col] != VACANT:
                break
            else:
                tetromino.append((new_row, new_col))

        if len(tetromino) == CELLS:
            return True

    return False


def render(
    board: np.ndarray, 
    use_color: bool=False, 
    use_unicode: bool=False
) -> str:
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
