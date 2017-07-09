# import things you need
import numpy as np
import time
# from neopixel import *

# Pixel object. Contains pixel colors 
class Pixel():

    # constuctor sets r,g,b colors
    def __init__(self, r, g, b):
        # use mod to make sure pixel val = [0,255]
        max_val = 255
        # set values
        self.r = int(  r %  max_val  )
        self.b = int(  b %  max_val  )
        self.g = int(  g %  max_val  )
        self.array = [self.r,self.b,self.g]

    # allows for print( Pixel ) to just 
    # def __str__(self):
        # l = ['r','g','b']
        # return str( [ i for i in zip(l, self.array) ] )
        
    def print_colors(self):
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
        # only keep map if not equal to -1
        pixel_map_stream = [ self.pmap[r][c] for r in range(self.m) for c in range(self.n) if self.pmap[r][c] != -1 ]
        # set field
        self.pmap_stream = pixel_map_stream

    def set_display_stream( self ):
        # reshape stream
        temp_stream = [ self.pdisplay[r][c] for r in range(self.m) for c in range(self.n) ]
        # only put it in stream if it belongs (pmap != 1)
        pixel_stream = [ pix for i,pix in enumerate(temp_stream) if self.pmap_stream[i] != -1 ]
        # set field 
        self.pdisplay_stream = pixel_stream

    def set_new_stream( self, new_display ):
        # make sure the size is correct
        if len( new_display ) == self.m and len( new_display[0] ) == self.n:
            # get diff
            diff_update  = [ [1 if new_display[r][c].array != self.pdisplay[r][c].array and self.pmap[r][c] != -1 else 0 for c in range(self.n)] for r in range(self.m) ]

           # try to only keep the difference 
            temp_stream = [ new_display[r][c] for r in range(self.m) for c in range(self.n) if diff_update[r][c] == 1 ]
            temp_map = [ self.pmap[r][c] for r in range(self.m)  for c in range(self.n)  if diff_update[r][c] == 1 ]
            # update stream
            self.pdisplay_stream = temp_stream
            self.pmap_stream = temp_map
        else:
            print('Error: invalid size')

    def update_panel( self, new_display ):
        # update streams
        self.set_new_stream( new_display )
        # update display
        self.set_display( new_display )

    def update_led_panel( self, strip ):
        # update led panel based on pixel stream
        for ii in range( self.num_pixels ):
            # check if you can just use pixel.array works!
            strip.setPixelColor( self.pmap_stream[i], self.pdisplay_stream[i].r, self.pdisplay_stream[i].b, self.pdisplay_stream[i].r )

    # get shapes and maps
    def print_stream( self, gen, len_obj ):
        # loop through and print
        for ix,x in enumerate(gen):
            if ix < len_obj-1: 
                print(x,end=', ')
            else:
                print(x,end='\n')
    def print_panel( self, gen_gen ):
        # interate through generator of generators
        for ir,gen in enumerate(gen_gen):
            for ic,x in enumerate(gen):
                if ic < self.n-1:
                    print( x, end=', ' )
                else:
                    print( x, end='  \n' )

    def print_shape( self ):
        # grab generator of generators
        shape_gen_gen = ( (val for val in i) for i in self.pshape )
        # print it
        self.print_panel( shape_gen_gen );

    def print_map( self ):
        # grab generator of generators
        map_gen_gen = ( (map_val for map_val in i) for i in self.pmap )
        # print it
        self.print_panel( map_gen_gen );

    def print_display( self ):
        # grab generator of generators
        pix_gen_gen = ( (pixel.array for pixel in i) for i in self.pdisplay )
        # print it
        self.print_panel( pix_gen_gen );

    def print_display_stream( self ):
        # create generator
        pix_gen = ( jj.array for jj in self.pdisplay_stream );
        # print it
        self.print_stream( pix_gen, len(self.pdisplay_stream) )

    def print_map_stream( self ):
        # create generator
        map_gen = ( jj for jj in self.pmap_stream );
        # print it
        self.print_stream( map_gen, len(self.pmap_stream) )

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
        self.set_display_stream()
        

