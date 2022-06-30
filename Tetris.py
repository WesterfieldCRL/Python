import pygame
import TetrisShape
import time
import random
from abc import ABC, abstractmethod
 
pygame.init()

blockWidth = 10


screenWidth = 200
screenHeight = 400

blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
amber = (255,191,0)
pistachio = (147,197,114)
lightBlue = (43,181,212)
purple = (185,43,212)

gameOver = False

gamePieces = []

#this is virtually unchanged from the original code, just added color
def summon():
    rand = random.randint(1, 7) 
    if rand == True:
        shape = TetrisShape.Line(screenWidth/2, 0, 0, blue)
    elif rand == 2:
        shape = TetrisShape.Jshape(screenWidth/2, 0, 0, red)
    elif rand == 3:
        shape = TetrisShape.Lshape(screenWidth/2, 0, 0, green)
    elif rand == 4:
        shape = TetrisShape.Oshape(screenWidth/2, 0, 0, amber)
    elif rand == 5:
        shape = TetrisShape.Sshape(screenWidth/2, 0, 0, pistachio)
    elif rand == 6:
        shape = TetrisShape.Tshape(screenWidth/2, 0, 0, lightBlue)
    elif rand == 7:
        shape = TetrisShape.Zshape(screenWidth/2, 0, 0, purple)
        
    gamePieces.append(shape)

screen = pygame.display.set_mode((screenWidth, screenHeight))
start_time = time.time()

summon()

#game loop
while not gameOver:

    #gets input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                gameOver = True
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_RIGHT:
                gamePieces[-1].ShiftRight(gamePieces[:-1], screenWidth)
            if event.key == pygame.K_LEFT:
                gamePieces[-1].ShiftLeft(gamePieces[:-1])
            if event.key == pygame.K_UP:
                gamePieces[-1].rotate()
            #currently does not work when held
            if event.key == pygame.K_DOWN:
                gamePieces[-1].ShiftDown(gamePieces[:-1])
        
    #loops every .1 seconds, causes the piece to fall
    if time.time() - start_time > .1:
        start_time = time.time()
        if not gamePieces[-1].fall(screenHeight,gamePieces):
            summon()
            if not gamePieces[-1].fall(screenHeight,gamePieces):
                gameOver = True


    #clears the screen
    screen.fill((255,255,255))
    
    #draws the game pieces
    for i in gamePieces[:]:
            i.DrawShape(screen)
    #draws a grid on the screen
    for x in range(0,screenWidth, blockWidth):
        pygame.draw.rect(screen,(0,0,0), pygame.Rect(x,0,1,screenHeight))
    for y in range(0,screenHeight, blockWidth):
        pygame.draw.rect(screen,(0,0,0), pygame.Rect(0,y,screenWidth,1))

    #idk what this does but its necessary
    pygame.display.flip()

print('Done')