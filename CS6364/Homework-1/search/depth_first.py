from search.base import UninformedSearch
from search.utils import Node


class DFS(UninformedSearch):
    """Implementation of Depth-First search strategy.

    Parameters:
        frontier (list):
            Stack of nodes for expansion.
        visited (list):
            List of expanded nodes.
        success (bool):
            True, if goal is found. False, otherwise.
        path (list):
            Sequence of nodes from start to goal.
    """
    def __init__(self, start, goal, depth_limit):
        """Initializes :class: ``DFS``.

        Runs the algorithm and prints path from start node to goal node.
        If path is not found, FAILURE message is thrown.

        Arguments:
            start (search.utils.State):
                Start node.
            goal (search.utils.State):
                Goal node.
            depth_limit (int):
                Expand the search only until ``depth_limit``.
        """
        start = Node(start, 'root', 0)
        self.success = None
        self.visited = [start]
        self.frontier = [start]

        self.run(start, goal, depth_limit)
        if self.success:
            print('Path to Goal state found.')
            self.path = self.compute_path()
            print('Printing path:')
            self.print_path()
            print(f'\nNumber of moves = {len(self.path) - 2}')
        else:
            print('FAILURE: Goal state not reachable.')

        print(f'Number of expanded nodes = {len(self.visited)}')

    def remove_from_frontier(self):
        """Frontier is a stack data structure.
        Last element is popped.

        Returns:
            element (search.utils.Node)
        """
        element = self.frontier.pop()
        return element
