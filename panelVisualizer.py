
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

    #This function sets the given pixel in the canvas to the set pixel value
    #index from 0!
    def set_pixel(self, row, col, pixel):
        self.canvasPixels[row * self.numColumns + col * self.numRows].setFill(color_rgb(pixel.r, pixel.g, pixel.b))
    #this keeps the panel open, which is kind of silly
    def wait_for_exit(self):
        self.win.getMouse() # Pause to view result
        self.win.close()    # Close window when done

    #this is handed a Panel() object that we display
    #for now we assume the panel is the same size as we were initialized to
    # def display_visualizer_panel( panel_to_display)



def main():
    panel = PanelVisualizer(5, 6)
    pix = Pixel(10, 40, 50)
    panel.set_pixel(0,2, pix)
    panel.wait_for_exit()

main()
