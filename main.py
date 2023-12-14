import pygame
import sys
import time
from puzzle import *
from bfs import bfsSearch
from astar import astarSearch

#Main function
def main():
    state = [row.copy() for row in GOAL]
    shuffle(state, 100)
    stateTemp = [row.copy() for row in state]

    showSolButton = False

    Puzzle.numOfInstances = 0
    t0 = time.time()
    astar = astarSearch(state)
    t1 = (time.time() - t0) * 1000
    detailAstar = [Puzzle.numOfInstances, round(t1, 5), 0]

    Puzzle.numOfInstances = 0
    t0 = time.time()
    bfs = bfsSearch(state)
    t1 = (time.time() - t0) * 1000
    detailBfs = [Puzzle.numOfInstances, round(t1, 5), 0]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    moveEmptyCell(state, 0, 1)
                elif event.key == pygame.K_LEFT:
                    moveEmptyCell(state, 0, -1)
                elif event.key == pygame.K_DOWN:
                    moveEmptyCell(state, 1, 0)
                elif event.key == pygame.K_UP:
                    moveEmptyCell(state, -1, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exitButton.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif restartButton.collidepoint(event.pos):
                    state = [row.copy() for row in stateTemp]
                elif helpButton.collidepoint(event.pos):
                    showSolButton = not showSolButton
                elif bfsButton.collidepoint(event.pos):
                    if state != stateTemp:
                        Puzzle.numOfInstances = 0
                        t0 = time.time()
                        bfs = bfsSearch(state)
                        t1 = (time.time() - t0) * 1000
                        detailBfs = [Puzzle.numOfInstances, round(t1, 5), 0]
                    help(state, bfs)
                    detailBfs[-1] = 1
                    showSolButton = not showSolButton
                elif astarButton.collidepoint(event.pos):
                    if state != stateTemp:
                        Puzzle.numOfInstances = 0
                        t0 = time.time()
                        astar = astarSearch(state)
                        t1 = (time.time() - t0) * 1000
                        detailAstar = [Puzzle.numOfInstances, round(t1, 5), 0]
                    help(state, astar)
                    detailAstar[-1] = 1
                    showSolButton = not showSolButton

        draw(state)

        if showSolButton:
            drawSolButton()
            
        if detailBfs[-1] == 1:
            showRating(detail1 = detailBfs)
            
        if detailAstar[-1] == 1:
            showRating(detail2 = detailAstar)

        if state == GOAL:
            welcomText = FONT.render('CONGRATULATIONS !', True, BLACK)
            WINDOW.blit(welcomText, (265, 385))
            pygame.display.update()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
