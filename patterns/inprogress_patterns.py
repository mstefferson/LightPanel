# functioning_patterns
#
from classes import Pixel

# this is a template pattern all patterns are inherit
class PanelPattern():
    def __init__(self , m, n):
        self.call_name = 'panel';
        # row and columns
        self.m = m
        self.n = n
        self.pixel_arr = [ [Pixel(0,0,0) for i in range( self.n ) ] for j in range(self.m) ]

    def get_pixel_arr(self):
        #then return the pixel_array
        return self.pixel_arr

# randwalk pattern
class RandwalkPattern(PanelPattern):
    def __init__(self, m, n, numwalkers):
        PanelPattern.__init__( self, m, n )
        self.call_name = 'randwalk';

