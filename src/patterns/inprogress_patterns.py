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

