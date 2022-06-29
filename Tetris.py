import pygame
import TetrisShape
import time
from abc import ABC, abstractmethod
 
pygame.init()

blockWidth = 10


screenWidth = 500
screenHeight = 800

Shapes = []

Shapes.append(TetrisShape.Line(40, 40, 0))
Shapes.append(TetrisShape.Zshape(80, 40, 0))
Shapes.append(TetrisShape.Lshape(120, 40, 0))
Shapes.append(TetrisShape.Sshape(160, 40, 0))
Shapes.append(TetrisShape.Oshape(200, 40, 0))
Shapes.append(TetrisShape.Jshape(240, 40, 0))
Shapes.append(TetrisShape.Tshape(280, 40, 0))
ShapeLine = TetrisShape.Line(280, 40, 0)
screen = pygame.display.set_mode((screenWidth, screenHeight))

blue = (0,0,255)

done = False
start_time = time.time()

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            ShapeLine.rotate()
        

    #if time.time() - start_time > .1:
        #start_time = time.time()
        #for i in Shapes[:]:
            #i.fall(screenHeight)

    
    screen.fill((255,255,255))
    
    for i in Shapes[:]:
            i.DrawShape(screen,blue)
    for x in range(0,screenWidth, blockWidth):
        pygame.draw.rect(screen,(0,0,0), pygame.Rect(x,0,1,screenHeight))
    for y in range(0,screenHeight, blockWidth):
        pygame.draw.rect(screen,(0,0,0), pygame.Rect(0,y,screenWidth,1))

    pygame.display.flip()