
from graphics import * #import the graphics
from classes import *

def main():
    win = GraphWin("My Circle", 100, 100)
    c = Circle(Point(50,50), 10)
    c.setFill('red');
    c.draw(win)
    win.getMouse() # Pause to view result
    win.close()    # Close window when done

main()

#def drawPixel(row, col, pixel):
