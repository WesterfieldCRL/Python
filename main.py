from graphics import *

x = .03
y = .03

win = GraphWin("My Circle", 500, 500)

dvd = Text(Point(250,0), 'DVD')

dvd.draw(win)



while True:
    if win.closed:
        exit()
    if dvd.getAnchor().getX() < 0 or dvd.getAnchor().getX() > 500:
        x*=-1
    if dvd.getAnchor().getY() < 0 or dvd.getAnchor().getY() > 500:
        y*=-1
    dvd.move(x,y)