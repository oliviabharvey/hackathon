import logging
import os
import random
import threading
from pynput.mouse import Listener

from utils.enums import *
from module_touchscreen.image_creator import ImageCreator

os.environ["DISPLAY"]=":0"


class TouchScreenHelper():
    """
    The TouchScreenHelper class creates an object that has a lot of methods to help us with the touch screen.
    It is instantiated in the base experiments since a lot of experiments require the touch screen and interaction with images.
    It takes as inputs an experiment and a display type.
    """
    def __init__(self, experiment, display_type):
        self.current_exp = experiment
        self.display_type = display_type
        self.touch_screen_enabled = False
        thread = threading.Thread(target=self.start_listening, args=())
        thread.daemon = True
        thread.start()

        # We also need to intialize some counters to track the progress of the experiments
        self.imageCreator = ImageCreator()
        self.side = random.choice([Sides.LEFT, Sides.RIGHT])
        self.same_side_count = 0
        self.consecutive_good_clicks = 0
        self.count_reversals = None
        self.consecutive_random_swaps = 0
        self.isListenerStarted = False
        return

    def start_listening(self):
        """
        This function will initialize the tracking of the movements on the touchscreen
        """
        with Listener(on_move=self.on_move) as listener:
            self.listener_ref = listener
            isListenerStarted = True
            listener.join()

    def on_move(self, x, y):
        """
        This function monitors the movement on the touchscreen and whether the touches are 
        good (in a rectangle) or not (outside of the borders of a rectangle)
        """
        if  self.touch_screen_enabled:
            self.touch_screen_enabled = False
            click_type, good_collision = self.check_click_type(x, y)
            self.current_exp.on_click(click_type, good_collision)

    def show_next_image(self):
        """
        This function shows the next image depending on the state of the display type
        """
        if self.display_type == DisplayPatterns.NONE:
            self.display_black_screen()
        elif self.display_type == DisplayPatterns.FIND_THE_SQUARE:
            self.display_find_the_square()
        elif self.display_type == DisplayPatterns.LEFT_OR_RIGHT or \
         self.display_type == DisplayPatterns.LEFT_OR_RIGHT_WITH_RANDOMNESS:
            self.display_left_or_right()
        
        self.touch_screen_enabled = True
    
    def display_black_screen(self):
        """
        This function displays the black screen
        """
        self.imageCreator.reset_canvas()

    def display_single_rectangle(self):
        """
        This function displays a single rectangle given the state self.side of the object.
        """
        if self.side == Sides.LEFT:
            self.imageCreator.show_left_rectangle()
        elif self.side == Sides.RIGHT:
            self.imageCreator.show_right_rectangle()

    def display_both_rectangle(self):
        self.imageCreator.show_left_and_right_rectangles()

    def display_find_the_square(self):
        """
        This function displays a single rectangle. In order to do so, it will randomly choose between displaying
        the rectangle on the same side or not. If the rectangle is being displayed in the same side 3 times or more, then 
        we enforce the object to swap sides. 
        """
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
        """
        This function checks whether there has been 5 or more consecutive good clicks.
        It will swap the side of the rectangle depending on this condition.
        """
        if self.consecutive_good_clicks >= 5:
            if self.count_reversals == None:
                self.count_reversals = 1
            else:
                self.count_reversals += 1
            self.swap_side()
        self.display_both_rectangle()

    def swap_side(self):
        if self.side == Sides.LEFT:
            self.side = Sides.RIGHT
        else: 
            self.side = Sides.LEFT

    def check_click_type(self, x, y):
        """
        This function checks for the validity of the click using mulitple functions.
        It checks whether it's a good or bad collision. We also increment a counter to take note
        of the consecutive good clicks.

        If the collision is good, we return a given number representing GOOD and the boolean
        """
        good_collision = self.check_collision(x, y)
        if good_collision:
            self.consecutive_good_clicks += 1         

        else: 
            self.consecutive_good_clicks = 0

        if self.display_type == DisplayPatterns.LEFT_OR_RIGHT_WITH_RANDOMNESS and random.uniform(0, 1) <= 0.2:
            self.consecutive_random_swaps += 1
            if self.consecutive_random_swaps <= 2:
                if good_collision:
                    return ClickTypes.BAD, good_collision
                else:
                    return ClickTypes.GOOD, good_collision

        self.consecutive_random_swaps = 0
        if good_collision:
            return ClickTypes.GOOD, good_collision
        else:
            return ClickTypes.BAD, good_collision

    def check_collision(self, x, y) -> bool:
        """
        Depending on the coordinates, this checks whether the click on the touchscreen
        was inside the left or right rectangle or outside the rectangles

        Inputs:
            - x: a coordinate on the X axis
            - y: a coordinate on the Y axis

        Outputs:
             - Check if the touch was inside the borders of the rectangles (True or False)
        """
        if self.side == Sides.LEFT:
            box_left = ImageCreator.rectangle_left[0][0]
            box_right = ImageCreator.rectangle_left[1][0]
            box_top = ImageCreator.rectangle_left[1][1]
            box_bottom = ImageCreator.rectangle_left[0][1]
        elif self.side == Sides.RIGHT:
            box_left = ImageCreator.rectangle_right[0][0]
            box_right = ImageCreator.rectangle_right[1][0]
            box_top = ImageCreator.rectangle_right[1][1]
            box_bottom = ImageCreator.rectangle_right[0][1]
        else:
            return False
        return self.check_collision_internal(x,y,box_left, box_right, box_top, box_bottom)


    def check_collision_internal(self,click_x, click_y, box_left, box_right, box_top, box_bottom) -> bool:
        """
        This function checks whether the collision happenned inside or outside certain coordinates.
        It returns True or False
        """
        return not (click_x < box_left or click_x > box_right or click_y > box_top or click_y < box_bottom)

    def get_number_reversals(self):
        return self.count_reversals