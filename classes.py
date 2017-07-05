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
    # contructor: Panel( int m, int n, int num_pixels, list panel_shape )
    # 
    # fields:
    #   m: number of rows in panel
    #   n: number of columns in panel
    #   pshape: m x n list that gives the shape. 0 is no phys pixel. 1 is a phy pixel
    #   pmap: m x n list that maps the shapes onto a pixel value. -1 is a null pixel
    #   pdisplay: m x n list of pixel objects to be displayed 
    #   pdisplay_stream 
    #   pmap_stream:
    #
    # methods:
    #   make_map_from_shape()
    #   wipe_display()
    #   set_display()
    #   init_pixel_stream()
    #   set_map_stream()
    #   set_display_stream()
    #   get_display()
    #   get_map()
    #   get_shape()
    #   get_map_stream():
    #   get_display_stream():
     
 # make map from panel shape
    def make_map_from_shape( self ):
        # loop over indices
        counter = 0;
        panel_map = [ [-1 for c in range(self.m) ] for r in range(self.n)]
        for ii in range(self.m):
            for jj in range(self.n):
                # if row even, count upwards
                if ii % 2 == 0:
                    if self.pshape[ ii ][ jj ] == 1:
                        panel_map[ii][jj] = counter
                        counter = counter + 1
                else:
                    if self.pshape[ ii ][ self.n - 1 - jj ] == 1:
                        panel_map[ ii ][ self.n - 1 - jj ] = counter
                        counter = counter + 1
        self.pmap = panel_map

    def wipe_display( self ):
        # Set the display to zero
        panel_display = [ [Pixel(0,0,0) for c in range(self.n)] for r in range(self.m) ];
        self.pdisplay = panel_display

    def set_display( self, new_display ):
        # check size
        num_rows = len( new_display )
        num_cols = len( new_display[0] )
        if ( num_rows != self.m ) or ( num_cols != self.n ):
            print( "size not the same. not resetting" )
        else:
            self.pdisplay = [ [ new_display[r][c] if self.pmap[r][c] != -1 else Pixel(0,0,0) for c in range(self.n) ] for r in range(self.m) ]

    def init_pixel_stream( self ):
        pixel_stream = [ Pixel(0,0,0) for i in range( self.num_pixels ) ]
        self.pdisplay_stream = pixel_stream

    def set_map_stream( self ):
        pixel_map_stream = [ self.pmap[r][c] if r % 2 == 0 else self.pmap[r][self.n -1 - c] for r in range(self.m) for c in range(self.n) ]
        # set field
        self.pmap_stream = pixel_map_stream

    def set_display_stream( self ):
        # reshape stream
        temp_stream = [ self.pdisplay[r][c] for r in range(self.m) for c in range(self.n) ]
        # only put it in stream if it belongs (pmap != 1)
        pixel_stream = [ pix for i,pix in enumerate(temp_stream) if self.pmap_stream[i] != -1 ]
        # set field 
        self.pdisplay_stream = pixel_stream

    # get shapes and maps
    def grab_pixel(self, some_object ):
        return( (pixel.array for pixel in some_object ) )

    def get_shape( self ):
        print( self.pshape )

    def get_map( self ):
        print( self.pmap )

    def get_display( self ):
        # print( [pix.r for pix in self.pdisplay ])
        temp = self.grab_pixel( self.pdisplay ) 
        print( ii for ii in temp )

    def get_map_stream( self ):
        print( [pix.array for pix in self.pmap_stream] )

    def get_display_stream( self ):
        print( [pix.array for pix in self.pdisplay_stream] )


    # constuctor
    def __init__(self, m, n, num_pixels, panel_shape):
        # set basic internal variables
        self.m = m
        self.n = n
        self.num_pixels = num_pixels
        self.pshape = panel_shape
        # make the map. sets self.pmap
        self.make_map_from_shape()
        # wipe all pixels to start. sets self.pmap
        self.wipe_display()
        self.set_map_stream()
        

