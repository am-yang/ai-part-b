import numpy as np
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
MAX_DEPTH = 150
RED = 1
BLUE = 2
VACANT = 0
TOO_LARGE_BRANCHING_FACTOR = 100

reached_opponent = False

def possible_actions(
    board:np.ndarray, 
    color:int, 
    opponent_tiles: list[tuple[int, int]]
) -> list[list[tuple[int, int]]]:
    '''
    Function that takes two args, a board representation, and the current player, 
    and outputs the list of posisble actions the current player can take
    '''
    children = []
    empty_adjacent_tiles: list[tuple[int, int]] = get_empty_adjacent_tiles(board, color)
    for tile in empty_adjacent_tiles:
        children += generate_tetrominoes(board, tile[0], tile[1])
    
    unique_children = [list(child) for child in set(tuple(child) for child in children)]

    # if len(unique_children) == 0:
    #     string = "RED" if color == RED else "BLUE"
    #     print("Curr player is: " + string)
    #     print(render(board, True))

    # Storing actions and their corresponding values in a dict. Since some actions may have the same value, our dict value will be of type list
    children_ranking: dict[int, list[list[tuple[int, int]]]] = {} 
    for children in unique_children:
        ranking = evaluate_child(children, opponent_tiles, board, color)
        if ranking not in children_ranking:
            children_ranking[ranking] = [children]
        else:
            children_ranking[ranking].append(children)

    smallest_heuristic = min(children_ranking.keys())

    # If branching factor is too large, perform another heuristic evaluation
    if (len(children_ranking[smallest_heuristic]) >= MAX_BOARD_INDEX):
        # Part 3 calculate the furthest manhattan distance from the opponent 
        eval_3 = furthest_distance(children, opponent_tiles, board, color)

    return children_ranking[smallest_heuristic]


def evaluate_child(
    action: list[tuple[int, int]], 
    opponent_tiles: list[tuple[int, int]],
    board: np.ndarray,
    curr_player: int
) -> int:
    '''
    Function that returns a heuristic value for a child state 
    We evaluate the 'usefulness' of the child. That is, how much we are able to block off the opponent from making potential actions. Our filtering mechanism
    helps, because we don't want to waste time visiting moves that take us further from the goal (of blocking the opponent)
    
    The ranking consists of two parts (added together):

    Part 1:
    The manhattan distance of us from the nearest opponent tile. 
    
    Part 2:
    The number of tiles adjacent to the opponent that are blocked off (thereby limiting potential moves) 

    Part 3:
    Minimise the furthest distance from opponent. Say that no moves can further fill an opponenent's adjacent tile,
    try to determine the furthest distance from the opponent (so that we are continuously moving closer to the opponent) 
    and choose the node with the minimal furthest distance
    '''

    # Part 1 manhattan distance calculation
    eval_1 = get_manhattan_distance(action=action, opponent_tiles=opponent_tiles)

    # Part 2 number of adjacent tiles (to opponent) that are free
    eval_2 = count_free_adjacent_opponent_tiles(action=action, opponent_tiles=opponent_tiles, board=board, curr_player=curr_player)

    return eval_1 + eval_2


def furthest_distance(
    actions: list[list[tuple[int, int]]], 
    opponent_tiles: list[tuple[int, int]],
    board: np.ndarray,
    curr_player: int
) -> int:
    
    max_distance = 0
    for action in actions:
        curr_distance = get_manhattan_distance(action=action, opponent_tiles=opponent_tiles)
        if curr_distance > max_distance:
            max_distance = curr_distance
    
    return max_distance
    



def get_manhattan_distance(
    action: list[tuple[int, int]], 
    opponent_tiles: list[tuple[int, int]],
) -> int:
    '''
    Part 1 manhattan distance calculation between us and the nearest opponent
    '''
    min_manhattan_distance = BOARD_DIMENSION + BOARD_DIMENSION
    global reached_opponent
    if not reached_opponent:
        c1, c2, c3, c4 = action
        for tile in opponent_tiles:
            first_coord_distance = get_min_distance(tile[0], tile[1], c1[0], c1[1])
            second_coord_distance = get_min_distance(tile[0], tile[1], c2[0], c2[1])
            third_coord_distance = get_min_distance(tile[0], tile[1], c3[0], c3[1])
            fourth_coord_distance = get_min_distance(tile[0], tile[1], c4[0], c4[1])
            min_manhattan_distance = min(min_manhattan_distance, first_coord_distance, second_coord_distance, third_coord_distance, fourth_coord_distance)
            if min_manhattan_distance <= 1:
                reached_opponent = True
                break
    else:
        min_manhattan_distance = 1
    
    return min_manhattan_distance


def get_min_distance(
    opponent_row: int,
    opponent_col: int,
    player_row: int,
    player_col: int
) -> int:
    '''
    Helper that returns the shortest cell distance between two rows and two columns
    While computing abs(x - y) would have sufficed, we need to take into account the torus behavior of the board
    '''
    row_distance_1 = abs(opponent_row - player_row)
    row_distance_2 = (MAX_BOARD_INDEX - opponent_row) + player_row if player_row < opponent_row else (MAX_BOARD_INDEX - player_row) + opponent_row

    col_distance_1 = abs(opponent_col - player_col)
    col_distance_2 = (MAX_BOARD_INDEX - opponent_col) + player_col if player_col < opponent_col else (MAX_BOARD_INDEX - player_col) + opponent_col

    return min(row_distance_1, row_distance_2) + min(col_distance_1, col_distance_2) 


def count_free_adjacent_opponent_tiles(
    action: list[tuple[int, int]], 
    opponent_tiles: list[tuple[int, int]],
    board: np.ndarray,
    curr_player: int
) -> int:
    '''
    Part 2 number of adjacent tiles that are free
    '''
    free_adjacent_tiles: list[tuple[int, int]] = []
    action_applied_board = apply_move(board=board, place_action=None, color=None, place_action_list=action, color_as_int=curr_player)
    for tile in opponent_tiles:
        for adjacent in ADJACENT:
            adjacent_tile = get_cell_coords(tile[0] + adjacent[0], tile[1] + adjacent[1])
            if action_applied_board[adjacent_tile[0], adjacent_tile[1]] == VACANT:
                free_adjacent_tiles.append(adjacent_tile)
    
    return len(set(free_adjacent_tiles))


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
    color_as_int: int = 0,
    opponent_tiles: list[tuple[int, int]] = None,
    player_tiles: list[tuple[int, int]] = None
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
        # Also update our list of player/opponent tiles 
        if player_tiles and opponent_tiles:
            for col in range(BOARD_DIMENSION):
                if (row, col) in player_tiles:
                    player_tiles.remove((row, col))
                if (row, col) in opponent_tiles:
                    opponent_tiles.remove((row, col))

    for col in clear_out_col:
        board_ref[:, col] = VACANT
        if player_tiles and opponent_tiles:
            for row in range(BOARD_DIMENSION):
                if (row, col) in player_tiles:
                    player_tiles.remove((row, col))
                if (row, col) in opponent_tiles:
                    opponent_tiles.remove((row, col))

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
    board:np.ndarray
) -> PlaceAction:

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


# def count_colors(
#     board: np.ndarray, 
#     color: int
# ) -> int:
#     count = 0
#     for row in range(BOARD_DIMENSION):
#         for col in range(BOARD_DIMENSION):
#             if board[row,col] == color:
#                 count += 1
#     return count


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
