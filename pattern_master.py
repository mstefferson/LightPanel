from __future__ import print_function
import sys
sys.path.insert(0, './src')
sys.path.insert(0, './src/patterns')
from functioning_patterns import *
from inprogress_patterns import *
from classes import Panel
import time


# LED strip configuration:
# LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# panel configuration for the wooden panel I've made
NUM_ROWS = 13
NUM_COLUMNS = 34
#these are the configs for the cardboard test panel
#NUM_ROWS = 5
#NUM_COLUMNS = 6

# note: frame rate set in pattern classes

#run example: python3 pattern_master.py randwalk vis2

#this is out lookup table that checks the run time input args and calls the appropriate pattern generator
#at the core of it, this function just calls another pattern function, which returns a pixel array object
def get_active_pattern( name):
    if name == 'test':
        active_pattern = TestPattern( my_panel.m , my_panel.n )
    elif name == 'example':
        active_pattern = ExamplePattern( my_panel.m , my_panel.n )
    elif name == 'worm':
        active_pattern = WormPattern( my_panel.m , my_panel.n )
    elif name == 'randwalk':
        active_pattern = RandwalkPattern( my_panel.m , my_panel.n, 8 )
    else :
        print('NO VALID VISUALIZER GIVEN, USING DEFAULT')
        active_pattern = TestPattern( my_panel.m , my_panel.n )
    return active_pattern


if __name__ == '__main__':
    print('running panel_master')

    script = sys.argv[1]
    print('running script: ', script)

    run_type = sys.argv[2]
    m = NUM_ROWS
    n = NUM_COLUMNS
    pix_num = m * n
    if run_type != "pi":
        if run_type != "vis2":
            run_type = "vis"
    else:
        #need to perform the import in here since we only do it if using the pi hardware
        from neopixel import *
        LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
        strip = Adafruit_NeoPixel(pix_num, LED_PIN, LED_FREQ_HZ,
            LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        strip.begin()
    print('run_type is: ', run_type)
    my_panel_shapes = [ [1 for c in range(n)] for r in range(m) ]
    print('Panel . M : ', len( my_panel_shapes ), " N: ",len( my_panel_shapes[0] ))
    my_panel = Panel(m,n,pix_num,my_panel_shapes, run_type)
    # initialize pattern
    active_pattern = get_active_pattern( script )

    if run_type == "vis":
        from panel_visualizer import PanelVisualizer
        visualizer = PanelVisualizer(m, n, False)
    if run_type == "vis2":
        from panel_visualizer import PanelVisualizer
        visualizer = PanelVisualizer(m, n, True)
    #run a loop forever that just gets new pixel arrays and visualizes them
    while True:
        # update and get pixel array
        pixel_arr = active_pattern.update_and_get_pixel_arr()
        if run_type == "vis" or run_type=="vis2":
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
