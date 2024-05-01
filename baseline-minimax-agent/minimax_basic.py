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
    if is_terminal_state(node.state, node.depth):
        return None
    
    # Array that stores info about the current state's children
    child_nodes: list[MiniMaxNode] = []
    curr_depth = 1 + node.depth
    child_player = node.color
    if node.state != {} and node.color == PlayerColor.RED:
        child_player = PlayerColor.BLUE
    elif node.state != {} and node.color == PlayerColor.BLUE:
        child_player = PlayerColor.RED
    
    possible_actions = all_possible_moves(node.state, curr_depth, child_player)

    for action in possible_actions:
        board = apply_move(node.state, action, child_player)
        child_nodes.append(MiniMaxNode(color=child_player, state=board, depth=curr_depth, parent=node, parent_action=action))

    node.children = child_nodes

def minimax_decision(node):
    # Assuming node contains the current game state and the current player's turn
    max_val = float('-inf')
    best_action = None
    init_children(node)  # Generate possible moves and resulting states

    for child in node.children:
        # child.parent_action is the operator used to generate this child
        value = minimax_value(child, child.color)
        if value > max_val:
            max_val = value
            best_action = child.parent_action

    return best_action

def minimax_value(node, current_player): #Passing in depth as parameter 
    if is_terminal_state(node.state):
        return utility(node.state, current_player)
    
    # TO-DO: Check the case where the game ends at 150 turns 
    if node.depth == 150:
        count = count_colors(node.turn)
        if count > 75:
            return 1
    elif count == 75: 
        return 0
    else: 
        return -1

    init_children(node)  # Make sure all possible moves from this state are explored

    if maximizer_turn: # TO-DO: Define what does it mean by when it's maximizer's turn
        depth += 1  
        return max(minimax_value(child, node.color) for child in node.children)
    else:
        depth += 1 
        return min(minimax_value(child, node.color) for child in node.children)
    
def utility(board, current_player):
    if minimizer_turn : # TO-DO: Define what does it mean by turn 
        return 1
    if maximizer_turn: # TO-DO: Define what does it mean by when it's maximizer's turn 
        return -1