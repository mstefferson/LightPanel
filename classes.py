# import things you need
import numpy as np

# Pixel object. Contains pixel colors 
class Pixel():
    
    # constuctor sets r,g,b colors
    def __init__(self, r, g, b):
        # use mod to make sure pixel val = [0,255]
        max_val = 255
        # set values
        self.r = int(  r %  max_val  )
        self.b = int(  g %  max_val  )
        self.g = int(  b %  max_val  )
        self.array = [self.r,self.b,self.g]
        
    def get_colors(self):
        print( self.array )

class Panel():

    # constuctor
    def __init__(self, m, n, num_pixels, panel_shape):
        # set basic internal variables
        self.m = m
        self.n = n
        self.num_pixels = num_pixels
        self.panel_shape = panel_shape
        
        def makeMapFromShape( self, panel_shape ):
            counter = 0;
            panel_map = -1 * np.ones( n, m ) 
            for ii in range(0, m):
                for jj in range(0,n):
                    # if row even, count upwards
                    if ii % 2:
                        if panel_shape[ ii, jj ] == 1:
                            panel[ii, n - 1 - jj] = counter
                            counter = counter + 1
                    else:
                        if panel_shape[ ii, n - 1 - jj ] == 1:
                            panel[ii, n - 1 - jj] = counter
                            counter = counter + 1
                            
            # print( "filled " + str( counter+1 ) + "LEDs. There should be " str( self.num_pixels ) )




