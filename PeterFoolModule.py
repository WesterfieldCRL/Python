from abc import ABC, abstractmethod
class TetrisShape(ABC):
    def __init__(self, state, x, y):
        self.state = state
        self.x = x
        self.y = y
        self.blocks = [(0, 0), (0, 0), (y, x),(0, 0)]
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
    
    def shiftDown(self):
        retVal = []
        for i in range(4):
            retVal.append((self.blocks[i][0]+1, self.blocks[i][1]))
        return retVal

    def shiftLeft(self):
        retVal = []
        for i in range(4):
            retVal.append((self.blocks[i][0], self.blocks[i][1]-1))
        return retVal
    def shiftRight(self):
        retVal = []
        for i in range(4):
            retVal.append((self.blocks[i][0], self.blocks[i][1]+1))
        return retVal
    
    
    def overlaps(self, otherBlocks):
        for i in range(4):
            for j in range(4):
                if (self.blocks[i][0] == otherBlocks[j][0]) and (self.blocks[i][1] == otherBlocks[j][1]):
                    return True
        return False
        
            
    @abstractmethod
    def setup():
        pass

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

        
class Jshape(TetrisShape):
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.blocks = [(0, 0), (0, 0), (y, x), (0, 0)]
        self.state = state
        self.setup()
        self.isFalling = True

    def setup(self):
        if self.state == 0:
            self.blocks[0] = (self.y-1, self.x-1)   # x
            self.blocks[1] = (self.y, self.x-1)     # x o x
            self.blocks[2] = (self.y, self.x)
            self.blocks[3] = (self.y, self.x+1)
            self.bottomNum = 0
            self.wideRight = 1
            self.wideLeft = 0
        elif self.state == 1:
            self.blocks[0] = (self.y-1, self.x)     # x x
            self.blocks[1] = (self.y-1, self.x+1)   # o
            self.blocks[2] = (self.y, self.x)       # x
            self.blocks[3] = (self.y+1, self.x)
            self.bottomNum = 1
            self.wideRight = 1
            self.wideLeft = 0
        elif self.state == 2:
            self.blocks[0] = (self.y, self.x-1)     # x o x
            self.blocks[1] = (self.y, self.x)       #     x
            self.blocks[2] = (self.y, self.x+1)
            self.blocks[3] = (self.y+1, self.x+1)
            self.bottomNum = 1
            self.wideRight = 1
            self.wideLeft = 1
        elif self.state == 3:
            self.blocks[0] = (self.y-1, self.x)     # x
            self.blocks[0] = (self.y, self.x)       # o
            self.blocks[0] = (self.y+1, self.x-1)   # x x
            self.blocks[0] = (self.y+1, self.x)
            self.bottomNum = 1
            self.wideRight = 0
            self.wideLeft = 1

class Lshape(TetrisShape):
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.blocks = [(0, 0), (0, 0), (y, x), (0, 0)]
        self.state = state
        self.setup()
        self.isFalling = True

    def setup(self):
        if self.state == 0:
            self.blocks[0] = (self.y-1, self.x+1)   #     x
            self.blocks[1] = (self.y, self.x-1)     # x o x
            self.blocks[2] = (self.y, self.x)
            self.blocks[3] = (self.y, self.x+1)
            self.bottomNum = 0
            self.wideRight = 1
            self.wideLeft = 0
        elif self.state == 1:
            self.blocks[0] = (self.y-1, self.x)     # x
            self.blocks[1] = (self.y, self.x)       # o
            self.blocks[2] = (self.y+1, self.x)     # x x
            self.blocks[3] = (self.y+1, self.x+1)
            self.bottomNum = 1
            self.wideRight = 1
            self.wideLeft = 0
        elif self.state == 2:
            self.blocks[0] = (self.y, self.x-1)     # x o x
            self.blocks[1] = (self.y, self.x)       # x
            self.blocks[2] = (self.y, self.x+1)
            self.blocks[3] = (self.y+1, self.x+1)
            self.bottomNum = 1
            self.wideRight = 1
            self.wideLeft = 1
        elif self.state == 3:
            self.blocks[0] = (self.y-1, self.x-1)   # x x
            self.blocks[1] = (self.y-1, self.x)     #   o
            self.blocks[2] = (self.y, self.x)       #   x
            self.blocks[3] = (self.y+1, self.x)
            self.bottomNum = 1
            self.wideRight = 0
            self.wideLeft = 1

class Oshape(TetrisShape):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blocks = [(y-1, x), (y-1, x+1), (y, x), (y, x+1)]
        self.setup()
        self.isFalling = True

    def setup(self):
        self.blocks[0] = (self.y-1, self.x)
        self.blocks[1] = (self.y-1, self.x+1)
        self.blocks[2] = (self.y, self.x)
        self.blocks[3] = (self.y, self.x+1)
        self.bottomNum = 0
        self.wideRight = 1
        self.wideLeft = 0

