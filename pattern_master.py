from __future__ import print_function
import sys
sys.path.insert(0, './patterns')
from panel_patterns_starter import *
from classes import Panel

def run_visualizer(name, test_panel):
    if name == 'test':
        test_panel.simple_pixels()
    elif name == 'worm':
        test_panel.simple_rectangles_animated()
    else :
        print('NO VALID VISUALIZER GIVEN, USING DEFAULT')
        test_panel.simple_pixels()

if __name__ == '__main__':
    print('running panel_master')

    script = sys.argv[1]
    print('running script: ', script)

    run_type = sys.argv[2]
    if run_type != "pi":
        run_type = "vis"
    print('run_typ is: ', run_type)
    m = 5
    n = 6
    pix_num = m * n
    my_panel_shapes = [ [1 for c in range(n)] for r in range(m) ]
    my_panel = Panel(m,n,pix_num,my_panel_shapes)

    if run_type == "vis":
        panel = PanelVisualizer(10,10)
        test_panel = TestPanels(panel)
        run_visualizer(script, test_panel)
        panel.wait_for_exit();
