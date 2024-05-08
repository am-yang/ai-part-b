from .moves import MAX_DEPTH, RED , BLUE, convert_to_place_action, possible_actions, is_terminal_state, apply_move, get_empty_adjacent_tiles, render
from referee.game import PlayerColor, PlaceAction
from copy import deepcopy
import numpy as np

CUTOFF_DEPTH = 5
# In the context of chess: 4-ply lookahead is very average. Try to get to 5. 

class MiniMaxNode:

    def __init__(
        self, 
        color: int, 
        state: np.ndarray, 
        depth: int, 
        root_colour: int, 
        opponent_tiles:list[tuple[int, int]], # Knowing where opponent tiles are will help the maximising determine which child nodes to explore 
        player_tiles: list[tuple[int, int]], # Contrastingly, knowing where (root) player tiles are will help the minimising player
        parent=None, 
        parent_action: list[tuple[int, int]]=None
    ):
        self.color: int = color
        self.state: np.ndarray = state
        self.parent: MiniMaxNode = parent
        self.parent_action: list[tuple[int, int]] = parent_action # action that led to this state
        self.children: list[MiniMaxNode] = None
        self.depth: int = depth
        self.value: int = 0
        self.root_colour: int = root_colour
        self.opponent_tiles = opponent_tiles 
        self.player_tiles = player_tiles
        return


def evaluation(
    node: MiniMaxNode
) -> int:
    
    opponent_color = BLUE if node.root_colour == RED else RED
    
    if node.depth == MAX_DEPTH:

        opponent_occupied = node.opponent_tiles if node.color == node.root_colour else node.player_tiles
        count_opponent_tiles = len(opponent_occupied)

        if count_opponent_tiles > 75:
            return float('-inf')
        elif count_opponent_tiles < 75: 
            return float('inf')
        else: 
            return 0
        
    empty_opponent_tiles = get_empty_adjacent_tiles(node.state, opponent_color)
    return -1 * len(empty_opponent_tiles)
    # opponent_action = possible_actions(node.state, opponent_color, node.opponent_tiles, node.player_tiles, True)
    # return -1 * len(opponent_action)


def get_minimax_action(
    state: np.ndarray, 
    depth: int, 
    current_player: PlayerColor, 
    opponent_occupied: list[tuple[int, int]],
    player_occupied: list[tuple[int, int]],
    is_first_action: bool = False
) -> PlaceAction:

    # initialise root node
    root_player = RED if current_player == PlayerColor.RED else BLUE
    opponent_player = BLUE if current_player == PlayerColor.RED else RED
    root_depth = depth - 1
    root_node = MiniMaxNode(
        color=opponent_player, 
        state=state, 
        depth=root_depth, 
        root_colour=root_player, 
        opponent_tiles=player_occupied, 
        player_tiles=opponent_occupied
    )
    root_node.children = init_children(root_node, is_first_action)

    max_val = minimax(node=root_node, alpha=float('-inf'), beta=float('inf'), is_max=True, explore_depth=CUTOFF_DEPTH)

    action: list[tuple[int, int]] = []
    # Look for children with that maximum value
    for child in root_node.children:
        if child.value == max_val:
            action = child.parent_action
            break
    
    return convert_to_place_action(action)


def minimax(node: MiniMaxNode, alpha: int, beta: int, is_max: bool, explore_depth: int):
    
    if explore_depth == 0:
        eval = evaluation(node)
        return eval
    
    if is_terminal_state(board=node.state, depth=node.depth, color=node.color) and node.depth > 2:
        if node.depth == MAX_DEPTH:
            return evaluation(node)
        
        # Check if our player was the one that made the last move 
        if node.root_colour == node.color:
            return float('inf')
        
        return float('-inf')

    if is_max:
        max_eval = float('-inf')

        # If we have no yet generated its children, do so now
        if not node.children:
            node.children = init_children(node)
        # print("Depth: " + str(node.depth ) + ", num children: " + str(len(node.children)))
        for child in node.children:
            child.value = minimax(child, alpha, beta, False, explore_depth - 1)
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
        for child in node.children:
            child.value = minimax(child, alpha, beta, True, explore_depth - 1)
            min_eval = min(min_eval, child.value)
            beta = min(beta, child.value)
            if beta <= alpha:
                break
        
        node.value = min_eval
        return min_eval


def init_children(node: MiniMaxNode, is_first_action: bool = False):

    children: list[MiniMaxNode] = []
    child_depth: int = node.depth + 1
    child_player: int = BLUE if node.color == RED else RED

    actions: list[list[tuple[int, int]]] = possible_actions(node.state, child_player, node.player_tiles, node.opponent_tiles, is_first_action)
    for action in actions:
        player_occupied = deepcopy(node.opponent_tiles)
        player_occupied += action
        opponent_occupied = deepcopy(node.player_tiles)
        new_node = MiniMaxNode(
            color=child_player, 
            state=apply_move(
                board=node.state, 
                color=None, 
                place_action=None, 
                place_action_list=action, 
                color_as_int=child_player, 
                opponent_tiles=opponent_occupied, 
                player_tiles=player_occupied
            ), 
            depth=child_depth, 
            root_colour=node.root_colour, 
            opponent_tiles=player_occupied, 
            player_tiles=opponent_occupied, 
            parent=node, 
            parent_action=action
        )
        children.append(new_node)
    return children