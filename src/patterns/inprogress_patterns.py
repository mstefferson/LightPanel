# functioning_patterns
#
import sys
from classes import Pixel
from functioning_patterns  import PanelPattern
sys.path.insert(0, '../audioReactive/')
import microphone
#import music

# randwalk pattern
class RandwalkPattern(PanelPattern):
    def __init__(self, m, n, numwalkers):
        PanelPattern.__init__( self, m, n )
        self.call_name = 'randwalk';

# audioReactive test pattern
class AudioReactiveTestPattern(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__(self, m, n)
        self.call_name = 'arTest';
        self.frame_sleep_time = 0.0
    def update_pixel_arr(self):
        # update and change the pixel array
        self.pixel_arr = [ [Pixel(30,0,0) for i in range( self.n ) ] for j in range(self.m) ]
        
