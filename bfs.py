from queue import Queue
from puzzle import *

# Breadth-First Search
def bfsSearch(startState):
    start = Puzzle(startState, None, None, 0)
    if start.check():
        return start.findSolution()
    queue = Queue()
    queue.put(start)
    exp = dict()
    while queue:
        curr = queue.get()
        exp[tuple(map(tuple, curr.state))] = 0b0
        children = curr.createChild()
        for child in children:
            if tuple(map(tuple, child.state)) not in exp:
                if child.check():
                    return child.findSolution()
                queue.put(child)
    return