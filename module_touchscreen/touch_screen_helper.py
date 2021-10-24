# Imports
import os
os.environ["DISPLAY"]=":0"

from pynput.mouse import Listener

import threading
import logging
logging.basicConfig(filename="module_touchscreen/mouse_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')


class TouchScreenHelper():
    def __init__(self, experiment, display_type):
        self.current_exp = experiment
        self.display_type = display_type
        thread = threading.Thread(target=self.start_listening, args=())
        thread.start()
        return

    def start_listening(self):
        with Listener(on_move=self.on_move) as listener:
            listener.join()

    def on_move(self, x, y):
        self.current_exp.on_click()
        logging.info("Mouse moved to ({0}, {1})".format(x, y))
    
