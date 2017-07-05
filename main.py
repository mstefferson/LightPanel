#!/usr/bin/python

from classes import *
import numpy as np

if __name__ == "__main__":

    # Test pixel
    pix = Pixel(3, 4, 5 )
    print( pix )
    print( pix.r, pix.b, pix.g )
    print( pix.array )
    pix.get_colors()

    # Test panel
    m = 5
    n = 5
    pix_num = m * n
    my_panel_shapes = [ [1 for c in range(n)] for r in range(m) ] 
    my_panel = Panel(m,n,pix_num,my_panel_shapes)
    print("Here is the shape:\n")
    my_panel.get_shape()
    print("Here is the map:\n")
    my_panel.get_map()
    print("Here is the pixel display")
    my_panel.get_display()

