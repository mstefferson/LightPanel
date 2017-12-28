from __future__ import print_function
import sys
sys.path.insert(0, './src')
sys.path.insert(0, './src/patterns')
from functioning_patterns import *
from inprogress_patterns import *
from classes import Panel
import time
import json


# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# panel configuration
NUM_ROWS = 24
NUM_COLUMNS = 24
#these are the configs for the cardboard test panel
#NUM_ROWS = 5
#NUM_COLUMNS = 6

# note: frame rate set in pattern classes

#this is out lookup table that checks the run time input args and calls the appropriate pattern generator
#at the core of it, this function just calls another pattern function, which returns a pixel array object
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

if __name__ == '__main__':
    print('running panel_master')
    myconfig_file = sys.argv[1]
    with open(myconfig_file) as json_data_file:
        pattern_input = json.load(json_data_file)
    mypanel_input = pattern_input["panel_config"]
    print('running config: ', myconfig_file)
    run_type = mypanel_input["RUN_TYPE"]
    print('run_typ is: ', run_type)
    m = mypanel_input["NUM_ROWS"]
    n = mypanel_input["NUM_COLUMNS"]
    pix_num = m * n
    if run_type == "vis":
        print("Nothing to set-up, using visualizer") 
        from panel_visualizer import PanelVisualizer
        visualizer = PanelVisualizer(m, n)
    else:
        #need to perform the import in here since we only do it if using the pi hardware
        from neopixel import *
        LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
        strip = Adafruit_NeoPixel(mypanel_input["LED_COUNT"], mypanel_input["LED_PIN"],
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
