
from graphics import * #import the graphics
from classes import *
class PanelVisualizer():
    canvasWidth = 500
    canvasHeight = 500
    pixelDistance = 10 #this is how much distance we put between pixels
    # canvasPixels
    numColumns = 0
    numRows = 0
    win = GraphWin("My Circle", canvasWidth, canvasHeight)
    def __init__(self, number_of_columns, number_of_rows):
        self.numColumns = number_of_columns
        self.numRows = number_of_rows
        self.pixelDistance = self.canvasWidth / (self.numColumns+1)
        self.canvasHeight = self.pixelDistance*(self.numRows+1)
        self.canvasPixels = [Circle(Point(0,0),10) for n in range(self.numRows*self.numColumns) ]
        for i in range(self.numRows):
            for j in range(self.numColumns):
                self.canvasPixels[i*self.numColumns + j].move((i+.5)*self.pixelDistance, (j+.5)*self.pixelDistance)
                self.canvasPixels[i*self.numColumns + j].draw(self.win)


    def set_pixel(self, row, col, pixel):
        pixel.print_colors()
        self.canvasPixels[row * self.numColumns + col * self.numRows].setFill('red')
    def wait_for_exit(self):
        self.win.getMouse() # Pause to view result
        self.win.close()    # Close window when done
def main():
    panel = PanelVisualizer(5, 6)
    pix = Pixel(10, 40, 50)
    panel.set_pixel(1,2, pix)
    panel.wait_for_exit()

main()
