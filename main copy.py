from graphics import *

x = .03
y = .03

win = GraphWin("My Circle", 500, 500)

dvd = Text(Point(250,0), 'DVD')

dvd.draw(win)



while True:
    if win.closed:
        exit()
    dvd.move(x,y)