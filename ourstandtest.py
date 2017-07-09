#!/usr/bin/python
import time
from classes import *
import numpy as np
from neopixel import *

# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

# panel configuration
NUM_ROWS = 5
NUM_COLUMNS = 6

if __name__ == "__main__":
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    # initializing
    my_panel_shapes = [ [1 for c in range(NUM_COLUMNS)] for r in range(NUM_ROWS) ]
    print( 'rows', NUM_ROWS, 'col', NUM_COLUMNS, 'leds', LED_COUNT )
    my_panel = Panel(NUM_ROWS, NUM_COLUMNS, LED_COUNT, my_panel_shapes, "pi")
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
    print("Updating leds:")
    my_panel.update_led_panel(strip)

    print ('Press Ctrl-C to quit.')
    while True:
        # set a new panel
        new_panel = [ [ Pixel(255,0,0)  if j % 2 == 0 else Pixel(0,0,0) for j in range(NUM_COLUMNS) ] for i in range(NUM_ROWS) ]
        my_panel.update_panel( new_panel )
        print("Here is the new display:")
        my_panel.print_display()
        print("Here is the new map stream:")
        my_panel.print_map_stream()
        print("Here is the new display stream:")
        my_panel.print_display_stream()
        print("Updating leds:")
        my_panel.update_led_panel(strip)

        time.sleep( 1 )

        new_panel = [ [ Pixel(0,255,0)  if j % 2 != 0 else Pixel(0,0,0) for j in range(NUM_COLUMNS) ] for i in range(NUM_ROWS) ]
        my_panel.update_panel( new_panel )
        print("Here is the new display:")
        my_panel.print_display()
        print("Here is the new map stream:")
        my_panel.print_map_stream()
        print("Here is the new display stream:")
        my_panel.print_display_stream()
        print("Updating leds:")
        my_panel.update_led_panel(strip)
        time.sleep( 1 )
