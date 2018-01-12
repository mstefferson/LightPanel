from __future__ import print_function
import sys
sys.path.insert(0, './src')
sys.path.insert(0, './src/patterns')
from functioning_patterns import *
from inprogress_patterns import *
from classes import Panel
import time
import json

# Sample call:
# Using PI, you need sudo
# sudo python3 pattern_master.py myconf.json
#
# Using visualizer,
# python3 pattern_master.py myconf.json
# 
# Additional functions:
# get_active_pattern( pattern )
# this is out lookup table that checks the run time input args 
# and calls the appropriate pattern generator at the core of it, 
# this function just calls another pattern function, which 
# returns a pixel array object
def get_active_pattern( pattern ):
    if pattern["TYPE"] == 'test':
        active_pattern = TestPattern( my_panel.m , my_panel.n )
    elif pattern["TYPE"] == 'example':
        active_pattern = ExamplePattern( my_panel.m , my_panel.n )
    elif pattern["TYPE"] == 'worm':
        active_pattern = WormPattern( my_panel.m , my_panel.n )
    else :
        print('NO VALID VISUALIZER GIVEN, USING DEFAULT')
        active_pattern = TestPattern( my_panel.m , my_panel.n )
    return active_pattern

# Main
if __name__ == '__main__':
    print('running panel_master')
    # get json config file
    myconfig_file = sys.argv[1]
    print('using config file', myconfig_file)
    with open(myconfig_file) as json_data_file:
        pattern_input = json.load(json_data_file)
    # print some things
    mypanel_input = pattern_input["panel_config"]
    print('running config:', myconfig_file)
    run_type = mypanel_input["RUN_TYPE"]
    print('run_typ is:', run_type)
    m = mypanel_input["NUM_ROWS"]
    n = mypanel_input["NUM_COLUMNS"]
    pix_num = m * n
    if run_type == "vis":
        print("Nothing to set-up, using visualizer")
        from panel_visualizer import PanelVisualizer
        visualizer = PanelVisualizer(m, n)
    else:
        # need to perform the import in here since we only do it 
        # if using the pi hardware
        from neopixel import *
        LED_STRIP = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
        LED_COUNT = mypanel_input["NUM_COLUMNS"] * mypanel_input["NUM_ROWS"]
        strip = Adafruit_NeoPixel(LED_COUNT, mypanel_input["LED_PIN"],
                mypanel_input["LED_FREQ_HZ"], mypanel_input["LED_DMA"],
                mypanel_input["LED_INVERT"], mypanel_input["LED_BRIGHTNESS"],
                mypanel_input["LED_CHANNEL"], mypanel_input["LED_STRIP"])
        strip.begin()
    my_panel_shapes = [ [1 for c in range(n)] for r in range(m) ]
    print('Panel . M : ', len( my_panel_shapes ), " N: ",len( my_panel_shapes[0] ))
    my_panel = Panel(m,n,pix_num,my_panel_shapes, run_type)
    # initialize pattern
    active_pattern = get_active_pattern( pattern_input["pattern"] )
    #run a loop forever that just gets new pixel arrays and visualizes them
    while True:
        # update and get pixel array
        pixel_arr = active_pattern.update_and_get_pixel_arr()
        if run_type == "vis":
            #send our array over to the visualizer for the GUI
            visualizer.display_visualizer_panel(pixel_arr)
            #this is the refresh speed of our panel.
        else:
            #update the panel object's state
            my_panel.update_panel(pixel_arr)
            #update the actual LEDs
            my_panel.update_led_panel(strip)
        # refresh speed of our panel. We should be able to make this
        # pretty fast for the raspi
        time.sleep(active_pattern.frame_sleep_time)
