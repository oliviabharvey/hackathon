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
        self.touch_screen_enabled = False
        thread = threading.Thread(target=self.start_listening, args=())
        thread.start()

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
        # to do : dan (use self.side)

    def display_left_or_right(self):
        if self.consecutive_good_clicks <= 4:
            return
            # to do : dan (use self.side)
        else: 
            self.swap_side()
        # to do : dan (use self.side)

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
            else: 
                if good_collision:
                    return ClickTypes.GOOD
                else:
                    return ClickTypes.BAD
        else:
            self.consecutive_random_swaps = 0
            if good_collision:
                return ClickTypes.GOOD
            else:
                return ClickTypes.BAD

    def check_collision(self, x, y):
        # to do Dan (use self.side)
        return True
    


        if DisplayPatterns.LEFT_OR_RIGHT_WITH_RANDOMNESS:
            swap = random.uniform(0, 1) <= 0.2
            if swap:
                self.consecutive_random_swaps += 1
            if self.consecutive_random_swaps <= 2:
                if (good_collision and not swap) or (not good_collision and swap):
                    return ClickTypes.GOOD
                else:
                    return ClickTypes.BAD
            else: 
                if good_collision:
                    return ClickTypes.GOOD
                else:
                    return ClickTypes.BAD