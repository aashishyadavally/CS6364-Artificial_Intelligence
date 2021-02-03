import argparse
from search import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CS6364: Homework 1')
    parser.add_argument('--input-path', dest='input_path', type=str,
                        required=True, help='Path to input file: \
                        (a) \'*\' refers to the blank tile in 8-Puzzle Problem. \
                        (b) First line -> Input State, Second line -> Goal State.')
    parser.add_argument('--algorithm', dest='algo', type=str,
                        choices=['dfs', 'bfs', 'astar1', 'astar2'],
                        required=True, help='Search algorithm to run, choices are: \
                        (a) dfs: Depth-First Search (b) bfs: Breadth-First Search \
                        (c) astar1: A* algorithm with heuristic 1 \
                        (d) astar2: A* algorithm with heuristic 2')

    args = parser.parse_args()

    input_state, goal_state = read_states(args.input_path)

    if args.algo == 'dfs':
        print('BFS')
    elif args.algo == 'bfs':
        print('DFS')
    elif args.algo == 'astar1':
        print('AStar1')
    elif args.algo == 'astar2':
        print('AStar2')
