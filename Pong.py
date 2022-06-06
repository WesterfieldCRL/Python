from graphics import *

xHeight = 500
yHeight = 500
ballXSpeed = .05
ballYSpeed = .01
cpuYSpeed = .5
keyPressedUp = False
keyPressedDown = False
key = ''

win = GraphWin("Pong", xHeight, yHeight)

PaddleUser = Rectangle(Point(xHeight/20,yHeight/6), Point((xHeight/20)*2,(yHeight/6)*2))
PaddleCPU = Rectangle(Point(xHeight-(xHeight/20),yHeight/6), Point(xHeight-((xHeight/20)*2),(yHeight/6)*2))
Ball = Circle(Point(xHeight/2,yHeight/2),xHeight/40)

PaddleUser.draw(win)
PaddleCPU.draw(win)
Ball.draw(win)


while True:
    if win.closed:
        exit()
    #check for balls collsion with sides
    if Ball.getP1().getX() < 0 or Ball.getP2().getX() > xHeight:
        ballXSpeed *= -1
    if Ball.getP1().getY() < 0 or Ball.getP2().getY() > xHeight:
        ballYSpeed *= -1
    #check for collision with cpu
    if (Ball.getP1().getY() > PaddleCPU.getP1().getY() and Ball.getP1().getY() < PaddleCPU.getP2().getY()) or (Ball.getP2().getY() < PaddleCPU.getP2().getY() and Ball.getP2().getY() > PaddleCPU.getP1().getY()):
        if Ball.getP2().getX() >= PaddleCPU.getP2().getX():
            ballXSpeed = -.05
    #check for collision with player
    if (Ball.getP1().getY() > PaddleUser.getP1().getY() and Ball.getP1().getY() < PaddleUser.getP2().getY()) or (Ball.getP2().getY() < PaddleUser.getP2().getY() and Ball.getP2().getY() > PaddleUser.getP1().getY()):
        if Ball.getP1().getX() <= PaddleUser.getP2().getX():
            ballXSpeed =.05
    #check for cpu collision with sides
    if PaddleCPU.getP2().getY() > yHeight or PaddleCPU.getP1().getY() < 0:
        cpuYSpeed *= -1

    #check for input

    key = win.checkKey()

    if key == 'Up':
         PaddleUser.move(0,-8)
    if key == 'Down':
        PaddleUser.move(0,8)

    #check for paddle collision with screen
    if PaddleUser.getP2().getY() > yHeight:
        PaddleUser.move(0,-8)
    if PaddleUser.getP1().getY() < 0:
        PaddleUser.move(0,8)



    Ball.move(ballXSpeed,ballYSpeed)
    PaddleCPU.move(0, cpuYSpeed)
