#from abc import ABC, abstractmethod
import PeterFoolModule
import time
import os
import random
#from turtle import up
import colorama
import keyboard
import threading
from collections import deque

colorama.init()
start = "\033[1;31m"
end = "\033[0;0m"
#print( "File is: " + start + "<placeholder>" + end)

eventQueue = deque()



    

gamePieces = []

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
        shape = PeterFoolModule.Line(4, 3, 0)
    elif rand == 2:
        shape = PeterFoolModule.Jshape(4, 2, 0)
    elif rand == 3:
        shape = PeterFoolModule.Lshape(5, 2, 0)
    elif rand == 4:
        shape = PeterFoolModule.Oshape(4, 2)
    elif rand == 5:
        shape = PeterFoolModule.Sshape(4, 2, 0)
    elif rand == 6:
        shape = PeterFoolModule.Tshape(4, 2, 0)
    elif rand == 7:
        shape = PeterFoolModule.Zshape(4, 2, 0)
    
    for piece in gamePieces:
        gameOver = shape.overlaps(piece.blocks)
        
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
            if isinstance(shape, PeterFoolModule.Line):
                board[y][x] = '\u001b[36;1mx\u001b[0m'
            elif isinstance(shape, PeterFoolModule.Lshape):
                board[y][x] = "\u001b[33mx\u001b[0m"
            elif isinstance(shape, PeterFoolModule.Jshape):
                board[y][x] = "\u001b[34mx\u001b[0m"
            elif isinstance(shape, PeterFoolModule.Oshape):
                board[y][x] = "\u001b[33;1mx\u001b[0m"
            elif isinstance(shape, PeterFoolModule.Sshape):
                board[y][x] = "\u001b[32mx\u001b[0m"
            elif isinstance(shape, PeterFoolModule.Tshape):
                board[y][x] = "\u001b[35mx\u001b[0m"
            elif isinstance(shape, PeterFoolModule.Zshape):
                board[y][x] = "\u001b[31mx\u001b[0m"
        



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

    #the last block is the only falling one
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

