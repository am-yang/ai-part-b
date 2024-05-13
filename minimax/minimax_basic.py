from .moves import MAX_DEPTH, RED , BLUE, convert_to_place_action, possible_actions, is_terminal_state, apply_move, get_empty_adjacent_tiles, render, count_tiles
from referee.game import PlayerColor, PlaceAction
from copy import deepcopy
import numpy as np

CUTOFF_DEPTH = 4
# In the context of chess: 4-ply lookahead is very average. Try to get to 5. 

class MiniMaxNode:

    def __init__(
        self, 
        color: int, 
        state: np.ndarray, 
        depth: int, 
        root_colour: int, 
        parent=None, 
        parent_action: list[tuple[int, int]]=None,
        weight: int = 0,
    ):
        self.color: int = color
        self.state: np.ndarray = state
        self.parent: MiniMaxNode = parent
        self.parent_action: list[tuple[int, int]] = parent_action # action that led to this state
        self.children: dict[str, MiniMaxNode] = None
        self.depth: int = depth
        self.value: int = 0
        self.root_colour: int = root_colour
        self.weight = weight
        return


def get_minimax_action(
    root_node: MiniMaxNode
) -> MiniMaxNode:
    
    if root_node.children is None:
        root_node.children = init_children(root_node)

    depth = CUTOFF_DEPTH
    num_children = len(root_node.children)
    if num_children > 200:
        depth = 2
    elif num_children > 20:
        depth = 3

    max_val = minimax(node=root_node, alpha=float('-inf'), beta=float('inf'), is_max=True, explore_depth=depth)

    # Look for children with that maximum value
    for child in root_node.children.values():
        if child.value == max_val:
            return child
    

def minimax(node: MiniMaxNode, alpha: int, beta: int, is_max: bool, explore_depth: int):
    
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
    
    if explore_depth == 0:
        return node.weight

    if is_max:
        max_eval = float('-inf')

        # If we have no yet generated its children, do so now
        if not node.children:
            node.children = init_children(node)
        # print("Depth: " + str(node.depth) + ", num children: " + str(len(node.children)))
        for child in node.children.values():
            child.value = minimax(child, alpha, beta, False, explore_depth - 1)
            # print("Child depth: " + str(child.depth) + ", eval" + str(child.value))
            max_eval = max(max_eval, child.value)
            alpha = max(alpha, child.value)
            if beta <= alpha:
                break 
        node.value = max_eval
        return max_eval

    else:
        min_eval = float('inf')

        if not node.children:
            node.children = init_children(node)
        # print("Depth: " + str(node.depth ) + ", num children: " + str(len(node.children)))
        # print(render(node.state, True))
        for child in node.children.values():
            child.value = minimax(child, alpha, beta, True, explore_depth - 1)
            # print("Child depth: " + str(child.depth) + ", eval" + str(child.value))
            min_eval = min(min_eval, child.value)
            beta = min(beta, child.value)
            if beta <= alpha:
                break
        
        node.value = min_eval
        return min_eval


def init_children(node: MiniMaxNode):

    children: dict[str, MiniMaxNode] = {}
    child_depth: int = node.depth + 1
    child_player: int = BLUE if node.color == RED else RED

    actions: list[tuple[list[tuple[int, int]], np.ndarray, int, str]] = possible_actions(node.state, child_player)
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
        hash = action[3]
        children[hash]= new_node
    return children