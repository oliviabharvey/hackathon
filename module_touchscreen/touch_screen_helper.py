# Imports
import os
import random
os.environ["DISPLAY"]=":0"

from pynput.mouse import Listener

import threading
import logging
from utils.enums import *
from module_touchscreen.image_creator import ImageCreator

logging.basicConfig(filename="module_touchscreen/mouse_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

class TouchScreenHelper():
    def __init__(self, experiment, display_type):
        self.current_exp = experiment
        self.display_type = display_type
        self.touch_screen_enabled = False
        thread = threading.Thread(target=self.start_listening, args=())
        thread.start()

        self.imageCreator = ImageCreator()
        self.side = random.choice([Sides.LEFT, Sides.RIGHT])
        self.same_side_count = 0
        self.consecutive_good_clicks = 0
        self.consecutive_random_swaps = 0
        return

    def start_listening(self):
        with Listener(on_move=self.on_move) as listener:
            listener.join()

    def on_move(self, x, y):
        if  self.touch_screen_enabled:
            self.touch_screen_enabled = False
            self.click_type = self.check_click_type(x, y)
            self.current_exp.on_click(self.click_type)
            logging.info("Mouse moved to ({0}, {1})".format(x, y))

    def show_next_image(self):
        if self.display_type == DisplayPatterns.NONE:
            self.display_black_screen()
        elif self.display_type == DisplayPatterns.FIND_THE_SQUARE:
            self.display_find_the_square()
        elif self.display_type == DisplayPatterns.LEFT_OR_RIGHT or \
         self.display_type == DisplayPatterns.LEFT_OR_RIGHT_WITH_RANDOMNESS:
            self.display_left_or_right()
        
        self.touch_screen_enabled = True
    
    def display_black_screen(self):
        self.imageCreator.reset_canvas()

    def display_single_rectangle(self):
        if self.side == Sides.LEFT:
            self.imageCreator.show_left_rectangle()
        elif self.side == Sides.RIGHT:
            self.imageCreator.show_right_rectangle()

    def display_both_rectangle(self):
        self.imageCreator.show_left_and_right_rectangles()

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
        self.display_single_rectangle()

    def display_left_or_right(self):
        if self.consecutive_good_clicks >= 5:
            self.swap_side()
        self.display_both_rectangle()

    def swap_side(self):
        if self.side == Sides.LEFT:
            self.side = Sides.RIGHT
        else: 
            self.side = Sides.LEFT

    def check_click_type(self, x, y):
        good_collision = self.check_collision(x, y)
        if good_collision:
            self.consecutive_good_clicks += 1         

        else: 
            self.consecutive_good_clicks = 0

        if DisplayPatterns.LEFT_OR_RIGHT_WITH_RANDOMNESS and random.uniform(0, 1) <= 0.2:
            self.consecutive_random_swaps += 1
            if self.consecutive_random_swaps <= 2:
                if good_collision:
                    return ClickTypes.BAD
                else:
                    return ClickTypes.GOOD

        self.consecutive_random_swaps = 0
        if good_collision:
            return ClickTypes.GOOD
        else:
            return ClickTypes.BAD

    def check_collision(self, x, y):
        # to do Dan (use self.side)
        return True