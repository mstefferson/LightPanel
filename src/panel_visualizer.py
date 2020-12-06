from __future__ import print_function
from graphics import * #import the graphics
from classes import Pixel

class PanelVisualizer():
    canvasWidth = 2000
    canvasHeight = 800
    pixelDistance = 10 #this is how much distance we put between pixels
    offsetRows = False #This is how we track if the every other row has an offset
    # canvasPixels
    numColumns = 0
    numRows = 0
    win = GraphWin("My Circle", canvasWidth, canvasHeight,autoflush=False)
    def __init__(self, number_of_rows, number_of_columns, offset_rows ):
        self.numColumns = number_of_columns
        self.numRows = number_of_rows
        self.offsetRows = offset_rows
        self.pixelDistance = self.canvasWidth / (self.numColumns+1)
        self.canvasHeight = self.pixelDistance*(self.numRows+1)
        self.circle_size = 10
        if(self.pixelDistance < self.circle_size) :
            self.circle_size = self.pixelDistance/2
        print("Init of PanelVisualizer. pixel size: ", self.circle_size, " canvas width: ", self.canvasWidth, "pixelDistance: " , self.pixelDistance);

        self.canvasPixels = [Circle(Point(0,0),self.circle_size) for n in range(self.numRows*self.numColumns) ]
        for i in range(self.numRows):
            for j in range(self.numColumns):
                if i %2 == 1 and self.offsetRows == True:
                    row_offset = 1
                else: row_offset = 0.5
                self.canvasPixels[i*self.numColumns + j].move((j+row_offset)*self.pixelDistance, (i+.5)*self.pixelDistance)
                self.canvasPixels[i*self.numColumns + j].draw(self.win)

    #This function sets the given pixel in the canvas to the set pixel value
    #index from 0!
    def set_pixel(self, col, row, pixel):
        # print(col, " ", row)
        if( pixel.is_off() == True ):
            pixel.to_white()
        self.canvasPixels[row * self.numColumns + col ].setFill(color_rgb(pixel.r, pixel.g, pixel.b))
    #this keeps the panel open, which is kind of silly
    def wait_for_exit(self):
        self.win.getMouse() # Pause to view result
        self.win.close()    # Close window when done

    #this is handed a list of lists of pixels [r][c]
    #for now we assume the panel is the same size as we were initialized to
    def display_visualizer_panel(self, pixel_arr ):
        #iterate over all rows
        for i in range(self.numRows ):
            #move through the row
            for j in range( self.numColumns ) :
                self.set_pixel( j, i, pixel_arr[i][j] )
        self.win.update()
