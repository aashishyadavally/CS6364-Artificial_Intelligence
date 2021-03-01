from search.utils import Node as UNode
from search.utils import goal_check, number_of_misplaced, \
                        manhattan, PriorityQueue, get_children


class Node(UNode):
    """Inherits from :class: ``search.utils.Node``. Additional
    attributes necessary for the A-Star search algorithm such
    as f-score and h-score included as class attributes 
    'f' and 'h' respectively.

    Parameters:
        state (search.utils.State):
            Eight-Puzzle state.
        parent (search.astar.Node):
            Predecessor node.
        depth (int):
            Depth of node.
        h (int):
            h-score, computed from heuristic function.
        f (int):
            f-score
            f-score = h-score + depth

    Properties:
        children (list):
            List of neighbor states.
    """
    def __init__(self, current, parent, depth):
        """Initializes :class: ``search.astar.Node``.

        Arguments:
            current (search.utils.State):
                Current eight-puzzle state.
            parent (search.astar.Node):
                Predecessor node.
            depth (int):
                Depth of node.
        """
        self.state = current
        self.parent = parent
        self.depth = depth
        self.h = None
        self.f = None

    @property
    def children(self):
        children = [Node(child, self, self.depth + 1) \
                    for child in get_children(self.state)]
        return children

    def __lt__(self, other):
        if isinstance(other, self.__class__) and \
           self.f < other.f:
            return True
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, self.__class__) and \
           self.f > other.f:
            return True
        else:
            return False


class AStar:
    """Implementation of A-Star search strategy. Default heuristic
    is 'number of misplaced tiles'. Other option for heuristic
    is Manhattan Distance.

    Parameters:
        heuristic_fn (search.utils.*):
            Either :method: ``search.utils.number_of_misplaced``
            or :method: ``search.utils.manhattan``.
        depth_limit (int):
            Expand the search only until ``depth_limit``.
        open (search.utils.PriorityQueue):
            Priority queue representing list of open nodes.
        closed (list):
            List of expanded nodes.
        success (bool):
            True, if goal is found. False, otherwise.
        path (list):
            Sequence of nodes from start to goal.
    """
    def __init__(self, start, goal, depth_limit, heuristic='misplaced'):
        """Initializes :class: ``AStar``.

        Runs the algorithm and prints path from start node to goal node.
        If path is not found, FAILURE message is thrown.

        Arguments:
            start (search.utils.State):
                Start node.
            goal (search.utils.State):
                Goal node.
            depth_limit (int):
                Expand the search only until ``depth_limit``.
            heuristic (str):
                One of 'misplaced' or 'manhattan'.
                'misplaced' -> search.utils.number_of_misplaced
                'manhattan' -> search.utils.manhattan
        """
        if heuristic == 'misplaced':
            self.heuristic_fn = number_of_misplaced
        else:
            self.heuristic_fn = manhattan

        start = Node(start, 'root', 0)
        start.h = self.heuristic_fn(start.state, goal)
        start.f = start.h + start.depth

        self.depth_limit = depth_limit
        self.open = PriorityQueue([start])
        self.closed = []

        self.run(start, goal)
        if self.success:
            print('Path to Goal state found.')
            self.path = self.compute_path()
            print('Printing path:')
            self.print_path()
            print(f'\nNumber of moves = {len(self.path) - 2}')
        else:
            print('FAILURE: Goal state not reachable.')

        print(f'Number of expanded nodes = {len(self.closed)}')

    def _check_if_closed(self, node):
        _closed = set(self.closed)
        if node in _closed:
            return True
        else:
            return False

    def compute_path(self):
        """Computer sequence of nodes from start to goal.

        Returns:
            (list):
                List of nodes from start to goal.
        """
        current = self.closed.pop()
        path, root = [current], False

        while not root:
            parent = path[-1].parent
            path.append(parent)
            if parent == 'root':
                root = True
        return path[::-1]

    def print_path(self):
        """Prints sequence of nodes along the path from start
        to goal.
        """
        for index, element in enumerate(self.path):
            print(f'Step {index}:')
            print('--------------')
            if element == 'root':
                print('root\n')
            else:
                element.state.show()

    def run(self, start, goal):
        """Runs the A-Star algorithm.

        If the search can find a path from start to goal, it
        is computed. Otherwise, FAILURE message is thrown.
        """
        def _run_iteration(curr):
            self.closed.append(curr)
            for child in curr.children:
                child.h = self.heuristic_fn(child.state, goal)
                child.f =  child.h + child.depth
                if not self._check_if_closed(child):
                    self.open.add(child)

        while(self.open.heap):
            curr = self.open.pop()
            if goal_check(curr.state, goal):
                self.success = True
                break
            else:
                if curr.depth <= self.depth_limit:
                    _run_iteration(curr)

        if goal_check(curr.state, goal):
            self.closed.append(curr)
            self.success = True
        else:
            self.success = False
