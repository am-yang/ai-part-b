from .moves import all_possible_moves, is_terminal_state, apply_move, count_colors
from referee.game import PlayerColor, Coord, PlaceAction

class MiniMaxNode:

    def __init__(self, color: PlayerColor, state: dict[Coord, PlayerColor], depth: int, parent=None, parent_action=None):
        self.color: PlayerColor = color
        self.state: dict[Coord, PlayerColor]= state
        self.parent: MiniMaxNode = parent
        self.parent_action: PlaceAction = parent_action # action that led to this state
        self.children: list[MiniMaxNode] = None
        self.depth: int = depth
        return


def init_children(node: MiniMaxNode):
    if is_terminal_state(node.state, node.color, node.depth):
        return None
    
    # Array that stores info about the current state's children
    child_nodes: list[MiniMaxNode] = []
    child_depth = 1 + node.depth
    child_player = node.color
    if node.depth != 0 and node.color == PlayerColor.RED:
        child_player = PlayerColor.BLUE
    elif node.depth != 0 and node.color == PlayerColor.BLUE:
        child_player = PlayerColor.RED
    
    possible_actions = all_possible_moves(node.state, child_depth, child_player)

    for action in possible_actions:
        board = apply_move(node.state, action, child_player)
        child_nodes.append(MiniMaxNode(color=child_player, state=board, depth=child_depth, parent=node, parent_action=action))

    node.children = child_nodes


def minimax_decision(node):

    max_val = float('-inf')
    best_action = None

    init_children(node)  # Generate possible moves and resulting states

    for child in node.children:
        value = minimax_value(child, child.color)
        if value > max_val:
            max_val = value
            best_action = child.parent_action # child.parent_action is the operator used to generate this child

    return best_action

def minimax_value(node, current_player): #Passing in depth as parameter 
    if is_terminal_state(node.state): # ❓ Question: If the depth is already counted in terminal state function, how should we incorporate 150 turns 
        return utility(node, current_player)
    
    # Check the case where the game ends at 150 turns 
    if node.depth == 150:
        count = count_colors(node.color)
        if count > 75:
            return 1
    elif count == 75: 
        return 0
    else: 
        return -1

    if current_player == node.color: # ❓ Question: How do we keep track of the initial state node colour? 
        depth += 1  
        return max(minimax_value(child, node.color) for child in node.children)
    else:
        depth += 1 
        return min(minimax_value(child, node.color) for child in node.children)
    
def utility(node, current_player):
    #❓ Question: How do we keep track of the initial state node colour? 
    if current_player != node.color : # Stopping at minimizer's turn - Opponent has no more moves to make, we win
        return 1
    if current_player == node.color: # Stopping at maximizer's turn - We have no more moves to make, we lose
        return -1