import math
import random
from .moves import all_possible_moves, is_terminal_state, apply_move, count_colors
from referee.game import PlayerColor, Coord, PlaceAction
import ast

UCB_CONSTANT = 1
TIME_LIMIT = 50

class MCTSNode:

    def __init__(self, color: PlayerColor, state: dict[Coord, PlayerColor], depth: int, parent=None, parent_action=None):
        self.color: PlayerColor = color
        self.state: dict[Coord, PlayerColor]= state
        self.parent: MCTSNode = parent
        self.parent_action: PlaceAction = parent_action # action that led to this state
        self.children: list[MCTSNode] = None
        self.wins: int = 0
        self.num_visits: int = 0
        self.depth: int = depth
        self.ucb_score: float = 0
        return
    

def calculate_ucb(node: MCTSNode) -> float:
    if node.num_visits == 0:
        return float('inf')
    
    if node.parent:
        return (node.wins / float(node.num_visits)) + UCB_CONSTANT * math.sqrt(math.log(node.parent.num_visits) / float(node.num_visits)) 
    else:
        return (node.wins / float(node.num_visits)) + UCB_CONSTANT * math.sqrt(math.log(node.parent.num_visits) / float(node.num_visits)) 


def init_children(node: MCTSNode):
    if is_terminal_state(node.state, node.color, node.depth):
        return None
    
    # Array that stores info about the current state's children
    child_nodes: list[MCTSNode] = []
    child_depth = 1 + node.depth
    child_player = node.color
    if node.depth != 0 and node.color == PlayerColor.RED:
        child_player = PlayerColor.BLUE
    elif node.depth != 0 and node.color == PlayerColor.BLUE:
        child_player = PlayerColor.RED
    
    possible_actions = all_possible_moves(node.state, child_depth, child_player)

    for action in possible_actions:
        board = apply_move(node.state, action, child_player)
        child_nodes.append(MCTSNode(color=child_player, state=board, depth=child_depth, parent=node, parent_action=action))

    node.children = child_nodes

def simulation(
    node: MCTSNode
) -> int:
    '''
    A random playout of the current node, which will return a value representing the outcome. 
    '''
    board: list[Coord, PlayerColor] = {key: value for key, value in node.state.items()}
    depth: int = node.depth
    curr_player = node.color # also keep track of whose turn it is
    self_won = False

    while not is_terminal_state(board, node.color, depth):
        print(render(board, use_color=True))
        print("depth: " + str(depth) + ", color: " + str(curr_player))

        # Alternate turns
        curr_player = PlayerColor.BLUE if curr_player == PlayerColor.RED else PlayerColor.RED
        depth += 1
        possible_actions = all_possible_moves(board, depth, curr_player)

        random_action = random.choice(possible_actions)

        board = apply_move(board, random_action, curr_player)

    
    # Check who won the simulation 
    if depth == 150:
        count = count_colors(node.color)
        if count > 75:
            self_won = True
    else:
        # if the game ended on a player's turn (i.e., before they could make another move), then the opponent wins
        if curr_player != node.color:
            self_won = True

    if self_won:
        print(str(node.color) + " WON this simulation")
        return 1
    else:
        print(str(node.color) + " LOST this simulation")
        return 0

def selection(
    node: MCTSNode
) -> MCTSNode:
    curr_node = node
    # Keep traversing down tree until we reach leaf
    while curr_node.children:
        children = curr_node.children
        max_child = children[0] 
        max_ucb = calculate_ucb(max_child)
        # Find the child with the highest UCB value
        for child in children:
            child_ucb = calculate_ucb(child)
            if child_ucb > max_ucb:
                max_child = child
                max_ucb = child_ucb

        # Path to child chosen
        curr_node = max_child
    return curr_node

def expansion(
    node: MCTSNode
) -> MCTSNode:
    '''
    Function that chooses a child at random to perform rollout
    '''
    if not node.children:
        init_children(node)
    
    child = random.choice(node.children)

    return child


def backpropagate(
    result: int,
    node: MCTSNode
):

    # First update child node 
    node.num_visits += 1
    node.wins += result

    # Now recursively update parent 

    parent = node.parent

    while parent:
        parent.num_visits += 1

        result = 0 if result == 1 else 1
        
        parent.wins += result

        parent = parent.parent


def monte_carlo_tree_search(
    player_color: PlayerColor,
    curr_state: dict[Coord, PlayerColor],
    depth: int
) -> PlaceAction | None:

    tree = MCTSNode(color=player_color, state=curr_state, depth=depth)

    for time in range(TIME_LIMIT):
        leaf = selection(tree)
        child = expansion(leaf)
        outcome = simulation(child)
        backpropagate(outcome, child)

    max_ucb = float('-inf')
    max_ucb_action = None

    for child in tree.children:
        child_ucb = child.calculate_ucb()
        if child_ucb > max_ucb:
            max_ucb = child_ucb
            max_ucb_action = child.parent_action
    
    return max_ucb_action



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
