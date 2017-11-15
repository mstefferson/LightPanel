# functioning_patterns
#
import sys
from classes import Pixel
import numpy as np
from functioning_patterns  import PanelPattern
sys.path.insert(0, '../audioReactive/')
import micStream
#import music

# audioReactive test pattern
class AudioReactiveTestPattern(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__(self, m, n)
        self.call_name = 'arTest';
        self.frame_sleep_time = 0.0
        self.pix_np = np.zeros([3,self.m,self.n])
        self.stream = micStream.Stream(fps=24,nBuffers=4)
	print(self.stream.freqs[0:10])
        print(self.stream.freqs[-10:])
    def update_pixel_arr(self):
        # update and change the pixel array
        success = self.stream.readAndCalc()
        if success:
            print(np.mean(self.stream.noteSpectrum))
            self.pix_np[0,0,:] = self.stream.noteSpectrum
            self.pixel_arr = [ [Pixel(self.pix_np[0,j,i],self.pix_np[1,j,i],self.pix_np[2,j,i]) for i in range(self.n) ] for j in range(self.m) ]
