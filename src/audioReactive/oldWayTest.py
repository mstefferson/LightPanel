from __future__ import print_function
from __future__ import division

import sys
sys.path.insert(0, '../src')
import platform
import numpy as np
import time
import neopixel
import microphone

nLed = 60
LED_FREQ_HZ = 800000
LED_PIN = 12
LED_DMA = 5
BRIGHTNESS = 255
LED_INVERT = 0

# create strip object
strip = neopixel.Adafruit_NeoPixel(nLed, 
                                   LED_PIN,
                                   LED_FREQ_HZ,
                                   LED_DMA,
                                   LED_INVERT,
                                   BRIGHTNESS)
# initialize strip
strip.begin()
prevPixels = np.tile(253, (3, nLed))
pixels = np.tile(0, (3, nLed))
print(prevPixels.shape)
print(pixels.shape)

def update():
    global pixels, prevPixels
    # Truncate values and cast to integer
    pixels = np.clip(pixels, 0, 255).astype(int)
    p = np.copy(pixels)
    # Encode 24-bit LED values in 32 bit integers
    r = np.left_shift(p[0][:].astype(int), 8)
    g = np.left_shift(p[1][:].astype(int), 16)
    b = p[2][:].astype(int)
    rgb = np.bitwise_or(np.bitwise_or(r, g), b)
    # Update the pixels
    for i in range(nLed):
        # Ignore pixels if they haven't changed (saves bandwidth)
        if np.array_equal(p[:, i], prevPixels[:, i]):
            continue
        strip._led_data[i] = rgb[i]
    strip.show()

stream = microphone.Stream()
print('frequencies')
print(stream.freqs)
print('shape of freqsToMelMatrix')
print(stream.freqsToMelMatrix.shape)
print('first few lines of freqsToMelMatrix')
print(stream.freqsToMelMatrix[0,0:20])
print(stream.freqsToMelMatrix[1,0:20])
print(stream.freqsToMelMatrix[2,0:20])
while True:
    # reads new data from mic and saves it in object.  returns true on success or false on failure
    success = stream.readAndCalc()
    if success:
        print(stream.noteSpectrum[10])
        pixels[0,:] = stream.noteSpectrum[10] / 1.e4
        update()
           

