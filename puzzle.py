import pygame
import random
import time

# Constants for the game
CELL_SIZE = 100
WINDOW_SIZE = 700
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (173, 216, 230)

# Initialize Pygame
pygame.init()

# Set up some variables
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE - 50))
FONT = pygame.font.Font(None, CELL_SIZE//4)
clock = pygame.time.Clock()
exitButton = pygame.Rect(WINDOW_SIZE//2 - 100, WINDOW_SIZE//2 - 20, 90, 30)
restartButton = pygame.Rect(WINDOW_SIZE//2 - 300, WINDOW_SIZE//2 - 20, 90, 30)
helpButton = pygame.Rect(WINDOW_SIZE//2 + 100, WINDOW_SIZE//2 - 20, 90, 30)
bfsButton = pygame.Rect(WINDOW_SIZE - 150, WINDOW_SIZE//2 - 35, 76, 30)
astarButton = pygame.Rect(WINDOW_SIZE - 150, WINDOW_SIZE//2 - 4, 76, 30)

# Draw state
def drawState(state, startPos):
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                WINDOW.blit(state[i][j], (startPos[0] + j*CELL_SIZE, startPos[1] + i*CELL_SIZE))
# Draw button
def drawButton(button, x, y, message, colorButton = WHITE, colorMess = BLACK, dx = None, dy = None):
    pygame.draw.rect(WINDOW, colorButton, button)
    mess = FONT.render(message, True, colorMess)
    WINDOW.blit(mess, (button.x + x, button.y + y))
    pygame.draw.rect(WINDOW, BLACK, (dx, dy, 90, 30), 2, 5)

# Draw function
def draw(state, isHelp = False):
    WINDOW.fill(WHITE)
    drawState(state, (30,0))
    drawState(GOAL, (WINDOW_SIZE//2 + 20, 0))
    pygame.draw.rect(WINDOW, BLACK, (30, 0, WINDOW_SIZE//2 - 50, WINDOW_SIZE//2 - 50), 2)
    pygame.draw.rect(WINDOW, BLACK, (WINDOW_SIZE//2 + 20, 0, WINDOW_SIZE//2 - 50, WINDOW_SIZE//2 - 50), 2)
    pygame.draw.line(WINDOW, BLACK, (30, 100), (329, 100))
    pygame.draw.line(WINDOW, BLACK, (30, 200), (329, 200))
    pygame.draw.line(WINDOW, BLACK, (130, 0), (130, 299))
    pygame.draw.line(WINDOW, BLACK, (230, 0), (230, 299))
    pygame.draw.line(WINDOW, BLACK, (370, 100), (669, 100))
    pygame.draw.line(WINDOW, BLACK, (370, 200), (669, 200))
    pygame.draw.line(WINDOW, BLACK, (470, 0), (470, 299))
    pygame.draw.line(WINDOW, BLACK, (570, 0), (570, 299))
    drawButton(restartButton, 6, 7, 'RESTART', dx = 50, dy = 330)
    drawButton(exitButton, 25, 7, 'EXIT', dx = 250, dy = 330)
    if isHelp:
        drawButton(helpButton, 17, 7, 'PAUSE', dx = 450, dy = 330)
    else:
        drawButton(helpButton, 25, 7, 'HELP', dx = 450, dy = 330)

# Draw solution buttons
def drawSolButton():
    trianglePoints = [(WINDOW_SIZE - 162, WINDOW_SIZE//2 - 20), (WINDOW_SIZE - 162, WINDOW_SIZE//2 + 8), (WINDOW_SIZE - 144, WINDOW_SIZE//2 - 5)]
    pygame.draw.polygon(WINDOW, BLACK, trianglePoints)
    drawButton(bfsButton, 7, 7, 'BFS SOL', dx = WINDOW_SIZE - 150, dy = WINDOW_SIZE//2 - 35)
    drawButton(astarButton, 15, 7, 'A* SOL', dx = WINDOW_SIZE - 150, dy = WINDOW_SIZE//2 - 4)

# Show rating
def showRating(detail1 = None, detail2 = None):
    if detail1 != None:
        pygame.draw.rect(WINDOW, BLACK, (30, 440, 320, 150), 2)
        b = FONT.render('BFS Solution:', True, BLACK)
        space = FONT.render('Space: ' + str(detail1[0]), True, BLACK)
        t = FONT.render('Time: ' + str(detail1[1]) + ' ms', True, BLACK)
        WINDOW.blit(b, (130, 460))
        WINDOW.blit(space, (80, 500))
        WINDOW.blit(t, (80, 540))
    if detail2 != None:
        pygame.draw.rect(WINDOW, BLACK, (350, 440, 320, 150), 2)
        a = FONT.render('A* Solution:', True, BLACK)
        space = FONT.render('Space: ' + str(detail2[0]), True, BLACK)
        t = FONT.render('Time: ' + str(detail2[1]) + ' ms', True, BLACK)
        WINDOW.blit(a, (470, 460))
        WINDOW.blit(space, (410, 500))
        WINDOW.blit(t, (410, 540))

# Process image and upload
def loadImage():
    image = pygame.image.load('image.jpg')
    image = pygame.transform.scale(image, (WINDOW_SIZE//2, WINDOW_SIZE//2))
    cells = []
    for i in range(3):
        row = []
        for j in range(3):
            if (i == 2 and j == 2):
                row.append(0)
            else:
                rect = pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                cell = image.subsurface(rect)
                row.append(cell)
        cells.append(row)
    return cells

# Global variable
GOAL  = loadImage()

# Get the cell index
def getIndex(state, cell):
    for i in range(3):
        for j in range(3):
            if state[i][j] == cell:
                return (i, j)
            
# Move empty cell
def moveEmptyCell(state, x, y, i = None, j = None):
    index = getIndex(state, 0) if (i == None and j == None) else (i, j)
    if (x != 0 and y != 0) or index[0] + x < 0 or index[0] + x >= 3 or index[1] + y < 0 or index[1] + y >= 3:
        return False
    state[index[0]][index[1]], state[index[0] + x][index[1] + y] = state[index[0] + x][index[1] + y], state[index[0]][index[1]]
    return True

# Create start state
def shuffle(state, numOfShuffles):
    for _ in range(numOfShuffles):
        while not moveEmptyCell(state, random.choice([-1, 0, 1]), random.choice([-1, 0, 1])):
            pass

# Auto move empty cell
def help(state, solution):
    load = FONT.render('Loading...', True, BLACK)
    draw(state, True)
    WINDOW.blit(load, (315, 385))
    pygame.display.update()
    for i in range(1, len(solution) + 1):
        if solution[-i] == 'U':
            moveEmptyCell(state, -1, 0)
        elif solution[-i] == 'D':
            moveEmptyCell(state, 1, 0)
        elif solution[-i] == 'L':
            moveEmptyCell(state, 0, -1)
        elif solution[-i] == 'R':
            moveEmptyCell(state, 0, 1)
        time.sleep(0.65)
        draw(state, True)
        WINDOW.blit(load, (315, 385))
        pygame.display.update()
        clock.tick(FPS)

# Puzzle object
class Puzzle:
    heuristic = 0
    evalFunc = None
    useTheEvalFunc = False
    numOfInstances = 0

    # Initialization function
    def __init__(self, state, prevState, action, cost, useTheEvalFunc = False):
        self.prevState = prevState
        self.state = state
        self.action = action
        self.cost = prevState.cost + cost if prevState else cost
        if useTheEvalFunc:
            self.useTheEvalFunc = True
            self.calcHeuristicVal()
            self.evalFunc = self.heuristic + self.cost
        Puzzle.numOfInstances += 1

    # Calculate heuristic value
    def calcHeuristicVal(self):
        self.heuristic = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0:
                    iGoal, jGoal = getIndex(GOAL, self.state[i][j])
                    self.heuristic += abs(iGoal - i) + abs(jGoal - j)
    
    # Check the state space
    def check(self):
        return self.state == GOAL
    
    # Find the possible next steps/actions of the current state
    def findPossibleActions(self):
        i, j = getIndex(self.state, 0)
        actions = ['U', 'D', 'L', 'R']
        if i == 0: actions.remove('U')
        elif i == 2: actions.remove('D')
        if j == 0: actions.remove('L')
        elif j == 2: actions.remove('R')
        return actions
    
    # Create child states
    def createChild(self):
        children = []
        i, j = getIndex(self.state, 0)
        actions = self.findPossibleActions()

        for action in actions:
            newState = [row.copy() for row in self.state]
            if action == 'U':
                moveEmptyCell(newState, -1, 0, i, j)
            elif action == 'D':
                moveEmptyCell(newState, 1, 0, i, j)
            elif action == 'L':
                moveEmptyCell(newState, 0, -1, i, j)
            elif action == 'R':
                moveEmptyCell(newState, 0, 1, i, j)
            children.append(Puzzle(newState, self, action, 1, self.useTheEvalFunc))
        return children
    
    # Find solutions
    def findSolution(self):
        sol = [self.action]
        curr = self
        while curr.prevState != None:
            curr = curr.prevState
            sol.append(curr.action)
        sol = sol[:-1]
        return sol