class Sshape(TetrisShape):
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.blocks = [(0, 0), (0, 0), (y, x), (0, 0)]
        self.state = state
        self.setup()
        self.isFalling = True


    def setup(self):
        if self.state == 0:
            self.blocks[0] = (self.y, self.x)       #   o x
            self.blocks[1] = (self.y, self.x+1)     # x x
            self.blocks[2] = (self.y+1, self.x-1)
            self.blocks[3] = (self.y+1, self.x)
            self.bottomNum = 1
            self.wideRight = 1
            self.wideLeft = 0
        elif self.state == 1:
            self.blocks[0] = (self.y-1, self.x-1)   # x
            self.blocks[1] = (self.y, self.x-1)     # x o
            self.blocks[2] = (self.y, self.x)       #   x
            self.blocks[3] = (self.y+1, self.x)
            self.bottomNum = 1
            self.wideRight = 0
            self.wideLeft = 1
        elif self.state == 2:
            self.blocks[0] = (self.y-1, self.x)     #   x x
            self.blocks[1] = (self.y-1, self.x+1)   # x o
            self.blocks[2] = (self.y, self.x-1)
            self.blocks[3] = (self.y, self.x)
            self.bottomNum = 0
            self.wideRight = 1
            self.wideLeft = 1
        elif self.state == 3:
            self.blocks[0] = (self.y-1, self.x)     # x
            self.blocks[1] = (self.y, self.x)       # o x
            self.blocks[2] = (self.y, self.x+1)     #   x
            self.blocks[3] = (self.y+1, self.x+1)
            self.bottomNum = 1
            self.wideRight = 1
            self.wideLeft = 0


class Tshape(TetrisShape):
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.blocks = [(0, 0), (0, 0), (y, x), (0, 0)]
        self.state = state
        self.setup()
        self.isFalling = True

    def setup(self):
        if self.state == 0:
            self.blocks[0] = (self.y-1, self.x)     #   x
            self.blocks[1] = (self.y, self.x-1)     # x o x
            self.blocks[2] = (self.y, self.x)
            self.blocks[3] = (self.y, self.x+1)
            self.bottomNum = 0
            self.wideRight = 1
            self.wideLeft = 0
        elif self.state == 1:
            self.blocks[0] = (self.y-1, self.x)     # x
            self.blocks[1] = (self.y, self.x)       # o x
            self.blocks[2] = (self.y, self.x+1)     # x
            self.blocks[3] = (self.y+1, self.x)
            self.bottomNum = 1
            self.wideRight = 1
            self.wideLeft = 0
        elif self.state == 2:
            self.blocks[0] = (self.y, self.x-1)     # x o x
            self.blocks[1] = (self.y, self.x)       #   x
            self.blocks[2] = (self.y, self.x+1)
            self.blocks[3] = (self.y+1, self.x)
            self.bottomNum = 1
            self.wideRight = 1
            self.wideLeft = 1
        elif self.state == 3:
            self.blocks[0] = (self.y-1, self.x)     #   x
            self.blocks[1] = (self.y, self.x-1)     # x o
            self.blocks[2] = (self.y, self.x)       #   x
            self.blocks[3] = (self.y+1, self.x)
            self.bottomNum = 1
            self.wideRight = 0
            self.wideLeft = 1


class Zshape(TetrisShape):
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.blocks = [(0, 0), (0, 0), (y, x), (0, 0)]
        self.state = state
        self.setup()
        self.isFalling = True

    def setup(self):
        if self.state == 0:
            self.blocks[0] = (self.y, self.x-1)     # x o
            self.blocks[1] = (self.y, self.x)       #   x x
            self.blocks[2] = (self.y+1, self.x)
            self.blocks[3] = (self.y+1, self.x+1)
            self.bottomNum = 1
            self.wideRight = 1
            self.wideLeft = 1
        elif self.state == 1:
            self.blocks[0] = (self.y-1, self.x)     #   x
            self.blocks[1] = (self.y, self.x-1)     # x o
            self.blocks[2] = (self.y, self.x)       # x
            self.blocks[3] = (self.y+1, self.x-1)
            self.bottomNum = 1
            self.wideRight = 0
            self.wideLeft = 1
        elif self.state == 2:
            self.blocks[0] = (self.y-1, self.x-1)   # x x
            self.blocks[1] = (self.y-1, self.x)     #   o x
            self.blocks[2] = (self.y, self.x)
            self.blocks[3] = (self.y, self.x+1)
            self.bottomNum = 0
            self.wideRight = 1
            self.wideLeft = 1
        elif self.state == 3:
            self.blocks[0] = (self.y-1, self.x+1)   #   x
            self.blocks[1] = (self.y, self.x)       # o x
            self.blocks[2] = (self.y, self.x+1)     # x
            self.blocks[3] = (self.y+1, self.x)
            self.bottomNum = 1
            self.wideRight = 1
            self.wideLeft = 0