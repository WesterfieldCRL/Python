from graphics import *

win = GraphWin("Box", 500, 500)

test = Rectangle(Point(250,0), Point(200,10))

test.draw(win)

while True:
    if win.closed:
        exit()
    test.move(.05,0)