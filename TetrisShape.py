import pygame
from abc import ABC, abstractmethod

moveSpeed = 10
blockWidth = 10

class TetrisShape(ABC):
    def __init__(self, x, y, state, color):
        self.state = state
        #x and y coords are for the rotation point of the piece
        self.x = x
        self.y = y
        self.color = color
        #each piece is made up of 4 rectangles
        self.blocks = [pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth)]
        self.isFalling = True

    #NOT FINISHED, changes state of piece
    #all pieces' states are defined in the individual declerations
    def rotate(self):
        self.state += 1
        if self.state > 3:
            self.state = 0
        self.setup()
    
    #if the piece can move down it gets moved down. Returns true if it can fall, otherwise false
    def fall(self, screenHeight, gamePieces):
        canFall = True
        for i in range(4):
            if self.blocks[i].y + moveSpeed + blockWidth > screenHeight:
                canFall = False
        for frozenPieces in gamePieces[:-1]:
            if self.overlaps(frozenPieces.blocks,0,moveSpeed):
                canFall = False
        if canFall:
            self.y += moveSpeed
            self.setup()
            return True
        else:
            return False

    #checks if a pixel of the other block is inside the block getting checked
    #the optional values are for the canShift functions, just shifts the detection by the specifed amount
    def overlaps(self, otherBlocks, xShift = 0, yShift = 0):
        for i in range(4):
            for j in range(4):
                if (otherBlocks[j].x >= self.blocks[i].x + xShift and otherBlocks[j].x < self.blocks[i].x + blockWidth + xShift) and (otherBlocks[j].y >= self.blocks[i].y + yShift and otherBlocks[j].y < self.blocks[i].y + blockWidth + yShift):
                    return True
        return False

    #all the shift functions just call overlaps, but add however far in the x or y direction they are shifted
    #the for loop loops through all shapes in the provided array except for the last one because peter assures me the last one will always be the only falling one
    #the shift left and right functions have additional dectection for the sides

    def ShiftLeft(self,gamePieces):
        canShift = True
        for frozenPieces in gamePieces[:-1]:
            if self.overlaps(frozenPieces.blocks,-moveSpeed):
                canShift = False
        for i in range(4):
            if self.blocks[i].x - moveSpeed < 0:
                canShift = False
        if canShift:
            self.x -= moveSpeed
            self.setup()


    def ShiftRight(self,gamePieces, screenWidth):
        canShift = True
        for frozenPieces in gamePieces[:-1]:
            if self.overlaps(frozenPieces.blocks,moveSpeed):
                canShift = False
        for i in range(4):
            if self.blocks[i].x + moveSpeed + blockWidth > screenWidth:
                canShift = False
        if canShift:
            self.x += moveSpeed
            self.setup()
    #might be causing collision problems
    def ShiftDown(self,gamePieces, screenHeight):
        canFall = True
        for i in range(4):
            if self.blocks[i].y + moveSpeed + blockWidth > screenHeight:
                canFall = False
        for frozenPieces in gamePieces[:-1]:
            if self.overlaps(frozenPieces.blocks,0,moveSpeed):
                canFall = False
        if canFall:
            self.y += moveSpeed
            self.setup()

    #this one doesnt need to exist
    def ShiftUp(self,gamePieces):
        canShift = True
        for frozenPieces in gamePieces[:-1]:
            if self.overlaps(frozenPieces.blocks,0,-moveSpeed):
                canShift = False
        if canShift:
            self.y -= moveSpeed
            self.setup()

    #needed for pygame, draws loops through the rectangles and draws each box of the piece
    def DrawShape(self,screen):
        for i in range(4):
            pygame.draw.rect(screen, self.color,self.blocks[i])

    @abstractmethod
    def setup():
        pass


