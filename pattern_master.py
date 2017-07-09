from __future__ import print_function
import sys
sys.path.insert(0, './patterns')
from panel_patterns_starter import *
from classes import Panel
from neopixel import *


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
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    print('run_typ is: ', run_type)
    m = 5
    n = 6
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
            my_panel.update_panel(pixel_arr)
            my_panel.update_led_panel(strip)
            # print("Here is the pixel display:")
            # my_panel.print_display()
            time.sleep(.1)
