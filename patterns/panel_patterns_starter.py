from __future__ import print_function
# from panel_visualizer import *
from classes import *
from pixel import *
import time

MAX_VAL = 236
MIN_VAL = 20

class TestPanels():

    def __init__(self , panel_):
        self.increment = 6
        self.lastr = 0
        self.lastg = 125
        self.lastb = 252
        self.multr = 1
        self.multb = .5
        self.multg = .75
        self.panel = panel_
        self.pixel_arr = [ [Pixel(0,0,0) for i in range( self.panel.n ) ] for j in range(self.panel.m) ]

    #fills in a rectangle of a color into the pixel array given
    def fill_rect_edge( self, offset):
        tr = offset*self.increment*self.multr
        tg = offset*self.increment *self.multg
        tb = offset*self.increment*self.multb
        for j in range ( offset, len(self.pixel_arr[0]) -offset):
            for i in range ( offset, len(self.pixel_arr) -offset ):
                self.pixel_arr[i][j] = Pixel( self.lastr+tr , self.lastb+tb, self.lastg+tg)

    def simple_rectangles(self):
        print(self.lastr, end = "\n")
        self.lastr +=  self.increment*self.multr
        self.lastg += self.increment*self.multg
        self.lastb += self.increment*self.multb

        if self.lastr > MAX_VAL :
            self.lastr = MAX_VAL
            self.multr *= -1
        if self.lastr < MIN_VAL:
            self.lastr = MIN_VAL
            self.multr *= -1
        if self.lastb > MAX_VAL :
            self.lastb = MAX_VAL
            self.multb *= -1
        if self.lastb < MIN_VAL:
            self.lastb = MIN_VAL
            self.multb *= -1
        if self.lastg > MAX_VAL :
            self.lastg = MAX_VAL
            self.multg *= -1
        if self.lastg < MIN_VAL:
            self.lastg = MIN_VAL
            self.multg *= -1


        #move through each row
        for i in range( int ( self.panel.m / 2 )  ):
            self.fill_rect_edge( i)
        # self.panel.display_visualizer_panel(self.pixel_arr)
        return self.pixel_arr


    def simple_rectangles_animated(self):
        print("running simple_rectangles_animated")
        while True:
            time.sleep(.1)
            self.simple_rectangles()

    #this is an example application that loads some pixels
    #into the panel for display
    def simple_pixels(self):
        print("running simple_pixels")
        # pixel_arr = [ [0 for i in range( panel.numRows ) ] for j in range(panel.numColumns) ]
        #move through each row
        for i in range( self.panel.m):
            #move through the column
            for j in range( self.panel.n ):
                self.pixel_arr[i][j] = Pixel( i*(220/self.panel.m) , j*(220/self.panel.n) , i+j)
        # self.panel.display_visualizer_panel(self.pixel_arr)
        return self.pixel_arr
