import pygame
from abc import ABC, abstractmethod
 
pygame.init()

blockWidth = 10

class TetrisShape(ABC):
    def __init__(self, state, x, y):
        self.state = state
        self.x = x
        self.y = y
        self.blocks = [pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth)]
        self.bottomNum = 0
        self.wideLeft = 0
        self.wideRight = 0
        self.isFalling = True

    def rotate(self):
        self.state += 1
        if self.state > 3:
            self.state = 0
        self.setup()
    
    def fall(self):
        if self.y < (19 - self.bottomNum):
            self.y += 1
            self.setup()
            return True
        else:
            return False

    def overlaps(self, otherBlocks):
        for i in range(4):
            for j in range(4):
                if (otherBlocks[j].x >= self.blocks[i].x and otherBlocks[j].x < self.blocks[i].x + blockWidth) and (otherBlocks[j].y >= self.blocks[i].y and otherBlocks[j].y < self.blocks[i].y + blockWidth):
                    return True
        return False

    def canShiftDown(self):
        
        return 1

    def canShiftLeft(self):
        return 1
    
    def canShiftRight(self):
        return 1

    @abstractmethod
    def setup():
        pass

"""
class Line(TetrisShape):
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.blocks = [(0, 0), (0, 0), (y, x),(0, 0)]
        self.state = state
        self.setup()
        self.isFalling = True


    def setup(self):
        if self.state == 0:
            self.blocks[0] = (self.y+2, self.x)         #  x
            self.blocks[1] = (self.y+1, self.x)         #  x
            self.blocks[2] = (self.y, self.x)           #  o
            self.blocks[3] = (self.y-1, self.x)         #  x
            self.bottomNum = 2
            self.wideRight = 0
            self.wideLeft = 0
        elif self.state == 1:
            self.blocks[0] = (self.y, self.x-2)         #  x x o x
            self.blocks[1] = (self.y, self.x-1)
            self.blocks[2] = (self.y, self.x)
            self.blocks[3] = (self.y, self.x+1)
            self.bottomNum = 0
            self.wideRight = 1
            self.wideLeft = 2
        elif self.state == 2:
            self.blocks[0] = (self.y+1, self.x)         #  x
            self.blocks[1] = (self.y, self.x)           #  o
            self.blocks[2] = (self.y-1, self.x)         #  x
            self.blocks[3] = (self.y-2, self.x)         #  x
            self.bottomNum = 1
            self.wideRight = 0
            self.wideLeft = 0
        elif self.state == 3:
            self.blocks[0] = (self.y, self.x-1)         #  x o x x
            self.blocks[1] = (self.y, self.x)           
            self.blocks[2] = (self.y, self.x+1)
            self.blocks[3] = (self.y, self.x+2)
            self.bottomNum = 0
            self.wideRight = 2
            self.wideLeft = 1
    def getBottomNum(self):
        return self.bottomNum
"""

screen = pygame.display.set_mode((200, 400))
done = False

#(xTopLeft,yTopLeft,width,height)
test = pygame.Rect(30,30,60,60)

pygame.draw.rect(screen, (0,0,255), test)

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue
    screen.fill((255,255,255))
    pygame.draw.rect(screen, (0,0,255), test)
    pygame.display.flip()