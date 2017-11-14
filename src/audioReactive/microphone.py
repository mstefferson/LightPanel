# sets up an audio stream from the microphone
import time
import numpy as np
import pyaudio
import audioConfig

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
def getFreqsToMelMatrix(freqs, dMel=1):
    # lowest note we have data for
    melMin = np.ceil(hertzToMel(freqs[1]))
    # highest note we have data for
    melMax = np.floor(hertzToMel(freqs[-1]))
    nFreqs = len(freqs)
    nMels = (melMax-melMin+1)/dMel
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
    return freqsToMelMatrix


###############################################################################
# Stream class
###############################################################################
'''
Creates a stream object according to the parameters in audioConfig.  
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
class Stream():
    def __init__(self, nBuffers=4):
        '''
        The mic samples at MIC_RATE, defined in audioConfig.  Usually 44100hz.
        The amount of samples each time we read data from the mic is then 
        MIC_RATE / FPS.  In order to sample frequencies of order FPS and lower,
        we need to take the spectrum of multiple buffers (hence nBuffers).
        '''
        print('initiating stream object')
        self.frameCount = 0
        self.nBuffers = nBuffers
        self.overflows = 0
        # array of zeros that will hold the rolling buffers
        self.micData = np.zeros(self.framesPerBuffer*self.nBuffers, dtype=np.float32)
        self.nSamples = len(self.micData)
        # set up audio stream
        self.p = pyaudio.PyAudio()
        self.framesPerBuffer = int(audioConfig.MIC_RATE / audioConfig.FPS)
        self.stream = self.p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=audioConfig.MIC_RATE,
                        input=True,
                        frames_per_buffer=self.framesPerBuffer)
        # set parameters for taking spectra later
        # Pad the sample with zeros until n = 2^i where i is an integer
        self.nZeros = 2**int(np.ceil(np.log2(self.nSamples))) - self.nSamples
        self.nSamplesPadded = self.nSamples + self.nZeros
        micData_padded = np.pad(self.micData, (0, nZeros), mode='constant')
        # Get the frequencies corresponding to the FFT we will take later.
        self.freqs = np.fft.fftfreq(self.nSamplesPadded, d=1./audioConfig.MIC_RATE)[0:self.nSamplesPadded//2]
        # Define an array to hold the current spectrum in freq space
        self.freqSpectrum = np.zeros_like(self.freqs)
        # Define matrix to convert freq spectrum to note spectrum. 
        self.freqsToMelMatrix = getFreqsToMelMatrix(self.freqs)
        # Define an array to hold the current spectrum in note space
        self.noteSpectrum = np.zeros(self.freqsToMelMatrix.shape[0])
        print('stream object initiated')
        
    def stopStream(self):
        # Not sure this needs to exist but it was in the previous repo
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        
    def readNewData(self):
        '''
        Updates micData by rolling the current array to the left and inserting
        the new sample at the right.  Or just overwriting completely in the case
        of nBuffers=1.  Returns True if reading the stream suceeded, False if 
        it failed.
        '''
        try:
            self.newMicData = np.fromstring(self.stream.read(self.framesPerBuffer), dtype=np.int16)
            self.newMicData = self.newMicData.astype(np.float32)
            self.micData = np.roll(self.micData, -self.framesPerBuffer)
            self.micData[(self.nBuffers-1)*self.framesPerBuffer:(self.nBuffers)*self.framesPerBuffer] = self.newMicData
            print('successfully got data from audio stream')
            self.frameCount += 1
            return True
        except IOError:
            print('failed to get data from audio stream')
            self.overflows += 1
            return False
        
    def calcFreqSpectrum(self):
        '''
        Calculates a spectrum in frequency space from the current micData.
        Returns nothing, just saves ths spectrum to the object.
        '''
        micData_padded = np.pad(self.micData, (0, self.nZeros), mode='constant')
        self.freqSpectrum = np.abs(np.fft.rfft(micData_padded)[0:self.nSamplesPadded//2])    
  
    def calcNoteSpectrum(self):
        '''
        Converts the current frequency-space specturm to note-space.
        Returns nothing, just saves the spectrum to the object.
        '''
        self.noteSpectrum = np.dot(self.freqsToMelMatrix, self.freqSpectrum)
        
    def readAndCalc(self):
        '''
        Most visualizers will probably just call this once per loop.  It reads
        new data from the mic and calculates the specta.
        '''
        self.readNewData()
        self.calcFreqSpectrum()
        self.calcNoteSpectrum()
    
    
    
    
    
    
    
    
    
    
