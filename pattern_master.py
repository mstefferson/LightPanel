from __future__ import print_function
import sys
sys.path.insert(0, './patterns')
from panel_patterns_starter import *
from classes import Panel


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
NUM_ROWS = 5
NUM_COLUMNS = 6

def get_visualizer_panel(name, test_panel):
    if name == 'test':
        return test_panel.simple_pixels()
    elif name == 'worm':
        return test_panel.simple_rectangles()
    else :
        print('NO VALID VISUALIZER GIVEN, USING DEFAULT')
        return test_panel.simple_pixels()


if __name__ == '__main__':
    print('running panel_master')

    script = sys.argv[1]
    print('running script: ', script)

    run_type = sys.argv[2]
    if run_type != "pi":
        run_type = "vis"
    else:
		#need to perform the import in here since we only do it if using the pi hardware
		from neopixel import *
		LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
		strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
		strip.begin()
    print('run_typ is: ', run_type)
    m = NUM_ROWS
    n = NUM_COLUMNS
    pix_num = m * n
    my_panel_shapes = [ [1 for c in range(n)] for r in range(m) ]
    my_panel = Panel(m,n,pix_num,my_panel_shapes, run_type)

    test_panel = TestPanels( my_panel )

    if run_type == "vis":
        while True:
            pixel_arr =  get_visualizer_panel(script, test_panel)

            my_panel.update_vis_panel(pixel_arr)
            time.sleep(.1)
            # my_panel.visualizer.wait_for_exit();
    else :
        while True:
            pixel_arr =  get_visualizer_panel(script, test_panel)
            # print("A")
            my_panel.update_panel(pixel_arr)
            # print("b")
            my_panel.update_led_panel(strip)
            # print("Here is the pixel display:")
            # my_panel.print_display()
            time.sleep(.1)
