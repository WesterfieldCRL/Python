from graphics import *

window = GraphWin("Drawing Time", 800, 800)

box = Rectangle(Point(10,10),Point(300,300))

box.draw(window)

window.getMouse()

box.move(100,0)

window.getMouse()