class Line(TetrisShape):
    def __init__(self, x, y, state, color):
        self.x = x
        self.y = y
        self.color = color
        self.blocks = [pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth)]
        self.state = state
        self.isFalling = True
        self.setup()


    def setup(self):
        # the x,y point this is based on is in the center of the line, on the line between two blocks
        # need to change to be tile based
        if self.state == 0:

            # 0
            # 1
            # 2
            # 3
            #with the rotation point on the left
            self.blocks[0].x = self.x
            self.blocks[0].y = self.y - (blockWidth*2)

            self.blocks[1].x = self.x
            self.blocks[1].y = self.y - blockWidth

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x
            self.blocks[3].y = self.y + blockWidth

        elif self.state == 1:
            # 0 1 2 3
            #with the rotation point on the top
            self.blocks[0].x = self.x - (blockWidth*2)
            self.blocks[0].y = self.y

            self.blocks[1].x = self.x - blockWidth
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x + blockWidth
            self.blocks[3].y = self.y

        elif self.state == 2:
             # 0
            # 1
            # 2
            # 3
            #with the rotation point on the right
            self.blocks[0].x = self.x - blockWidth
            self.blocks[0].y = self.y - (blockWidth*2)

            self.blocks[1].x = self.x - blockWidth
            self.blocks[1].y = self.y - blockWidth

            self.blocks[2].x = self.x - blockWidth
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x - blockWidth
            self.blocks[3].y = self.y + blockWidth

        elif self.state == 3:
            # 0 1 2 3
            #with the rotation point on the bottom
            self.blocks[0].x = self.x - (blockWidth*2)
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x - blockWidth
            self.blocks[1].y = self.y - blockWidth

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y - blockWidth

            self.blocks[3].x = self.x + blockWidth
            self.blocks[3].y = self.y - blockWidth

class Jshape(TetrisShape):
    def __init__(self, x, y, state, color):
        self.x = x
        self.y = y
        self.color = color
        self.blocks = [pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth)]
        self.state = state
        self.setup()
        self.isFalling = True

    def setup(self):
        if self.state == 0:
            # 0
            # 1 2 3
            #center is the 2
            self.blocks[0].x = self.x - blockWidth
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x - blockWidth
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x + blockWidth
            self.blocks[3].y = self.y

        elif self.state == 1:
            # 0 1
            # 2
            # 3
            #center is the 2
            self.blocks[0].x = self.x
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x + blockWidth
            self.blocks[1].y = self.y - blockWidth

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x
            self.blocks[3].y = self.y + blockWidth

        elif self.state == 2:
            # 0 1 2
            #     3
            #center is the 1
            self.blocks[0].x = self.x - blockWidth
            self.blocks[0].y = self.y

            self.blocks[1].x = self.x
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x + blockWidth
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x + blockWidth
            self.blocks[3].y = self.y + blockWidth

        elif self.state == 3:
            # 0
            # 1
            # 2 3
            #center is the 1
            self.blocks[0].x = self.x
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y + blockWidth

            self.blocks[3].x = self.x + blockWidth
            self.blocks[3].y = self.y + blockWidth

class Lshape(TetrisShape):
    def __init__(self, x, y, state, color):
        self.x = x
        self.y = y
        self.color = color
        self.blocks = [pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth)]
        self.state = state
        self.setup()
        self.isFalling = True

    def setup(self):
        if self.state == 0:
            #     0
            # 1 2 3
            # the center is 2
            self.blocks[0].x = self.x + blockWidth
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x - blockWidth
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x + blockWidth
            self.blocks[3].y = self.y

        elif self.state == 1:
            # 0
            # 1
            # 2 3
            # the center is 1
            self.blocks[0].x = self.x
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y + blockWidth

            self.blocks[3].x = self.x + blockWidth
            self.blocks[3].y = self.y + blockWidth

        elif self.state == 2:
            # 0 1 2
            # 3
            # the center is 1
            self.blocks[0].x = self.x - blockWidth
            self.blocks[0].y = self.y

            self.blocks[1].x = self.x
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x + blockWidth
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x - blockWidth
            self.blocks[3].y = self.y + blockWidth

        elif self.state == 3:
            # 0 1
            #   2
            #   3
            #the center is 2
            self.blocks[0].x = self.x - blockWidth
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x
            self.blocks[1].y = self.y - blockWidth

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x
            self.blocks[3].y = self.y + blockWidth

class Oshape(TetrisShape):
    def __init__(self, x, y, state, color):
        self.state = state
        self.x = x
        self.y = y
        self.color = color
        self.blocks = [pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth)]
        self.setup()
        self.isFalling = True

    def setup(self):
        # 0 1
        # 2 3
        #center is the middle
        self.blocks[0].x = self.x - blockWidth
        self.blocks[0].y = self.y - blockWidth

        self.blocks[1].x = self.x
        self.blocks[1].y = self.y - blockWidth

        self.blocks[2].x = self.x - blockWidth
        self.blocks[2].y = self.y

        self.blocks[3].x = self.x
        self.blocks[3].y = self.y

