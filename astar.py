from queue import PriorityQueue
from puzzle import Puzzle

# A* Search
def astarSearch(startState):
    order = 0
    exp = dict()
    start = Puzzle(startState, None, None, 0, True)
    queue = PriorityQueue()
    queue.put((start.evalFunc, order, start))
    while queue:
        curr = queue.get()[2]
        exp[tuple(map(tuple, curr.state))] = 0b0
        if curr.check():
            return curr.findSolution()
        children = curr.createChild()
        for child in children:
            tmp = [row.copy() for row in child.state]
            if tuple(map(tuple, tmp)) not in exp:
                order += 1
                queue.put((child.evalFunc, order, child))
    return