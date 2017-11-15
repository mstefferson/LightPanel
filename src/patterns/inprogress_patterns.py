# functioning_patterns
#
import sys
from classes import Pixel
import numpy as np
from functioning_patterns  import PanelPattern
sys.path.insert(0, '../audioReactive/')
#import microphone
#import music




import time
import numpy as np
import pyaudio

MIC_RATE = 44100

###############################################################################
# convert frequencies to notes 
###############################################################################
'''
Mels are a non-linear unit of frequency.  However this isn't the standard mel
definition.  This is defined such that C0 = 1 mel and each half step above that
is +1 mel and A4 = 440 hz.  
'''
def hertzToMel(freq):
    return 12.0*(np.log(0.0323963*freq)/0.693147)+12.0
def melToHertz(mel):
    return 440.0 * (2.0**(1.0/12.0))**(mel-58.0)

'''
This matrix basically "re-bins" the spectrum from frequency space to "note" 
(or mel) space.  It has nNotes rows and nFreqs columns.  The equation is then
noteSpectrum = thisMatrix dot frequencySpectrum
The function to define this matrix was not coded with speed in mind and should
not be called every frame.  Define it once at the beginning. 
'''
def getFreqsToMelMatrix(freqs, dMel=1, melMin=37, melMax=96):
    nFreqs = len(freqs)
    nMels = int((melMax-melMin+1)/dMel)
    mels = np.arange(melMin, melMax+1, dMel)
    centerFreqs    = [melToHertz(mel)          for mel in mels]
    lowerEdgeFreqs = [melToHertz(mel-dMel/2.0) for mel in mels]
    upperEdgeFreqs = [melToHertz(mel+dMel/2.0) for mel in mels]
    freqsToMelMatrix = np.zeros([nMels, nFreqs])
    # matrix for a "square" filter for each note
    for i in range(nMels):
        for j in range(nFreqs):
            if lowerEdgeFreqs[i] < freqs[j] < upperEdgeFreqs[i]:
                freqsToMelMatrix[i,j] = 1.0
    # normalize
    for i in range(nMels):
        freqsToMelMatrix[i] /= np.sum(freqsToMelMatrix[i])  
    return freqsToMelMatrix


###############################################################################
# Stream class
###############################################################################
'''
Creates a stream object.  
Some functions here take a non-trivial amount of computing time, make sure
those are being called only once per loop.
Typical usage will be:
-- stream = microphone.Stream()
within loop:
-- stream.readAndCalculate()
-- use stream.micData, stream.freqSpectrum, and/or stream.noteSpectrum to 
calculate pixel values
-- update leds
'''

class Stream:
    def __init__(self, fps=24, nBuffers=2):
        '''
        The mic samples at MIC_RATE,  Usually 44100hz.
        The amount of samples each time we read data from the mic is then 
        MIC_RATE / fps.  In order to sample frequencies of order fps and lower,
        we need to take the spectrum of multiple buffers (hence nBuffers).
        '''
        print('initiating stream object')
        self.frameCount = 0
        self.nBuffers = nBuffers
        self.overflows = 0
        self.fps = fps
        self.framesPerBuffer = int(MIC_RATE / self.fps)
        # array of zeros that will hold the rolling buffers
        self.micData = np.zeros(self.framesPerBuffer*self.nBuffers, dtype=np.float32)
        self.nSamples = len(self.micData)
        # set up audio stream
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=MIC_RATE,
                                  input=True,
                                  frames_per_buffer=self.framesPerBuffer)
        # set parameters for taking spectra later
        # Pad the sample with zeros until n = 2^i where i is an integer
        self.nZeros = 2**int(np.ceil(np.log2(self.nSamples))) - self.nSamples
        self.nSamplesPadded = self.nSamples + self.nZeros
        micData_padded = np.pad(self.micData, (0, self.nZeros), mode='constant')
        # Get the frequencies corresponding to the FFT we will take later.
        self.freqs = np.fft.fftfreq(self.nSamplesPadded, d=1./MIC_RATE)[0:self.nSamplesPadded//2]
        # Define an array to hold the current spectrum in freq space
        self.freqSpectrum = np.zeros_like(self.freqs)
        # Define matrix to convert freq spectrum to note spectrum. 
        self.freqsToMelMatrix = getFreqsToMelMatrix(self.freqs)
        # Define an array to hold the current spectrum in note space
        self.noteSpectrum = np.zeros(self.freqsToMelMatrix.shape[0])
        print('stream object initiated')
    def readNewData(self):
        ''' Updates micData by rolling the current array to the left and inserting
        the new sample at the right.  Or just overwriting completely in the case
        of nBuffers=1.  
        The stream.read() command blocks until the buffer has the requested
        number of frames.
        Returns True if reading the stream suceeded, False if the buffer overflowed.
        '''
        try:
            self.newMicData = np.fromstring(self.stream.read(self.framesPerBuffer), dtype=np.int16)
            self.newMicData = self.newMicData.astype(np.float32)
            self.micData = np.roll(self.micData, -self.framesPerBuffer)
            self.micData[(self.nBuffers-1)*self.framesPerBuffer:(self.nBuffers)*self.framesPerBuffer] = self.newMicData
            print('successfully got data from audio stream')
            self.frameCount += 1
            returnVal=True
        except IOError:
            self.overflows += 1
            print('Audio buffer overflowed. This has happened '+str(self.overflows)+' times')
            print('Either decrease the defined fps value or speed up the code in your loop')
            returnVal=False
        return returnVal
    def stopStream(self):
        # Not sure this needs to exist but it was in the previous repo
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    def calcFreqSpectrum(self):
        ''' Calculates a spectrum in frequency space from the current micData.
        Returns nothing, just saves ths spectrum to the object.
        '''
        micData_padded = np.pad(self.micData, (0, self.nZeros), mode='constant')
        self.freqSpectrum = np.square(np.abs(np.fft.rfft(micData_padded)[0:self.nSamplesPadded//2])) * 1.e-10    
    def calcNoteSpectrum(self):
        ''' Converts the current frequency-space specturm to note-space.
        Returns nothing, just saves the spectrum to the object.
        '''
        self.noteSpectrum = np.dot(self.freqsToMelMatrix, self.freqSpectrum)
    def readAndCalc(self):
        ''' Most visualizers will probably just call this once per loop.  It reads
        new data from the mic and calculates the specta.
        '''
        success = self.readNewData()
        if success:
            self.calcFreqSpectrum()
            self.calcNoteSpectrum()
        return success








# audioReactive test pattern
class AudioReactiveTestPattern(PanelPattern):
    def __init__(self, m, n):
        PanelPattern.__init__(self, m, n)
        self.call_name = 'arTest';
        self.frame_sleep_time = 0.0
        self.pix_np = np.zeros([3,m,n])
        self.stream1 = Stream()
        print(dir(self.stream1))
    def update_pixel_arr(self):
        # update and change the pixel array
        print(dir(self.stream1))
        success = self.stream1.readAndCalc()
        if success:
            print(np.mean(self.stream1.noteSpectrum))
            self.pix_np[0,0,:] = self.stream1.noteSpectrum
            self.pixel_arr = [ [Pixel(self.pix_np[0,self.m,
n],self.pix_np[1,
m,
n],self.pix_np[2,
m,
n]) for i in range(self.n) ] for j in range(self.m) ]
