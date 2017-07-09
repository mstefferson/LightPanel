from __future__ import print_function
#!/usr/bin/python
from classes import Pixel, Panel

if __name__ == "__main__":

    # Test pixel
    pix = Pixel(3, 4, 5 )
    print( 'Pixel: ', pix )
    print( 'Test print' )
    pix.print_colors()

    # Test panel
    m = 5
    n = 6
    pix_num = m * n
    my_panel_shapes = [ [1 for c in range(n)] for r in range(m) ]
    print( len(my_panel_shapes) )
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
    # set a red panel
    print('red')
    new_panel = [ [ Pixel(255,0,0)  if j % 2 == 0 else Pixel(0,0,0) for j in range(n) ] for i in range(m) ]
    my_panel.update_panel(new_panel)
    print("Here is the new display:")
    my_panel.print_display()
    print("Here is the new map stream:")
    my_panel.print_map_stream()
    print("Here is the new display stream:")
    my_panel.print_display_stream()
    print("visualizing the stream:")
    my_panel.update_vis_panel()
    # set a green panel
    print('green')
    new_panel = [ [ Pixel(0,255,0)  if j % 2 != 0 else Pixel(0,0,0) for j in range(n) ] for i in range(m) ]
    my_panel.update_panel(new_panel)
    print("Here is the new display:")
    my_panel.print_display()
    print("Here is the new map stream:")
    my_panel.print_map_stream()
    print("Here is the new display stream:")
    my_panel.print_display_stream()
    #wait for someone to click on the visualizer to close it
    my_panel.visualizer.wait_for_exit()
