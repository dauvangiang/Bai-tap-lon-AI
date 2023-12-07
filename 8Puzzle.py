import pygame
import random
import sys
import time

# Size of the board
BOARD_SIZE = 3

# Constants for the game
TILE_SIZE = 80
WINDOW_SIZE = 600
FPS = 60

#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)

# Initialize Pygame
pygame.init()

# Set up some variables
WINDOW = pygame.display.set_mode((WINDOW_SIZE - 40, WINDOW_SIZE - 200))
FONT = pygame.font.Font(None, TILE_SIZE//3)
clock = pygame.time.Clock()

#Process photos and upload
def loadImage():
    image = pygame.image.load('image.jpg')
    image = pygame.transform.scale(image, (WINDOW_SIZE//2, WINDOW_SIZE//2))
    tiles = []
    for i in range(BOARD_SIZE):
        row = []
        for j in range(BOARD_SIZE):
            rect = pygame.Rect(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            tile = image.subsurface(rect)
            row.append(tile)
        tiles.append(row)
    return tiles

#Draw board
def drawBoard(board, startPos):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != 0:
                WINDOW.blit(board[i][j], (startPos[0] + j*TILE_SIZE, startPos[1] + i*TILE_SIZE))

#Get the position of the empty tile  
def getEmptyTile(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                return (i, j)

#Move tile          
def move(board, x, y):
    emptyTile = getEmptyTile(board)
    if (x != 0 and y != 0) or emptyTile[0] + x < 0 or emptyTile[0] + x >= BOARD_SIZE or emptyTile[1] + y < 0 or emptyTile[1] + y >= BOARD_SIZE:
        return False
    board[emptyTile[0]][emptyTile[1]], board[emptyTile[0] + x][emptyTile[1] + y] = board[emptyTile[0] + x][emptyTile[1] + y], board[emptyTile[0]][emptyTile[1]]
    return True

#Generate random puzzles with numMove times
def shuffleBoard(board, numMove):
    for _ in range(numMove):
        while not move(board, random.choice([-1, 0, 1]), random.choice([-1, 0, 1])):
            pass

#Draw buttons
def drawButton(button, dx, dy, string):
    pygame.draw.rect(WINDOW, BLACK, button)
    text = FONT.render(string, True, WHITE)
    WINDOW.blit(text, (button.x + dx, button.y + dy))

#Main function
def main():
    board = loadImage()
    board[BOARD_SIZE-1][BOARD_SIZE-1] = 0
    targetBoard = [row.copy() for row in board]
    shuffleBoard(board, 100)
    boardTemp = [row.copy() for row in board]

    exitButton = pygame.Rect(WINDOW_SIZE//2, WINDOW_SIZE - 330, 60, 30)
    replayButton = pygame.Rect(WINDOW_SIZE//2 - 150, WINDOW_SIZE - 330, 100, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    move(board, 0, 1)
                elif event.key == pygame.K_LEFT:
                    move(board, 0, -1)
                elif event.key == pygame.K_DOWN:
                    move(board, 1, 0)
                elif event.key == pygame.K_UP:
                    move(board, -1, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exitButton.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif replayButton.collidepoint(event.pos):
                    board = [row.copy() for row in boardTemp]

        WINDOW.fill((255, 255, 255))
        drawBoard(board, (15,0))
        drawBoard(targetBoard, (WINDOW_SIZE//2, 0))

        #Draw the border
        pygame.draw.rect(WINDOW, BLACK, (15, 0, WINDOW_SIZE//2 - 60, WINDOW_SIZE//2 - 60), 1)
        pygame.draw.rect(WINDOW, BLACK, (WINDOW_SIZE//2, 0, WINDOW_SIZE//2 - 60, WINDOW_SIZE//2 - 60), 1)

        drawButton(replayButton, 6, 7, 'Play Again')
        drawButton(exitButton, 15, 7, 'Exit')

        #Update screen
        pygame.display.update()
        clock.tick(FPS)

        #Check status
        if board == targetBoard:
            welcomText = FONT.render('Ban da hoan thanh !', True, BLACK)
            WINDOW.blit(welcomText, (190, WINDOW_SIZE//2 + 30))
            pygame.display.update()
            time.sleep(2)
            break

if __name__ == "__main__":
    main()
