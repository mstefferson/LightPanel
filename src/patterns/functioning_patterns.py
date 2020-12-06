# functioning_patterns
#
from classes import Pixel
import random

# this is a template pattern all patterns are inherit
class PanelPattern():
    def __init__(self , m, n):
        self.call_name = 'panel';
        # row and columns
        self.m = m
        self.n = n
        # # of seconds to pause between fame updates.
        # this is the refresh speed of our panel.
        # Much faster than 0. 1 seems to piss off my computer
        self.frame_sleep_time = 0.1
        # pattern array
        self.pixel_arr = [ [Pixel(0,0,0) for i in range( self.n ) ]
            for j in range(self.m) ]
    # method that should be overridden
    ## update_pixel_arr: change the pixel array when called
    def update_pixel_arr(self):
        # update and change the pixel array
        self.pixel_arr = [ [Pixel(0,0,0) for i in range( self.n ) ]
            for j in range(self.m) ]
    # these methods should be be changed
    ## get_pixel_arr: returns current pixel array
    def get_pixel_arr(self):
        #then return the pixel_array
        return self.pixel_arr
    ## wipe_pixel_arr: sets all pixels to zero
    def wipe_pixel_arr(self):
        #set all pixels in array to zero
        self.pixel_arr = [ [Pixel(0,0,0) for i in range( self.n ) ]
            for j in range(self.m) ]
    ## update_and_get_pixel_arr: returns current pixel array
    def update_and_get_pixel_arr(self):
        self.update_pixel_arr()
        return self.pixel_arr

# example pattern
class ExamplePattern(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__( self, m, n )
        self.call_name = 'example';

# worm pattern
class WormPattern(PanelPattern):
    def __init__(self , m, n):
        PanelPattern.__init__( self, m, n )
        self.call_name = 'worm';
        self.increment = 6
        self.lastr = 0
        self.lastg = 125
        self.lastb = 252
        self.multr = 1
        self.multb = .5
        self.multg = .75
        self.MAX_VAL = 150
        self.MIN_VAL = 20

    #fills in a rectangle of a color into the pixel array given
    def fill_rect_edge( self, offset):
        tr = offset*self.increment*self.multr
        tg = offset*self.increment *self.multg
        tb = offset*self.increment*self.multb
        for j in range ( offset, len(self.pixel_arr[0]) -offset):
            for i in range ( offset, len(self.pixel_arr) -offset ):
                self.pixel_arr[i][j] = Pixel( self.lastr+tr , self.lastb+tb, self.lastg+tg)

    def update_pixel_arr(self):
        self.lastr +=  self.increment*self.multr
        self.lastg += self.increment*self.multg
        self.lastb += self.increment*self.multb

        if self.lastr > self.MAX_VAL :
            self.lastr =self.MAX_VAL
            self.multr *= -1
        if self.lastr <self.MIN_VAL:
            self.lastr =self.MIN_VAL
            self.multr *= -1
        if self.lastb >self.MAX_VAL :
            self.lastb =self.MAX_VAL
            self.multb *= -1
        if self.lastb <self.MIN_VAL:
            self.lastb =self.MIN_VAL
            self.multb *= -1
        if self.lastg >self.MAX_VAL :
            self.lastg =self.MAX_VAL
            self.multg *= -1
        if self.lastg <self.MIN_VAL:
            self.lastg =self.MIN_VAL
            self.multg *= -1
        #move through each row
        for i in range( int ( self.m / 2 )  ):
            self.fill_rect_edge( i)

class TestPattern(PanelPattern):
    MAX_VAL = 236
    MIN_VAL = 20
    def __init__(self , m , n):
        PanelPattern.__init__( self, m, n )
        self.call_name = 'test';
        self.increment = 6
        self.lastr = 0
        self.lastg = 125
        self.lastb = 252
        self.multr = 1
        self.multb = .5
        self.multg = .75

    #this is an example application that loads some pixels
    #into the panel for display
    def update_pixel_arr(self):
        #move through each row
        for i in range( self.m):
            #move through the column
            for j in range( self.n ):
                self.pixel_arr[i][j] = Pixel( i*(220/self.m) , j*(220/self.n) , i+j)

# randwalk pattern starts with partially lit white pixels, and randomly permutes pixels from there
class RandwalkPattern(PanelPattern):
    def __init__(self, m, n, numwalkers):
        PanelPattern.__init__( self, m, n )
        self.call_name = 'randwalk';
        #move through each row
        for i in range( self.m):
            #move through the column
            for j in range( self.n ):
                self.pixel_arr[i][j] = Pixel( 50,50,50)

    #This takes a value, alters it by a random amt and then returns taht alterd value
    def permute_val(self, value):
        MAX_VAL = 150
        value = value + random.randint(-5,5)
        if(value < 0):
            value =0
        elif value>MAX_VAL:
            value = MAX_VAL
        return value

    #this is an example application that loads some pixels
    #into the panel for display
    def update_pixel_arr(self):
        #move through each row
        for i in range( self.m):
            #move through the column
            for j in range( self.n ):
                curr_pixel = self.pixel_arr[i][j]
                self.pixel_arr[i][j] = Pixel( self.permute_val(curr_pixel.r) , self.permute_val(curr_pixel.g) , self.permute_val(curr_pixel.b))
