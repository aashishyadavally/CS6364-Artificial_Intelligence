from search.base import UninformedSearch
from search.utils import Node


class BFS(UninformedSearch):
    """Implementation of Breadth-First search strategy.

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
    def __init__(self, start, goal):
        """Initializes :class: ``BFS``.

        Runs the algorithm and prints path from start node to goal node.
        If path is not found, FAILURE message is thrown.

        Arguments:
            start (search.utils.State):
                Start node.
            goal (search.utils.State):
                Goal node.
        """
        start = Node(start, 'root', 0)
        self.success = None
        self.visited = [start]
        self.frontier = [start]

        self.run(start, goal)
        if self.success:
            print('Path to Goal state found.')
            self.path = self.compute_path()
            print('Printing path:')
            self.print_path()
            print(f'\nNumber of moves = {self.num_moves}')
        else:
            print('FAILURE: Goal state not reachable.')

        print(f'Number of expanded nodes = {self.num_nodes_expanded}')

    def remove_from_frontier(self):
        """Frontier is a queue data structure.
        First element is popped.

        Returns:
            element (search.utils.Node)
        """
        element = self.frontier.pop(0)
        return element
