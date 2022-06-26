import pygame
from abc import ABC, abstractmethod
import time
import os
import random
from turtle import up
import colorama
import keyboard
import threading
from collections import deque

colorama.init()
start = "\033[1;31m"
end = "\033[0;0m"
#print( "File is: " + start + "<placeholder>" + end)

eventQueue = deque()

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

    def pieceOverlaps(self, otherPiece):
        return self.overlaps(otherPiece.blocks)

    


        
            
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


board = [[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", ".", ".", "."]]

gameOver = False
def printBoard():
    for j in range(20):
        for i in range(10):
            print(board[j][i], end=" ")
        print()
 
def clearBoard():
    for j in range(20):
        for i in range(10):
            board[j][i] = "."

def summon():
    global gameOver
    rand = random.randint(1, 7) 
    if rand == True:
        shape = Line(4, 3, 0)
    elif rand == 2:
        shape = Jshape(4, 2, 0)
    elif rand == 3:
        shape = Lshape(5, 2, 0)
    elif rand == 4:
        shape = Oshape(4, 2)
    elif rand == 5:
        shape = Sshape(4, 2, 0)
    elif rand == 6:
        shape = Tshape(4, 2, 0)
    elif rand == 7:
        shape = Zshape(4, 2, 0)
    
    for piece in gamePieces:
        gameOver = shape.pieceOverlaps(piece)
        
    gamePieces.append(shape)



def setPiece(shape):
    for i in range(4):
        y = shape.blocks[i][0]
        x = shape.blocks[i][1]
        
        if x < 11 - shape.wideRight and x >= -1 + shape.wideLeft:
            if x > 10 - shape.wideRight:
                x = 10 - shape.wideRight
            elif x < 0 + shape.wideLeft:
                x = 0 + shape.wideLeft
            if isinstance(shape, Line):
                board[y][x] = '\u001b[36;1mx\u001b[0m'
            elif isinstance(shape, Lshape):
                board[y][x] = "\u001b[33mx\u001b[0m"
            elif isinstance(shape, Jshape):
                board[y][x] = "\u001b[34mx\u001b[0m"
            elif isinstance(shape, Oshape):
                board[y][x] = "\u001b[33;1mx\u001b[0m"
            elif isinstance(shape, Sshape):
                board[y][x] = "\u001b[32mx\u001b[0m"
            elif isinstance(shape, Tshape):
                board[y][x] = "\u001b[35mx\u001b[0m"
            elif isinstance(shape, Zshape):
                board[y][x] = "\u001b[31mx\u001b[0m"
        

gamePieces = []

def dropPiece(piece):
    shiftedBlocks = piece.shiftDown()
    
    for frozenPieces in gamePieces[:-1]:
        if (frozenPieces.overlaps(shiftedBlocks)):
            return False
    return piece.fall()


def canMoveLeft(piece):
    shiftedBlocks = piece.shiftLeft()

    for frozenPieces in gamePieces[:-1]:
        if (frozenPieces.overlaps(shiftedBlocks)):
            return False
    
    for block in shiftedBlocks:
        if block[1] <= -1:
            return False
    
    
    return True

def canMoveRight(piece):
    shiftedBlocks = piece.shiftRight()

    for frozenPieces in gamePieces[:-1]:
        if (frozenPieces.overlaps(shiftedBlocks)):
            return False
    
    for block in shiftedBlocks:
        if block[1] > 9:
            return False
    return True

def left_key_pressed(event):
     if len(gamePieces) > 0:
        if gamePieces[-1].isFalling == True and canMoveLeft(gamePieces[-1]):
            gamePieces[-1].x -= 1

        os.system("CLS")
        clearBoard()

        setPiece(gamePieces[-1])
        eventQueue.append("CLEAR")
def right_key_pressed(event):
    if len(gamePieces) > 0:
        if gamePieces[-1].isFalling == True and canMoveRight(gamePieces[-1]):
            gamePieces[-1].x += 1

        os.system("CLS")
        clearBoard()

        setPiece(gamePieces[-1])
        print("v")
        eventQueue.append("CLEAR")

sleepytime = .25
sleepyoriginal = .25
def down_key_pressed(event):
    global sleepytime
    if sleepytime == sleepyoriginal:
        sleepytime = sleepytime/4
    eventQueue.append("CLEAR")

def down_key_released(event):
    global sleepytime
    if sleepytime == sleepyoriginal/4:
        sleepytime = 4 * sleepytime
    eventQueue.append("CLEAR")
    

def up_key_pressed(event):
    if len(gamePieces) > 1:
        gamePieces[-1].rotate()
    else:
        gamePieces[0].rotate()

    os.system("CLS")
    clearBoard()

    setPiece(gamePieces[-1])
    eventQueue.append("CLEAR")
"""def eventLoop():
    
    #for piece in gamePieces:
    #    setPiece(piece)
    keyboard.on_press_key("left", left_key_pressed)
    keyboard.on_press_key("right", right_key_pressed)
    keyboard.on_press_key("down", down_key_pressed)
    keyboard.on_release_key("down", down_key_released)
    keyboard.on_press_key("up", up_key_pressed)
    printBoard()
    count = 0
    while not gameOver:
        
        time.sleep(sleepytime)
        os.system("CLS")
        clearBoard()
        if len(gamePieces) == 0:
            summon()
        else:
            for piece in gamePieces[:-1]:
                print("not last piece")
                setPiece(piece)
            lastPiece = gamePieces[-1]
            fallen = dropPiece(lastPiece)
            print("last piece")
            setPiece(lastPiece)
            if not fallen:
                lastPiece.isFalling = False
                summon()
        printBoard()"""

#eventLoop()

#summon()
#setPiece(gamePieces[0])
#printBoard()



def movement_task():
    loopCount = 0
    while gameOver == False:
        time.sleep(sleepytime)
        clearBoard()
        if len(gamePieces) == 0:
            summon()
        for piece in gamePieces[:-1]:
            setPiece(piece)
        lastPiece = gamePieces[-1]
        fallen = dropPiece(lastPiece)
        setPiece(lastPiece)
        if not fallen:
            lastPiece.isFalling = False
            summon()
        eventQueue.append("CLEAR")

        


        

def gui_task():
    while gameOver == False:
        if len(eventQueue) > 0:
            event = eventQueue.popleft()
            if event == "CLEAR":
                os.system("CLS")
                printBoard()

gui_thread = threading.Thread(target=gui_task)
movement_thread = threading.Thread(target=movement_task)


keyboard.on_press_key("left", left_key_pressed)
keyboard.on_press_key("right", right_key_pressed)
keyboard.on_press_key("down", down_key_pressed)
keyboard.on_release_key("down", down_key_released)
keyboard.on_press_key("up", up_key_pressed)

gui_thread.daemon = True
gui_thread.start()
movement_thread.daemon = True
movement_thread.start()

while not gameOver:
    time.sleep(2)

movement_thread.join()
gui_thread.join()
print("Done")