class Sshape(TetrisShape):
    def __init__(self, x, y, state, color):
        self.x = x
        self.y = y
        self.color = color
        self.blocks = [pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth)]
        self.state = state
        self.setup()
        self.isFalling = True


    def setup(self):
        if self.state == 0:
            #   0 1
            # 2 3
            # the center is the 0
            self.blocks[0].x = self.x
            self.blocks[0].y = self.y

            self.blocks[1].x = self.x + blockWidth
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x - blockWidth
            self.blocks[2].y = self.y + blockWidth

            self.blocks[3].x = self.x
            self.blocks[3].y = self.y + blockWidth

        elif self.state == 1:
            # 0
            # 1 2
            #   3
            # the center is the 2
            self.blocks[0].x = self.x - blockWidth
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x - blockWidth
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x
            self.blocks[3].y = self.y + blockWidth

        elif self.state == 2:
            #   0 1
            # 2 3
            # the center is the 3
            self.blocks[0].x = self.x
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x + blockWidth
            self.blocks[1].y = self.y - blockWidth

            self.blocks[2].x = self.x - blockWidth
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x
            self.blocks[3].y = self.y

        elif self.state == 3:
            # 0
            # 1 2
            #   3
            # the center is the 1
            self.blocks[0].x = self.x
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x + blockWidth
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x + blockWidth
            self.blocks[3].y = self.y + blockWidth


class Tshape(TetrisShape):
    def __init__(self, x, y, state, color):
        self.x = x
        self.y = y
        self.color = color
        self.blocks = [pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth)]
        self.state = state
        self.setup()
        self.isFalling = True

    def setup(self):
        #   0
        # 1 2 3
        # the center is the 2
        if self.state == 0:
            self.blocks[0].x = self.x
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x - blockWidth
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x + blockWidth
            self.blocks[3].y = self.y
            
        elif self.state == 1:
            # 0
            # 1 2
            # 3
            # the center is the 1
            self.blocks[0].x = self.x
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x + blockWidth
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x
            self.blocks[3].y = self.y + blockWidth
            
        elif self.state == 2:
            # 0 1 2
            #   3
            # the center is the 1
            self.blocks[0].x = self.x - blockWidth
            self.blocks[0].y = self.y

            self.blocks[1].x = self.x
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x + blockWidth
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x
            self.blocks[3].y = self.y + blockWidth
            
        elif self.state == 3:
            #   0
            # 1 2
            #   3
            # the center is the 2
            self.blocks[0].x = self.x
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x - blockWidth
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x
            self.blocks[3].y = self.y + blockWidth


class Zshape(TetrisShape):
    def __init__(self, x, y, state, color):
        self.x = x
        self.y = y
        self.color = color
        self.blocks = [pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth), pygame.Rect(0,0,blockWidth,blockWidth)]
        self.state = state
        self.setup()
        self.isFalling = True

    def setup(self):
        if self.state == 0:
            # 0 1
            #   2 3
            # the center is the 1
            self.blocks[0].x = self.x - blockWidth
            self.blocks[0].y = self.y

            self.blocks[1].x = self.x
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y + blockWidth

            self.blocks[3].x = self.x + blockWidth
            self.blocks[3].y = self.y + blockWidth
            
        elif self.state == 1:
            #   0
            # 1 2
            # 3
            # the center is the 2
            self.blocks[0].x = self.x
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x - blockWidth
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x - blockWidth
            self.blocks[3].y = self.y + blockWidth
            
        elif self.state == 2:
            # 0 1
            #   2 3
            # the center is the 2
            self.blocks[0].x = self.x - blockWidth
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x
            self.blocks[1].y = self.y - blockWidth

            self.blocks[2].x = self.x
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x + blockWidth
            self.blocks[3].y = self.y
            
        elif self.state == 3:
            #   0
            # 1 2
            # 3
            # the center is at 1
            self.blocks[0].x = self.x + blockWidth
            self.blocks[0].y = self.y - blockWidth

            self.blocks[1].x = self.x
            self.blocks[1].y = self.y

            self.blocks[2].x = self.x + blockWidth
            self.blocks[2].y = self.y

            self.blocks[3].x = self.x
            self.blocks[3].y = self.y + blockWidth
