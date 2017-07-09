from panel_visualizer import *

class TestPanels():

    def __init__(self , panel_):
        self.increment = 10
        self.lastr = 0
        self.lastg = 125
        self.lastb = 256
        self.multr = 1
        self.multb = .5
        self.multg = .75
        self.panel = panel_
        self.pixel_arr = [ [Pixel(0,0,0) for i in range( self.panel.numRows ) ] for j in range(self.panel.numColumns) ]

    #fills in a rectangle of a color into the pixel array given
    def fill_rect_edge( self, offset):
        tr = offset*self.increment*self.multr
        tg = offset*self.increment *self.multg
        tb = offset*self.increment*self.multb
        for j in range ( offset, len(self.pixel_arr[0]) -offset):
            for i in range ( offset, len(self.pixel_arr) -offset ):
                self.pixel_arr[i][j] = Pixel( self.lastr+tr , self.lastb+tb, self.lastg+tg)

    def simple_rectangles(self):
        print(self.lastr, end = "\n")
        self.lastr +=  self.increment*self.multr
        self.lastg += self.increment*self.multg
        self.lastb += self.increment*self.multb
        self.lastr %= 256
        self.lastb %= 256
        self.lastg %= 256
        #move through each row
        for i in range( int ( self.panel.numRows / 2 )  ):
            self.fill_rect_edge( i)
        self.panel.display_visualizer_panel(self.pixel_arr)

    def simple_rectangles_animated(self):
        while True:
            time.sleep(.1)
            self.simple_rectangles()

def main():
    panel = PanelVisualizer(10,10)
    pix = Pixel(10, 40, 50)
    test_panel = TestPanels(panel)

    # simple_pixels(panel)
    # test_panel.simple_rectangles()
    test_panel.simple_rectangles_animated();


main()
