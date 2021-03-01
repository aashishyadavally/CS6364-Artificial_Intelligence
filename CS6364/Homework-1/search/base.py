from abc import ABC, abstractmethod
from search.utils import Node, goal_check


class UninformedSearch(ABC):
    """Base class for uninformed search strategies such as
    breadth-first search, depth-first search and iterative
    deepening search.

    Properties:
        num_moves (int):
            Number of moves to reach goal state.
        num_nodes_expanded (int):
            Number of expanded nodes.
    """
    @abstractmethod
    def remove_from_frontier(self):
        """An abstract method to remove node from frontier.
        """
        pass

    @property
    def num_moves(self):
        try:
            return len(self.path) - 2
        except:
            return None

    @property
    def num_nodes_expanded(self):
        return len(self.visited) 

  
    def _check_if_visited(self, node):
        _visited = set(self.visited)
        if node in _visited:
            return True
        else:
            return False

    def compute_path(self):
        """Computer sequence of nodes from start to goal.

        Returns:
            (list):
                List of nodes from start to goal.
        """
        current = self.visited.pop()
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


    def run(self, start, goal, depth_limit=None):
        """Runs the Uninformed search algorithm.

        If the search can find a path from start to goal, it
        is computed. Otherwise, FAILURE message is thrown.
        """
        def _run_iteration(curr):
            unvisited_children = [child for child in curr.children \
                                  if not self._check_if_visited(child)]
            for child in unvisited_children:
                self.visited.append(child)
                self.frontier.append(child)

        while(self.frontier):
            curr = self.remove_from_frontier()
            if goal_check(curr.state, goal):
                self.success = True
                break
            else:
                if depth_limit is not None:
                    if curr.depth <= depth_limit:
                        _run_iteration(curr)
                else:
                    _run_iteration(curr)

        if goal_check(curr.state, goal):
            self.visited.append(curr)
            self.success = True
        else:
            self.success = False
