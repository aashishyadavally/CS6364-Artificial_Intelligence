from copy import deepcopy


ACTIONS = ['up', 'down', 'left', 'right']


def read_states(filename):
    """
    """
    with open(filename, 'r') as fileobj:
        contents = fileobj.readlines()
        _input, goal = contents[0].split(), contents[1].split()
    return State(_input), State(goal)


def get_child(parent, action):
    """
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
    """
    """
    children = [get_child(parent, action) for action in ACTIONS]
    children = [child for child in children if child is not None]
    return children


class State:
    def __init__(self, _input):
        """
        """
        self.config = [_input[0:3], _input[3:6], _input[6:9]]

    def show(self):
        """
        """
        for row in self.config:
            print(row)
        print('')