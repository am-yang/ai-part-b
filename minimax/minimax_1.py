from .moves import MAX_DEPTH, RED , BLUE, possible_actions, is_terminal_state, count_tiles, convert_to_place_action
import numpy as np
from referee.game import PlaceAction, PlayerColor
import time

MAX_TIME = 2.4
GREEDY_DEPTH = 1

class MiniMaxNode:

    def __init__(
        self, 
        color: int, 
        state: np.ndarray, 
        depth: int, 
        root_colour: int, 
        parent=None, 
        parent_action: list[tuple[int, int]]=None,
        weight: int = 0
    ):
        self.color: int = color
        self.state: np.ndarray = state
        self.parent: MiniMaxNode = parent
        self.parent_action: list[tuple[int, int]] = parent_action # action that led to this state
        self.children: list[MiniMaxNode] = None # List of immediate possible states from current state 
        self.depth: int = depth
        self.value: int = 0
        self.root_colour: int = root_colour
        self.weight = weight
        return


def get_minimax_action(
    state: np.ndarray,
    depth: int, 
    current_player: PlayerColor,
    allowed_time: float
) -> tuple[PlaceAction, float]:
    
    '''
    Entry point to minimax algorithm
    '''

    # Start timer 
    start_time = time.time()

    # initialise root node
    root_player = RED if current_player == PlayerColor.RED else BLUE
    opponent_player = BLUE if current_player == PlayerColor.RED else RED
    root_depth = depth - 1
    root_node = MiniMaxNode(
        color=opponent_player, 
        state=state, 
        depth=root_depth, 
        root_colour=root_player
    )

    root_node.children = init_children(root_node)

    explore_depth = MAX_DEPTH + 1
    num_children = len(root_node.children)
    # Many children and early on in the game 
    if num_children > 300 and root_node.depth < 20:
        explore_depth = GREEDY_DEPTH + 1
        
    # Perform iterative deepening 
    for curr_depth in range(1, explore_depth):
        max_value = minimax(
            node=root_node, 
            alpha=float('-inf'), 
            beta=float('inf'), 
            is_max=True, 
            explore_depth=curr_depth,
            start_time=start_time,
            allowed_time=allowed_time
        )
        elapsed_time = time.time() - start_time
        # Exit traversal if time limit exceeds, or if we reach a terminal state 
        if elapsed_time >= allowed_time or max_value == float('-inf') or max_value == float('inf'):
            break

    leftover_time = allowed_time - elapsed_time if elapsed_time < allowed_time else 0

    # Look for children with that maximum value
    for child in root_node.children:
        if child.value == max_value:
            return convert_to_place_action(child.parent_action), leftover_time
    
    
def minimax(node: MiniMaxNode, alpha: int, beta: int, is_max: bool, explore_depth: int, start_time: float, allowed_time: float):

    '''
    Minimax algorithm implementation
    '''

    if explore_depth == 0:
        return node.weight
    
    if is_terminal_state(board=node.state, depth=node.depth, color=node.color):
        if node.depth == MAX_DEPTH:
            count_root = count_tiles(node.state, node.root_colour)
            if count_root == 75:
                return 0
            elif count_root > 75:
                return float('inf')
            else:
                return float('-inf')
            
        # Check if our player was the one that made the last move 
        if node.root_colour == node.color:
            return float('inf')
        
        return float('-inf')
    
    if is_max:
        max_eval = float('-inf')
        
        # If we have no yet generated its children, do so now
        if node.children is None:
            node.children = init_children(node)
            
        for child in node.children:
            child.value = minimax(child, alpha, beta, False, explore_depth - 1, start_time, allowed_time)
            max_eval = max(max_eval, child.value)
            alpha = max(alpha, child.value)
            elapsed_time = time.time() - start_time
            if beta <= alpha or elapsed_time >= allowed_time:
                break 
        node.value = max_eval
        return max_eval

    else:
        min_eval = float('inf')

        if node.children is None:
            node.children = init_children(node)
        for child in node.children:
            child.value = minimax(child, alpha, beta, True, explore_depth - 1, start_time, allowed_time)
            min_eval = min(min_eval, child.value)
            beta = min(beta, child.value)
            elapsed_time = time.time() - start_time
            if beta <= alpha or elapsed_time >= allowed_time:
                break
        
        node.value = min_eval
        return min_eval


def init_children(node: MiniMaxNode):

    '''
    Function that initialises all child states from a given state
    '''

    children: list[MiniMaxNode] = []
    child_depth: int = node.depth + 1
    child_player: int = BLUE if node.color == RED else RED

    actions: list[tuple[list[tuple[int, int]], np.ndarray, int]] = possible_actions(node.state, child_player)
    for action in actions:
        new_node = MiniMaxNode(
            color=child_player, 
            state=action[1],
            depth=child_depth, 
            root_colour=node.root_colour,
            parent=node, 
            parent_action=action[0],
            weight=action[2]
        )
        children.append(new_node)
    return children