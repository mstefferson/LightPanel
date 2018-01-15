# functioning_patterns
#
from classes import Pixel

# this is a template pattern all patterns are inherit
class PanelPattern():
    def __init__(self, config_dict):
        # default name
        self.type = 'panel';
        # config dict should contain all parameters you want to set
        # some defaults are set here just in case
        # row and columns. Arbitrarilty set to 10. 
        self.m = 10
        self.n = 10
        # set all default fields here
        # number of seconds to pause between fame updates
        self.frame_sleep_time = 0.1
        # reset inputs based on config
        self.set_inputs( config_dict )
        # pattern array
        self.pixel_arr = [ [Pixel(0,0,0) for i in range( self.n ) ]
            for j in range(self.m) ]
    # method that should be overridden
    ## update_pixel_arr: change the pixel array when called
    def update_pixel_arr(self):
        # update and change the pixel array
        self.pixel_arr = [ [Pixel(0,0,0) for i in range( self.n ) ]
            for j in range(self.m) ]
    # update inputs based on dictionary values
    def set_inputs(self, config_dict):
        for key in config_dict:
            attribute2check = key.lower()
            if hasattr(self, attribute2check):
                print('I found key:', key, 'setting to', config_dict[key] )
                setattr( self, attribute2check, config_dict[key])
            else:
                print('Unrecognized key', key)
    def reset_pixel_array(self):
        # reset pixel array just in case:
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
    def __init__(self, config_dict ):
        PanelPattern.__init__( self, {} )
        # reset inputs based on config
        self.set_inputs( config_dict )
        self.reset_pixel_array()

# worm pattern
class WormPattern(PanelPattern):
    def __init__(self, config_dict):
        PanelPattern.__init__( self, {} )
        self.type = 'worm';
        self.increment = 6
        self.lastr = 0
        self.lastg = 125
        self.lastb = 252
        self.multr = 1
        self.multb = .5
        self.multg = .75
        self.max_val = 236
        self.min_val = 20
        # reset inputs based on config
        self.set_inputs( config_dict )
        self.reset_pixel_array()

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

        if self.lastr > self.max_val :
            self.lastr =self.max_val
            self.multr *= -1
        if self.lastr <self.min_val:
            self.lastr =self.min_val
            self.multr *= -1
        if self.lastb >self.max_val :
            self.lastb =self.max_val
            self.multb *= -1
        if self.lastb <self.min_val:
            self.lastb =self.min_val
            self.multb *= -1
        if self.lastg >self.max_val :
            self.lastg =self.max_val
            self.multg *= -1
        if self.lastg <self.min_val:
            self.lastg =self.min_val
            self.multg *= -1
        #move through each row
        for i in range( int ( self.m / 2 )  ):
            self.fill_rect_edge( i)

class TestPattern(PanelPattern):
    def __init__(self, config_dict):
        PanelPattern.__init__( self, {} )
        self.type = 'test';
        self.increment = 6
        self.lastr = 0
        self.lastg = 125
        self.lastb = 252
        self.multr = 1
        self.multb = .5
        self.multg = .75
        # reset inputs based on config
        self.set_inputs( config_dict )
        self.reset_pixel_array()

    #this is an example application that loads some pixels
    #into the panel for display
    def update_pixel_arr(self):
        #move through each row
        for i in range( self.m):
            #move through the column
            for j in range( self.n ):
                self.pixel_arr[i][j] = Pixel( i*(220/self.m) , j*(220/self.n) , i+j)
