# Imports
from pynput.mouse import Listener
import logging

# Class
class TouchScreenHelper():

    def __init__(self):
 
        with Listener(on_move=on_move) as listener:
            listener.join()
    
    def on_move(x, y):
        logging.info("Mouse moved to ({0}, {1})".format(x, y))
        logging.basicConfig(filename="mouse_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

        


#Listener(on_move=on_move).join()
tchsnscreenhlpr = TouchScreenHelper().listener
