# functioning_patterns
#
import sys
from classes import Pixel
import numpy as np
from functioning_patterns  import PanelPattern
sys.path.insert(0, '../audioReactive/')
import microphone
#import music


# audioReactive test pattern
class AudioReactiveTestPattern(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__(self, m, n)
        self.call_name = 'arTest';
        self.frame_sleep_time = 0.0
        self.pix_np = np.zeros([3,self.m,self.n])
        self.stream1 = microphone.Stream(fps=20,nBuffers=2)
        print(dir(self.stream1))
    def update_pixel_arr(self):
        # update and change the pixel array
        #print(dir(self.stream1))
        success = self.stream1.readAndCalc()
        if success:
            print(np.mean(self.stream1.noteSpectrum))
            self.pix_np[0,0,:] = self.stream1.noteSpectrum
            self.pixel_arr = [ [Pixel(self.pix_np[0,j,i],self.pix_np[1,j,i],self.pix_np[2,j,i]) for i in range(self.n) ] for j in range(self.m) ]
