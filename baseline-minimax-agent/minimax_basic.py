from .moves import all_possible_moves, is_terminal_state, apply_move, count_colors, TETROMINOES
from referee.game import PlayerColor, Coord, PlaceAction
import time

CUTOFF_DEPTH = 3

class MiniMaxNode:

    def __init__(self, color: PlayerColor, state: dict[Coord, PlayerColor], depth: int, root_colour: PlayerColor, parent=None, parent_action=None):
        self.color: PlayerColor = color
        self.state: dict[Coord, PlayerColor]= state
        self.parent: MiniMaxNode = parent
        self.parent_action: PlaceAction = parent_action # action that led to this state
        self.children: list[MiniMaxNode] = None
        self.depth: int = depth
        self.value: int = 0
        self.root_colour = root_colour
        return

def init_children(node: MiniMaxNode):
    if is_terminal_state(node.state, node.color, node.depth):
        return None
    # Array that stores info about the current state's children
    child_nodes: list[MiniMaxNode] = []
    child_depth = 1 + node.depth
    child_player = None
    if node.color == PlayerColor.BLUE:
        child_player = PlayerColor.RED
    else:
        child_player = PlayerColor.BLUE
    
    possible_actions = all_possible_moves(node.state, child_player)

    for action in possible_actions:
        board = apply_move(node.state, action, child_player)
        child_nodes.append(MiniMaxNode(color=child_player, state=board, depth=child_depth, root_colour=node.root_colour, parent=node, parent_action=action))

    node.children = child_nodes

def minimax(node: MiniMaxNode) -> MiniMaxNode:
    time_start = time.perf_counter()
    init_children(node)

    max_val = float('-inf')
    best_child = None

    if not node.children:
        return None

    for child in node.children:
        val = maximise(child, float('-inf'), float('inf'), time_start)
        if val >= max_val:
            max_val = val
            best_child = child

    return best_child 


def maximise(node: MiniMaxNode, alpha: int, beta: int, time_start: float) -> int:

    if node.depth == CUTOFF_DEPTH:
        return evaluation(node, node.root_colour)
     
    if is_terminal_state(node.state, node.color, node.depth) or (time.perf_counter() - time_start > 0.04):
        return utility(node, node.root_colour, node.depth)

    init_children(node)

    max_val = float('-inf')

    for child in node.children:
        max_val = max(max_val, minimise(child, alpha, beta))

        if max_val >= beta:
            break
        alpha = max(max_val, alpha)

    return max_val

def minimise(node: MiniMaxNode, alpha: int, beta: int, time_start: float) -> int:

    if node.depth == CUTOFF_DEPTH:
        return evaluation(node, node.root_colour)
    
    if is_terminal_state(node.state, node.color, node.depth) or (time.perf_counter() - time_start) > 20:
        return utility(node, node.root_colour, node.depth)

    init_children(node)

    min_val = float('inf')

    for child in node.children:
        min_val = min(min_val, maximise(child, alpha, beta))

        if min_val <= alpha:
            break
        beta = min(min_val, beta)

    return min_val


# def minimax_decision(
#     player_color: PlayerColor,
#     curr_state: dict[Coord, PlayerColor],
#     depth: int
# ) -> PlaceAction | None:

#     max_val = float('-inf')
#     best_action = None

#     root_node = MiniMaxNode(color=player_color, state=curr_state, depth=depth)
#     root_player_color = player_color

#     init_children(root_node)  # Generate possible moves and resulting states
#     for child in root_node.children:
#         value = minimax_value(child, root_player_color) 
#         if value > max_val:
#             max_val = value
#             best_action = child.parent_action # child.parent_action is the operator used to generate this child

#     return best_action

# def minimax_value(node: MiniMaxNode, root_player_color: PlayerColor) -> int:
#     # if is_terminal_state(node.state, node.color, node.depth):
#     #     return utility(node, root_player_color, node.depth)
#     if node.depth == CUTOFF_DEPTH:
#         return evaluation(node, root_player_color)
    
#     init_children(node)
    
#     if node.color == root_player_color: 
#         return max(minimax_value(child, root_player_color) for child in node.children)
#     else:
#         return min(minimax_value(child, root_player_color) for child in node.children)
    
def utility(node: MiniMaxNode, root_player_color: PlayerColor, depth: int) -> int:

    # Check the case where the game ends at 150 turns 
    if depth == 150:
        count = count_colors(node.state, node.color)
        if count > 75:
            return 1
        elif count == 75: 
            return 0
        else: 
            return -1

    if node.color != root_player_color: # Stopping at minimizer's turn - Opponent has no more moves to make, we win
        return 1
    else: # Stopping at maximizer's turn - We have no more moves to make, we lose
        return -1
    

def evaluation(
    node: MiniMaxNode, 
    root_player_color: PlayerColor
) -> int:
    
    opponent_color = PlayerColor.BLUE if root_player_color == PlayerColor.RED else PlayerColor.RED
    moves = all_possible_moves(node.state, opponent_color)

    return len(moves)


def render(board: dict[Coord, PlayerColor], use_color: bool=False, use_unicode: bool=False) -> str:
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
            coord = Coord(r, c)
            if coord in board:
                color: PlayerColor = board[coord]
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
