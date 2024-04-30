import math
import random
from .moves import all_possible_moves, is_terminal_state, apply_move, count_colors
from referee.game import PlayerColor, Coord, PlaceAction

UCB_CONSTANT = 1
TIME_LIMIT = 100

class MCTSNode:

    def __init__(self, color: PlayerColor, state: dict[Coord, PlayerColor], depth: int, is_first_move: bool = False, parent=None, parent_action=None):
        self.color: PlayerColor = color
        self.state: dict[Coord, PlayerColor]= state
        self.parent: MCTSNode = parent
        self.parent_action: PlaceAction = parent_action # action that led to this state
        self.children: list[MCTSNode] = None
        self.wins: int = 0
        self.num_visits: int = 0
        self.depth: int = depth
        self.ucb_score: float = 0
        self.is_first_move = is_first_move
        return
    

def calculate_ucb(node: MCTSNode) -> float:
    if node.visited_count == 0:
        return float('inf')
    
    if node.parent:
        return (node.wins / float(node.visited_count)) + UCB_CONSTANT * math.sqrt(math.log(node.parent.visited_count) / float(node.visited_count)) 
    else:
        return (node.wins / float(node.visited_count)) + UCB_CONSTANT * math.sqrt(math.log(node.parent.visited_count) / float(node.visited_count)) 


def init_children(node: MCTSNode):
    if is_terminal_state(node.state, node.depth):
        return None
    
    # Array that stores info about the current state's children
    child_nodes: list[MCTSNode] = []
    curr_depth = 1 + node.depth
    child_player = node.color
    if node.state != {} and node.color == PlayerColor.RED:
        child_player = PlayerColor.BLUE
    elif node.state != {} and node.color == PlayerColor.BLUE:
        child_player = PlayerColor.RED
    
    possible_actions = all_possible_moves(node.state, curr_depth, child_player)

    for action in possible_actions:
        board = apply_move(node.state, action, child_player)
        child_nodes.append(MCTSNode(color=child_player, state=board, depth=curr_depth, parent=node, parent_action=action))

    node.children = child_nodes

def simulation(
    node: MCTSNode
) -> int:
    '''
    A random playout of the current node, which will return a value representing the outcome. 
    '''
    board: list[Coord, PlayerColor] = {key: value for key, value in node.state.items()}
    depth: int = node.depth
    curr_player = node.turn # also keep track of whose turn it is
    self_won = False

    while not is_terminal_state(board, node.color, depth):
        
        possible_actions = all_possible_moves(board, depth, curr_player)

        random_action = random.choice(possible_actions)

        board = apply_move(board, random_action)

        # Alternate turns
        curr_player = PlayerColor.BLUE if curr_player == PlayerColor.RED else PlayerColor.RED

        depth += 1
    
    # Check who won the simulation 
    if depth == 150:
        count = count_colors(node.turn)
        if count > 75:
            self_won = True
    else:
        # if the game ended on a player's turn (i.e., before they could make another move), then the opponent wins
        if curr_player != node.turn:
            self_won = True

    if self_won:
        return 1
    else:
        return 0

def selection(
    node: MCTSNode
) -> MCTSNode:
    curr_node = node
    # Keep traversing down tree until we reach leaf
    while curr_node.children:
        children = curr_node.children
        max_child = children[0] 
        # Find the child with the highest UCB value
        for child in children:
            if child.calculate_ucb() > max_child.calculate_ucb():
                max_child = child

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
