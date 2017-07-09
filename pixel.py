# import things you need
from __future__ import print_function

# neopixel's Color
def Color(red, green, blue, white = 0):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	return (white << 24) | (red << 16)| (green << 8) | blue

# Pixel object. Contains pixel colors
class Pixel():

    # constuctor sets r,g,b colors
    def __init__(self, r, g, b):
        # use mod to make sure pixel val = [0,255]
        max_val = 256
        # set values
        self.r = int(  r %  max_val  )
        self.b = int(  b %  max_val  )
        self.g = int(  g %  max_val  )
        self.array = [self.r,self.b,self.g]

    def print_colors(self):
        print( self.array )
