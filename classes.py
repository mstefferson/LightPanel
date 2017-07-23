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
    # contructor: 
    #   Pixel( int r, int g, int b )
    #
    # fields:
    #   r: red pixel value
    #   g: green pixel value
    #   b: blue pixel value
    #   array: [r,g,b]
    # 
    # methods:
    # print_colors(): prints the pixel array

    # constuctor
    def __init__(self, r, g, b):
        # use mod to make sure pixel val = [0,255]
        max_val = 256
        # set values
        self.r = int(  r %  max_val  )
        self.g = int(  g %  max_val  )
        self.b = int(  b %  max_val  )
        self.array = [self.r,self.g,self.b]

    # methods
    def print_colors(self):
        print( self.array )

class Panel():
    # contructor: 
    #   Panel( int m, int n, int num_pixels, list panel_shape )
    #
    # fields:
    #   m: number of rows in panel
    #   n: number of columns in panel
    #   num_pixel: number of pixels
    #   pshape: m x n list that gives the shape. 0 is no phys pixel. 1 is a phy pixel
    #   pdisplay: m x n list of pixel objects to be displayed
    #   pmap: m x n list that maps the shapes onto a pixel value. -1 is a null pixel
    #   pdisplay_update_stream: an single list of updated pixel values. This should be looped over to update the strand.
    #   pmap_update_stream: a single list of map values that tell which pixel should be updated. This should be looped over to update the strand.
    #
    # methods:
    #   __init__( int m, int n, int num_pixel, list panel_shape): constructor
    #   make_map_from_shape(): takes shape, find map from array to pixel #.
    #   set_display(): sets the display
    #   print_display(): print the display array
    #   print_display_stream(): print the display stream
    #   print_map(): creates generator of generators and prints the map. 
    #   print_map_stream(): creates generator and prints the map stream
    #   print_shape(): creates generator of generators and prints the panel shape.
    #   print_gen_gen(): takes generator of generator and prints values.
    #   print_gen(): takes generator and prints values
    #   set_display(new_display): takes in new display and updates self.pdisplay
    #   set_new_stream( new_display): updates self.pdisplay_update_stream and self.pmap_update_stream
    #   update_led_panel(): take updated panel info and sends it to the neo_pixel object
    #   update_panel(new_display): updates the panel and streams
    #   wipe_display(): wipes the display
    #   wipe_led_panel(): wips the neo_pixel object

    # make map from panel shape
    def make_map_from_shape( self ):
        # loop over indices
        counter = 0;
        panel_map = [ [-1 for c in range(self.n) ] for r in range(self.m)]
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

    # wipe the panel display
    def wipe_display( self ):
        # Set the display to zero
        panel_display = [ [Pixel(0,0,0) for c in range(self.n)] for r in range(self.m) ];
        self.pdisplay = panel_display

    # update the panel display from the input
    def set_display( self, new_display ):
        # check size
        num_rows = len( new_display )
        num_cols = len( new_display[0] )
        if ( num_rows != self.m ) or ( num_cols != self.n ):
            print( "size not the same. not resetting" )
        else:
            self.pdisplay = [ [ new_display[r][c] if self.pmap[r][c] != -1 else Pixel(0,0,0) for c in range(self.n) ] for r in range(self.m) ]

    # set self.pdisplay_update_stream and self.pmap_update_stream from input
    def set_new_stream( self, new_display ):
        # make sure the size is correct
        if len( new_display ) == self.m and len( new_display[0] ) == self.n:
            # get diff
            diff_update  = [ [1 if new_display[r][c].array != self.pdisplay[r][c].array and self.pmap[r][c] != -1 else 0 for c in range(self.n)] for r in range(self.m) ]

           # try to only keep the difference
            temp_stream = [ new_display[r][c] for r in range(self.m) for c in range(self.n) if diff_update[r][c] == 1 ]
            temp_map = [ self.pmap[r][c] for r in range(self.m)  for c in range(self.n)  if diff_update[r][c] == 1 ]
            # update stream
            self.pdisplay_update_stream = temp_stream
            self.pmap_update_stream = temp_map
        else:
            print('Error: invalid size')

    # update the panel display and streams
    def update_panel( self, new_display ):
        # update streams
        self.set_new_stream( new_display )
        # update display
        self.set_display( new_display )

    # wipe the panel
    def wipe_led_panel( self, strip ):
	# wipe it
        for i in range(self.num_pixels):
            strip.setPixelColor( i, Color(0,0,0) )
            strip.show()

    # update the neo_pixel object
    def update_led_panel( self, strip ):
        # update led panel based on pixel stream
        for i,pix in enumerate(self.pdisplay_update_stream):
            # check if you can just use pixel.array works!
            strip.setPixelColor( self.pmap_update_stream[i], Color( pix.r, pix.g, pix.b) )
        strip.show()

    # print a generator
    def print_gen( self, gen, len_obj ):
        # loop through and print
        for ix,x in enumerate(gen):
            if ix < len_obj-1:
                print(x,end=', ')
            else:
                print(x,end='\n')

    # print a generator of generators
    def print_gen_gen( self, gen_gen ):
        # interate through generator of generators
        for ir,gen in enumerate(gen_gen):
            for ic,x in enumerate(gen):
                if ic < self.n-1:
                    print( x, end=', ' )
                else:
                    print( x, end='  \n' )

    # print the shape
    def print_shape( self ):
        # grab generator of generators
        shape_gen_gen = ( (val for val in i) for i in self.pshape )
        # print it
        self.print_gen_gen( shape_gen_gen );

    # print the map
    def print_map( self ):
        # grab generator of generators
        map_gen_gen = ( (map_val for map_val in i) for i in self.pmap )
        # print it
        self.print_gen_gen( map_gen_gen );

    # print the display
    def print_display( self ):
        # grab generator of generators
        pix_gen_gen = ( (pixel.array for pixel in i) for i in self.pdisplay )
        # print it
        self.print_gen_gen( pix_gen_gen );

    # print the display stream
    def print_display_stream( self ):
        # create generator
        pix_gen = ( jj.array for jj in self.pdisplay_update_stream );
        # print it
        self.print_gen( pix_gen, len(self.pdisplay_update_stream) )

    # print the map stream
    def print_map_stream( self ):
        # create generator
        map_gen = ( jj for jj in self.pmap_update_stream );
        # print it
        self.print_gen( map_gen, len(self.pmap_update_stream) )

    # constuctor
    def __init__(self, m, n, num_pixels, panel_shape, panel_display = None):
        # set basic internal variables
        self.m = m
        self.n = n
        self.num_pixels = num_pixels
        print('rows ', self.m, 'cols ', self.n, 'num_pixs ', self.num_pixels )
        self.pshape = panel_shape
        # make the map. sets self.pmap
        self.make_map_from_shape()
        # wipe all pixels to start. sets self.pmap
        self.wipe_display()
        if panel_display is None:
            print('No initial panel')
            self.pmap_update_stream = [];
            self.pdisplay_update_stream = [];
        else:
            print('Initial panel')
            self.update_panel(panel_display)
            
