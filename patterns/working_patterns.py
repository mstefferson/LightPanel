from classes import Pixel

#this is a template pattern
class ExamplePattern():
    def __init__(self , m, n):
        self.m = m
        self.n = n
        self.pixel_arr = [ [Pixel(0,0,0) for i in range( self.n ) ] for j in range(self.m) ]

    #this function
    def get_pixel_arr(self):
        #do some mutation on the pixel array
        #then return the pixel_array
        return self.pixel_arr

class WormPattern():

    def __init__(self , m, n):
        self.increment = 6
        self.lastr = 0
        self.lastg = 125
        self.lastb = 252
        self.multr = 1
        self.multb = .5
        self.multg = .75
        self.m = m
        self.n = n
        self.MAX_VAL = 236
        self.MIN_VAL = 20
        self.pixel_arr = [ [Pixel(0,0,0) for i in range( self.n ) ] for j in range(self.m) ]

    #fills in a rectangle of a color into the pixel array given
    def fill_rect_edge( self, offset):
        tr = offset*self.increment*self.multr
        tg = offset*self.increment *self.multg
        tb = offset*self.increment*self.multb
        for j in range ( offset, len(self.pixel_arr[0]) -offset):
            for i in range ( offset, len(self.pixel_arr) -offset ):
                self.pixel_arr[i][j] = Pixel( self.lastr+tr , self.lastb+tb, self.lastg+tg)

    def get_pixel_arr(self):
        # print(self.lastr, end = "\n")
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
        # self.panel.display_visualizer_panel(self.pixel_arr)
        return self.pixel_arr

class TestPattern():
    MAX_VAL = 236
    MIN_VAL = 20
    def __init__(self , m , n):
        self.increment = 6
        self.lastr = 0
        self.lastg = 125
        self.lastb = 252
        self.multr = 1
        self.multb = .5
        self.multg = .75
        self.m = m
        self.n = n
        self.pixel_arr = [ [Pixel(0,0,0) for i in range( self.n ) ] for j in range(self.m) ]

    #this is an example application that loads some pixels
    #into the panel for display
    def get_pixel_arr(self):
        print("running simple_pixels")
        # pixel_arr = [ [0 for i in range( panel.numRows ) ] for j in range(panel.numColumns) ]
        #move through each row
        for i in range( self.m):
            #move through the column
            for j in range( self.n ):
                self.pixel_arr[i][j] = Pixel( i*(220/self.m) , j*(220/self.n) , i+j)
        # self.panel.display_visualizer_panel(self.pixel_arr)
        return self.pixel_arr
