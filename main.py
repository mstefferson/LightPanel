#!/usr/bin/python

from classes import *
import numpy as np

if __name__ == "__main__":

    # Test pixel
    pix = Pixel(3, 4, 5 )
    print( 'Pixel: ', pix )
    print( 'Test print' )
    pix.print_colors()

    # Test panel
    m = 5
    n = 5
    pix_num = m * n
    my_panel_shapes = [ [1 for c in range(n)] for r in range(m) ] 
    my_panel = Panel(m,n,pix_num,my_panel_shapes)
    print("Here is the shape:")
    my_panel.print_shape()
    print("Here is the map:")
    my_panel.print_map()
    print("Here is the pixel display:")
    my_panel.print_display()
    print("Here is the pixel map stream:")
    my_panel.print_map_stream()
    print("Here is the pixel display stream:")
    my_panel.print_display_stream()

