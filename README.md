In order to use this, we call pattern_master.py. Here are some example usages :

Call the basic worm pattern on the visualizer : python pattern_master.py worm vis
Call the basic worm pattern on the Hardware panel : python pattern_master.py worm pi

Pattern options as of now are :
test
worm

If you want to add patterns, create a new .py file that creates your pattern
put it in the patterns folder, and add them to pattern_master.py's lookup scheme



to set up the raspi in case we mysteriously lose everything again:
Need to pull down our repo from https://github.com/mstefferson/LightPanel.git
Follow these adafruit instructions :  https://learn.adafruit.com/neopixels-on-raspberry-pi/software

Once that is working, to set up the raspi to execute a panel on startup we need to edit the basrc file to run our startup script.
open bashrc file:
nano ~/.bashrc
add to bashrc file at the last line :
source projects/LightPanel/panel_startup_script.sh

Here are instructions : https://www.raspberrypi.org/forums/viewtopic.php?t=59960
