"""Main script for running the search algorithm implementations
in ``search`` module.

To get the options, run:
    $ python main.py --help 
"""

import argparse
from search import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CS6364: Homework 1')
    parser.add_argument('--input-path', dest='input_path', type=str,
                        required=True, help='Path to input file: \
                        (a) \'*\' refers to the blank tile in 8-Puzzle Problem. \
                        (b) First line -> Input State, Second line -> Goal State.')
    parser.add_argument('--algorithm', dest='algo', type=str,
                        choices=['dfs', 'ids', 'astar1', 'astar2'],
                        required=True, help='Search algorithm to run, choices are: \
                        (a) dfs: Depth-First Search \
                        (b) ids: Iterative-Deepening Search \
                        (c) astar1: A* algorithm with heuristic 1 \
                            (Number of misplaced tiles) \
                        (d) astar2: A* algorithm with heuristic 2 \
                            (Manhattan Distance)')
    parser.add_argument('--depth-limit', dest='depth_limit', type=int,
                        default=10, help='Depth limit for search traversal. \
                        Valid for Depth-First and Iterative-Deepening Search algorithms.')

    args = parser.parse_args()

    start_state, goal_state = read_states(args.input_path)

    if args.algo == 'dfs':
        DFS(start_state, goal_state, args.depth_limit)
    elif args.algo == 'ids':
        IDS(start_state, goal_state, args.depth_limit)
    elif args.algo == 'astar1':
        AStar(start_state, goal_state, args.depth_limit,
              heuristic='misplaced')
    elif args.algo == 'astar2':
        AStar(start_state, goal_state, args.depth_limit,
              heuristic='manhattan')
