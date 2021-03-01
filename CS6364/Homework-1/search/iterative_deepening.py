from search.base import UninformedSearch
from search.utils import Node


class IDS(UninformedSearch):
    """Implementation of Iterative-Deepening search strategy.

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
        """Initializes :class: ``IDS``.

        Arguments:
            start (search.utils.State):
                Start node.
            goal (search.utils.State):
                Goal node.
            depth_limit (int):
                Expand the search only until ``depth_limit``.
        """
        start = Node(start, 'root', 0)

        for depth in range(1, depth_limit):
            self.success = None
            self.visited = [start]
            self.frontier = [start]

            print(f"Checking for maximum depth of {depth}:")
            print('================================')
            self.run(start, goal, depth)

            if self.success:
                print('Path to Goal state found.')
                self.path = self.compute_path()
                print('Printing path:')
                self.print_path()
                print(f'\nNumber of moves = {self.num_moves}')
                break
            else:
                print(f'Path not found at maximum depth of {depth}\n')

        if not self.success:
            print('FAILURE: Goal state not reachable.')

        print(f'Number of expanded nodes = {self.num_nodes_expanded}')

    def remove_from_frontier(self):
        """Frontier is a stack data structure.
        Last element is popped.

        Returns:
            element (search.utils.Node)
        """
        element = self.frontier.pop()
        return element
