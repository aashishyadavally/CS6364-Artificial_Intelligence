"""Utility functions used in ``search`` module.
"""

import heapq
from copy import deepcopy


ACTIONS = ['up', 'down', 'left', 'right']


def read_states(filename):
    """Parses input and goal states from .txt file in 'filename'.

    Arguments:
        filename (str):
            Path to input .txt file.

    Returns:
        tuple(search.utils.State, search.utils.State):
            Input state, goal state.
    """
    with open(filename, 'r') as fileobj:
        contents = fileobj.readlines()
        _input, goal = contents[0].split(), contents[1].split()
    return State(_input), State(goal)


def get_child(parent, action):
    """Computes neighbour state resulting from action on 'parent'
    state.

    Arguments:
        parent (search.utils.State):
            Current state.

        action (str):
            One of 'up', 'down', 'left' and 'right'.
            Indicates move for the current state. Returns None
            if move is not possible.

    Returns:
        (search.utils.State or None)
            Resultant state following action.
            None, if move is not possible.
    """
    child = deepcopy(parent.config)

    for x, row in enumerate(child):
        if '*' in row:
            y = row.index('*')
            break

    if action == 'up':
        next_x, next_y = x-1, y
    elif action == 'down':
        next_x, next_y = x+1, y
    elif action == 'left':
        next_x, next_y = x, y-1
    elif action == 'right':
        next_x, next_y = x, y+1

    if all(_next in [0, 1, 2] for _next in [next_x, next_y]):
        child[next_x][next_y], child[x][y] = child[x][y], child[next_x][next_y]
        _list = [x for sublist in child for x in sublist]
        return State(_list)
    else:
        return None


def get_children(parent):
    """Computes all neighbor states of the current state.

    Arguments:
        parent (search,utils.State):
            Current state.

    Returns:
        children (list):
            List of possible neighbour states.
    """
    children = [get_child(parent, action) for action in ACTIONS]
    children = list(filter(lambda x: x is not None, children))
    return children


def goal_check(current, goal):
    """Check whether 'current' state is same as 'goal' state.

    Arguments:
        current (search.utils.State):
            Current state.
        goal (search.utils.State):
            Goal state.

    Returns:
        (bool):
            True, if current state is same as goal state, else, False.
    """
    current = [item for sublist in current.config for item in sublist]
    goal = [item for sublist in goal.config for item in sublist]

    if current == goal:
        return True
    else:
        return False


def number_of_misplaced(current, goal):
    """Compute number of misplaced tiles in current state of eight-puzzle
    relative to goal state.

    Arguments:
        current (search.utils.State):
            Current state.
        goal (search.utils.State):
            Goal state.

    Returns:
        (int):
            Number of misplaced tiles in 'current' state w.r.t 'goal' state.
    """
    current = [item for sublist in current.config for item in sublist]
    goal = [item for sublist in goal.config for item in sublist]
    return len([x for x, y in zip(current, goal) if x != y])


def _manhattan_distance(point1, point2):
    """Computes Manhattan distance between two points in 2D plane.

    Arguments:
        point1 (list):
            Point 1 in 2D plane.
        point2 (list):
            Point 2 in 2D plane.

    Returns:
        (float):
            Manhattan distance between the two points.
    """
    return abs(point1[0] - point2[0]) +\
           abs(point1[1] - point2[1])


def manhattan(current, goal):
    """Computes Manhattan distance between the current state and
    the goal state of the Eight-Puzzle problem.

    Arguments:
        current (search.utils.State):
            Current state.
        goal (search.utils.State):
            Goal state.

    Returns:
        distance (int):
            Manhattan distance.
    """
    current_indices, goal_indices = {}, {}
    distance = 0

    for x in range(3):
        for y in range(3):
            current_element = current.config[x][y]
            goal_element = goal.config[x][y]
            if current_element != '*':
                current_indices[current_element] = [x, y]
            if goal_element != '*':
                goal_indices[goal_element] = [x, y]

    for x in range(1, 9):
        distance += _manhattan_distance(current_indices[str(x)],
                                        goal_indices[str(x)])
    return distance


class State:
    """Data structure implementing a possible state of the
    Eight-Puzzle problem.

    Parameters:
        config (list):
            List of lists, representing state of eight-puzzle problem.
    """
    def __init__(self, _input):
        """Initializes :class: ``State``.

        Arguments:
            _input (list):
                List of numbered tile positions.
        """
        self.config = [_input[0:3], _input[3:6], _input[6:9]]

    def show(self):
        """Pretty prints state configuration.
        """
        for row in self.config:
            print(row)
        print('')


class Node:
    """Node data structure useful for uninformed search strategies
    such as Breadth First Search (BFS), Depth First Search (DFS) and
    Iterative Deepening Search (IDS).

    Parameters:
        state (search.utils.State):
            Current state.
        parent (search.utils.State):
            Predecessor state.
        depth (int):
            Depth of current state w.r.t start state.
    """
    def __init__(self, current, parent, depth):
        """Initializes :class: ``Node``.
        """
        self.state = current
        self.parent = parent
        self.depth = depth

    @property
    def children(self):
        """Neibhour states of the current ``search.utils.State`` state
        in the Eight-Puzzle problem.

        Returns:
            children (list):
                List of neighbour :class: ``search.utils.State`` states.
        """
        children = [Node(child, self, self.depth + 1) \
                    for child in get_children(self.state)]
        return children

    def __key(self):
        _config = tuple(tuple(x) for x in self.state.config)
        return tuple(_config)

    def __eq__(self, other):
        if isinstance(other, self.__class__) and \
           self.__key() == other.__key():
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__key())


class PriorityQueue:
    """Implements priority queue data structure using heaps.
    :func: ``heapq.heapify`` is an in-place operation.
    
    Parameters:
        heap (list):
            List of nodes.
    """
    def __init__(self, nodes):
        """Initializes :class: ``PriorityQueue``.

        Arguments:
            nodes (list):
                List of :class: ``search.utils.Node`` nodes.
        """
        self.heap = nodes
        heapq.heapify(self.heap)

    def add(self, node):
        """Adds node to the heap data structure.

        Arguments:
            node (search.astar.Node):
                Node for A-Star algorithm
        """
        self.heap.append(node)
        heapq.heapify(self.heap)

    def pop(self):
        """Pops minimum element from the heap data structure.

        Returns:
            element (search.astar.Node):
                Minimum element from the priority queue.
        """
        element = self.heap.pop(0)
        return element
