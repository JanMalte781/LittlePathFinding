import pygame 
import sys
import AStar 
import Dijkstra
import DFS
import numpy as np


BLACK = (50,50,50)
WHITE = (190,190,190)
RED = (230,10,10)
GREEN = (10, 230, 10)
YELLOW = (230, 230, 10)
YELLOW2 = (100, 100, 10)


'change the size of the gamefield by changing the following'
LINE_BLOCKS = 20
ROW_BLOCKS = 20

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750

blockSize = int(SCREEN_WIDTH / LINE_BLOCKS)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)

clock = pygame.time.Clock()





def main():


    clickedPos = np.zeros((LINE_BLOCKS, ROW_BLOCKS))
    startingPos = (0,0)
    endPos = (0,0)
    startSet = False
    endSet = False
    


    pygame.init()
    #gameLoop
    run = True 
    while run:

        drawGrid()

        for event in pygame.event.get():

            if pygame.mouse.get_pressed()[1]:
                try:
                    pos = event.pos
                    try:
                        clickedPos[clickedField(pos)[1]][clickedField(pos)[0]] = 1
                        redrawGrid(pos)
                    except:
                        pass

                except AttributeError:
                    pass
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                # start pathFinding or restart
                if event.button == 1 and pygame.mouse.get_pos()[1] > 600:
                    if pygame.mouse.get_pos()[1] < 700:
                        # Astar
                        if pygame.mouse.get_pos()[0] < 200:
                            path = AStar.a_star(startingPos, endPos, clickedPos)
                        
                        # Dijkstra
                        if pygame.mouse.get_pos()[0] > 200 and pygame.mouse.get_pos()[0] < 400:
                            path = Dijkstra.dijkstraPath(startingPos, endPos, clickedPos)

                        #DFS
                        if pygame.mouse.get_pos()[0] > 400:
                            path = DFS.DFS_path(startingPos, endPos, clickedPos)
                        
                        drawPath(path)
                        print(path[0])
                    else:
                        # reset the Field
                        rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_WIDTH)
                        pygame.draw.rect(screen, WHITE, rect, 0)
                        drawGrid()
                        clickedPos = np.zeros((LINE_BLOCKS, ROW_BLOCKS))
                        startingPos = (0,0)
                        endPos = (0,0)
                        startSet = False
                        endSet = False
    
                #set a starting point
                if event.button == 1 and not startSet:
                    pos = pygame.mouse.get_pos()
                    if(pos[1] < 600):
                        setStart(pos)
                        startingPos = clickedField((pos))
                        startSet = True

                #set an ending point
                if event.button == 3 and not endSet:
                    pos = pygame.mouse.get_pos()
                    if(pos[1] < 600):
                        setEnd(pos)
                        endPos = clickedField((pos))
                        endSet = True

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit(0)
        
        pygame.display.update()


class Button:
    def __init__(self, text, x, y, width, height) -> None:
        self.text = text
        self.left = x
        self.top = y
        self.width = width
        self.height = height

    def draw(self):
        rect = pygame.Rect(self.left, self.top, self.width, self.height)
        pygame.draw.rect(screen, (211, 101, 43), rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        font = pygame.font.SysFont("arial", 25)

        text = font.render(self.text, True, (0,0,0))
        textRectangle = text.get_rect(center=rect.center)
        screen.blit(text, textRectangle)

        

def drawGrid():

    font = pygame.font.SysFont("arial", 25)

    for x in range(0, SCREEN_WIDTH, blockSize):
        for y in range(0, SCREEN_HEIGHT - 100, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, BLACK, rect, 1)
    
    # Astar button
    aStarButton = Button("A*", 0, SCREEN_WIDTH, SCREEN_WIDTH / 3, 100)
    aStarButton.draw()

    # Dijkstra button
    dijkstraButton = Button("Dijkstra", SCREEN_WIDTH / 3, SCREEN_WIDTH, SCREEN_WIDTH / 3, 100)
    dijkstraButton.draw()

    # DFS button
    dfsButton = Button("DFS", 2 * SCREEN_WIDTH / 3, SCREEN_WIDTH, SCREEN_WIDTH / 3, 100)
    dfsButton.draw()

    # RESET button
    resetButton = Button("RESET", 0, 700, SCREEN_WIDTH, 50)
    resetButton.draw()

def redrawGrid(pos : tuple[int, int]):
    cornerPos = (pos[0] - (pos[0] % blockSize), pos[1] - (pos[1] % blockSize))
    rect = pygame.Rect(cornerPos[0], cornerPos[1], blockSize, blockSize)
    pygame.draw.rect(screen, BLACK, rect, 0)

def clickedField(pos : tuple[int, int]):
    x = int((pos[0] - (pos[0] % blockSize)) / blockSize)
    y = int((pos[1] - (pos[1] % blockSize)) / blockSize)
    return(x,y)

def setStart(pos : tuple[int, int]):
    cornerPos = (pos[0] - (pos[0] % blockSize), pos[1] - (pos[1] % blockSize))
    rect = pygame.Rect(cornerPos[0], cornerPos[1], blockSize, blockSize)
    pygame.draw.rect(screen, GREEN, rect, 0)

def setEnd(pos : tuple[int, int]):
    cornerPos = (pos[0] - (pos[0] % blockSize), pos[1] - (pos[1] % blockSize))
    rect = pygame.Rect(cornerPos[0], cornerPos[1], blockSize, blockSize)
    pygame.draw.rect(screen, RED, rect, 0)

def drawPath(path):
    'path is tuple of 2 Lists, first List is the optimal way, second list is list of tuples ((a,b),c), where (a,b) is the position '
    'of node which was progressed and c = 0 or 1 gives the list, i.e 0 for openlist and 1 for closed list'
    'order of path[1] is the order in which they are processed'

    # draw the exploration of the algorithm
    for i in range(len(path[1])):
        pygame.time.delay(10)
        xPos = path[1][i][0][0]* blockSize
        yPos = path[1][i][0][1]* blockSize
        rect = pygame.Rect(xPos, yPos, blockSize, blockSize)
        if path[1][i][1] == 0:
            pygame.draw.rect(screen, YELLOW2, rect, 0)
        else:
            pygame.draw.rect(screen, YELLOW , rect, 0)
        pygame.display.update()
    
    # draw shortest path from start to finish
    for i in range(len(path[0])):
        pygame.time.delay(10)
        xPos = path[0][i][0]* blockSize
        yPos = path[0][i][1]* blockSize
        rect = pygame.Rect(xPos, yPos, blockSize, blockSize)
        pygame.draw.rect(screen, GREEN, rect, 0)
        pygame.display.update()
        


if __name__ == '__main__':
    main()
