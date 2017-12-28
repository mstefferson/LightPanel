### Things to put in the config.json
#
# panel_config: this tells the code whether to use visualizer or pi. If
# using pi, set all of the LED strip parametershere
# pattern: this tells the code what pattern you want to use and what 
# the frame rate should be. Some patterns may have options parameteres
# to set. You'd put those here.
#
# an example can be found in src/configTmpl.json
#
## "panel_config" to always set
  "NUM_ROWS": 24, #int
  "NUM_COLUMNS": 24, #int
  "RUN_TYPE": "vis"/"pi" #str
## "pane_config" to set if using led strip
  # LED strip configuration:
  "LED_COUNT": 30 # int, Number of LED pixels.
  # GPIO pin connected to the pixels 
  # (18 uses PWM!), (10 uses SPI /dev/spidev0.0) 
  "LED_PIN": 18 # int
  "LED_FREQ_HZ": 800000 # int, LED signal frequency in hertz (usually 800khz)
  "LED_DMA": 5 # int, DMA channel to use for generating signal (try 5)
  "LED_BRIGHTNESS": 255 # int, Set to 0 for darkest and 255 for brightest
  # Invert LED flag (true/false in json)
  # True to invert the signal (when using NPN transistor level shift) 
  "LED_INVERT": false # bool, 
  "LED_CHANNEL": 0 # int, set to '1' for GPIOs 13, 19, 41, 45 or 53
## "pattern"
  "TYPE":"worm"/"test" # str
  "FRAME_SLEEP_TIME": 0.1 # float, frame rate

## example using Mike and Stephen's pi and strip
{
  "panel_config":
    "NUM_ROWS": 5,
    "NUM_COLUMNS": 6,
    "RUN_TYPE": "pi",
    "LED_PIN": 18,
    "LED_FREQ_HZ": 800000,
    "LED_DMA": 5,
    "LED_BRIGHTNESS": 255,
    "LED_INVERT": false,
    "LED_CHANNEL": 0
  },
  "pattern":{
      "TYPE":"worm",
      "FRAME_SLEEP_TIME":0.1
  }
}

## example using visualizer
{
  "panel_config":
    "NUM_ROWS": 24,
    "NUM_COLUMNS": 24,
    "RUN_TYPE": "vis",
  },
  "pattern":{
      "TYPE":"test",
      "FRAME_SLEEP_TIME":0.1
  }
}

