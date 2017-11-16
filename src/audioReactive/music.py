from __future__ import print_function
from __future__ import division
import time
import sys
import numpy as np
from numpy import *
from scipy.ndimage.filters import gaussian_filter1d
import config

class ExpFilter:
    """Temporal exponential smoothing filter
    """
    def __init__(self, val=0.0, alpha_decay=0.5, alpha_rise=0.5):
        """Small rise / decay factors = more smoothing"""
        self.alpha_decay = alpha_decay
        self.alpha_rise = alpha_rise
        self.value = val
    def update(self, value):
        if isinstance(self.value, (list, np.ndarray, tuple)):
            alpha = value - self.value
            alpha[alpha > 0.0] = self.alpha_rise
            alpha[alpha <= 0.0] = self.alpha_decay
        else:
            alpha = self.alpha_rise if value > self.value else self.alpha_decay
        self.value = alpha * value + (1.0 - alpha) * self.value
            
            
def getNotesToKeyMatrix(noteList, keyPattern=[0,2,4,5,7,9,11], weights=[2.,1.,1.,1.,3.,1.,1.]):
    matrix = np.zeros([12, len(noteList)])
    for i in range(12):
        for note in noteList:
            scaleDegree = ((note-i%12)%12)-1
            if scaleDegree in keyPattern:
                arg = np.argmin(np.abs(keyPattern-scaleDegree))
                matrix[i,note-noteList[0]] = weights[arg]
            else:
                matrix[i,note-noteList[0]] = 0.0
    print(matrix)
    return matrix    
    
    
class Key:
    def __init__(self, matrix, alpha=0.0005):
        self.keySums = ExpFilter(np.ones(12), alpha_rise=alpha, alpha_decay=alpha)
        self.matrix = matrix
        self.keyStringList = ['c  ', 'cs ', 'd  ', 'ef ',
                              'e  ', 'f  ', 'fs ', 'g  ',
                              'af ', 'a  ', 'bf ', 'b  ' ]
        self.currentKeyNum = 0
    def update(self, newNoteSpectrum):
        newKeySums = np.dot(self.matrix, newNoteSpectrum)
        self.keySums.update(newKeySums)
        self.currentKeyNum = np.argmax(self.keySums.value)
    def printKey(self):
        sortedValues = np.sort(self.keySums.value)
        sortedNames = list(self.keyStringList[i] for i in np.argsort(self.keySums.value))
        surety = np.round(100 * (sortedValues[-1]/sortedValues[-2] - 1.),1)
        print("most likely key is: " + self.keyStringList[self.currentKeyNum] + " " + str(surety) + "%")
        print(np.fliplr([sortedNames])[0][0:8])
        print(np.round(np.fliplr([sortedValues])[0],0)[0:8])
        
        
class NoteSums:
    def __init__(self, matrix, alpha=0.0005):
        self.noteSums = ExpFilter(np.ones(12), alpha_rise=alpha, alpha_decay=alpha)
        self.matrix = matrix
        self.noteStringList = ['c  ', 'cs ', 'd  ', 'ef ',
                              'e  ', 'f  ', 'fs ', 'g  ',
                              'af ', 'a  ', 'bf ', 'b  ' ]
    def update(self, newNoteSpectrum):
        newNoteSums = np.dot(self.matrix, newNoteSpectrum)
        self.noteSums.update(newNoteSums)
    def printNoteSums(self):
        print("most used notes are: ")
        sortedValues = np.sort(self.noteSums.value)
        sortedNames = list(self.noteStringList[i] for i in np.argsort(self.noteSums.value))
        print(np.fliplr([sortedNames])[0][0:8])
        print(np.round(np.fliplr([sortedValues])[0],0)[0:8])
        
         
class Chord:
    def __init__(self, noteList, alpha=0.05):
        # define the 7 x notes matrix for each of 12 possible keys.
        # 0 2 4 5 7 9 11   
        chordRefMatrix = np.array([[0,4,7], [2,5,9], [4,7,11], [5,9,0], [7,11,2], [9,0,4], [11,2,5]])
        weights        = np.array([[1,1,1], [1,1,1], [1,1,1], [1,1,1], [1,1,1], [1,1,1], [1,1,1]])
        self.chordMatrixList = []
        for i in range(12):
            self.chordMatrixList.append(np.zeros([7,len(noteList)]))
        for keyNum in range(12):
            for chordNum in range(7):
                for note in noteList:
                    scaleDegree = (note-keyNum%12)%12 -1 
                    if scaleDegree in chordRefMatrix[chordNum]:
                        arg = np.argmin(np.abs(chordRefMatrix[chordNum]-scaleDegree))
                        matrix[i,note-noteList[0]] = weights[arg]
                        self.chordMatrixList[keyNum][chordNum, note-noteList[0]] = weights[chordNum, arg]
                    else:
                        self.chordMatrixList[keyNum][chordNum, note-noteList[0]] = 0.0
        self.chordSums = ExpFilter(np.zeros(7), alpha_rise=alpha, alpha_decay=alpha)
        self.chordStringList = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii']
        self.currentChordNum = 0
    def update(self, newNoteSpectrum, currentKeyNum):
        newChordSums = np.dot(self.chordMatrixList[currentKeyNum], newNoteSpectrum)
        self.chordSums.update(newChordSums)
        self.currentChordNum = np.argmax(self.chordSums.value)
    def printChord(self):
        print("most likely chord is " + self.chordStringList[self.currentChordNum])
        print(np.round(self.chordSums.value,0))
            

class Beat:
    def __init__(self, freqs, freqMin=2, freqMax=60):
        self.matrix = np.zeros_like(freqs)
        for i in range(len(freqs)):
            if freqMin < freqs[i] < freqMax:
                self.matrix[i] = 1.0
            else:
                self.matrix[i] = 0.0                   
        self.bassPower = np.zeros(5)
    def update(self, freqSpectrum):
        self.bassPower = np.roll(self.bassPower, -1)
        self.bassPower[4] = np.dot(self.matrix, freqSpectrum)
    def beatRightNow(self):
        if (self.bassPower[2]*1.2 < self.bassPower[3] and
            self.bassPower[3]*1.2 < self.bassPower[4]):
            return True 
        else:
            return False
        
        
