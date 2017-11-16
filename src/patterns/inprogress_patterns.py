# functioning_patterns
#
import sys
from classes import Pixel
import numpy as np
import time
from functioning_patterns  import PanelPattern
sys.path.insert(0, '../audioReactive/')
import micStream
import music

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
        self.frameCount = 0
        self.frame_sleep_time = 0.0
        self.pix_np = np.zeros([3,self.m,self.n])
        self.stream = micStream.Stream(fps=60,nBuffers=6)
        self.t0 = time.time() 
        self.t1 = time.time()
        #print(self.stream.freqs[0:10])
        #print(self.stream.freqs[-10:])
    def update_pixel_arr(self):
        # update and change the pixel array
        success = self.stream.readAndCalc()
        if success:
            #print(np.mean(self.stream.noteSpectrum))
            self.pix_np[0,0,:] = self.stream.noteSpectrum
            self.pixel_arr = [ [Pixel(self.pix_np[0,j,i],self.pix_np[1,j,i],self.pix_np[2,j,i]) for i in range(self.n) ] for j in range(self.m) ]
            self.frameCount+=1
            if self.frameCount%100==0:
	        self.t1 = time.time()
	        print('fps last 100 frames: ' + str(100 / (self.t1 - self.t0)))
            self.t0 = self.t1
		
		
# audioReactive test pattern
class AudioReactiveTheoryDemo(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__(self, m, n)
        self.call_name = 'arTheoryDemo';
        self.frameCount = 0
        self.frame_sleep_time = 0.0
        self.pix_np = np.zeros([3,self.m,self.n])
        self.stream = micStream.Stream(fps=60,nBuffers=6)
        self.volume = music.ExpFilter(0.0, alpha_rise=0.8, alpha_decay=0.3)
        self.keyObj = music.Key(music.getNotesToKeyMatrix(self.stream.notes))
        self.chordObj = music.Chord(self.stream.notes)
    def update_pixel_arr(self):
        # update and change the pixel array
        success = self.stream.readAndCalc()
        if success:
	    self.volume.update(np.mean(self.stream.noteSpectrum))
	    self.keyObj.update(self.stream.noteSpectrum)
	    self.chordObj.update(self.stream.noteSpectrum, self.keyObj.currentKeyNum)
            if self.frameCount%10==0:
                print(self.volume.value)
                self.keyObj.printKey()
                self.chordObj.printChord()
            self.pix_np[:,:,:] = 0
            self.pix_np[0, 0, 0 :6 ] = 30
            self.pix_np[0, 0, 18:24] = 30
            self.pix_np[0, 0, 36:42] = 30
            self.pix_np[0, 0, 54:60] = 30
            self.pix_np[2, 0, 6+self.keyObj.currentKeyNum] = 100
            self.pix_np[2, 0, 24+self.chordObj.currentChordNum] = 100
            self.pixel_arr = [ [Pixel(self.pix_np[0,j,i],self.pix_np[1,j,i],self.pix_np[2,j,i]) for i in range(self.n) ] for j in range(self.m) ]
            self.frameCount+=1
 
