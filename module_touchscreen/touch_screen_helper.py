# Imports
import os
import random
os.environ["DISPLAY"]=":0"

from pynput.mouse import Listener
import threading
import logging
from utils.enums import *

logging.basicConfig(filename="module_touchscreen/mouse_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

class TouchScreenHelper():
    def __init__(self, experiment, display_type):
        self.current_exp = experiment
        self.display_type = display_type
        thread = threading.Thread(target=self.start_listening, args=())
        thread.start()

        self.side = random.choice([Sides.LEFT, Sides.RIGHT])
        self.same_side_count = 0
        return

    def start_listening(self):
        with Listener(on_move=self.on_move) as listener:
            listener.join()

    def on_move(self, x, y):
        self.current_exp.on_click()
        logging.info("Mouse moved to ({0}, {1})".format(x, y))

    def show_next_image(self):
        if self.display_type == DisplayPatterns.NONE:
            self.display_black_screen()
        elif self.display_type == DisplayPatterns.FIND_THE_SQUARE:
            self.display_find_the_square()
        elif self.display_type == DisplayPatterns.LEFT_OR_RIGHT:
            self.display_left_or_right()
        elif self.display_type == DisplayPatterns.LEFT_OR_RIGHT_WITH_RANDOMNESS:
            self.display_left_or_right_with_randomness()

    
    def display_black_screen(self):
        # to do : dan
        return

    def display_find_the_square(self):
        if self.same_side_count >= 3: 
            self.swap_side()
            self.same_side_count = 1
        else: 
            swap = random.choice([True, False])
            if swap:  
                self.swap_side()
                self.same_side_count = 1
            else: 
                self.same_side_count += 1
        # to do : dan

    def display_left_or_right(self):
            
        return

    def display_left_or_right_with_randomness(self):
        return

    def swap_side(self):
        if self.side == Sides.LEFT:
            self.side = Sides.RIGHT
        else: 
            self.side = Sides.LEFT



    
