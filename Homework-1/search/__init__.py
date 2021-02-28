"""
Implementations for uninformed and informed search strategies:
(a) Depth-First Search : ``search.depth_first.DFS``
(b) Breadth-First Search : ``search.breadth_first.BFS``
(c) Iterative-Deepening Search : ``search.iterative_deepening.IDS``
(d) A-Star Search: ``search.aster.AStar``

Each requires multiple membership-tests in the search algorithm.
Membership-test in a list has a time complexity of O(n), while that
in a set is O(1). Thus, sets are used for this purpose.
"""

from search.utils import *
from search.depth_first import DFS
from search.iterative_deepening import IDS
from search.breadth_first import BFS
from search.astar import AStar
