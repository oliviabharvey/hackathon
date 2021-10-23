import time
import random

from experiments.base_exp import BaseExperiment
from utils.enums import *

class Experiment4(BaseExperiment):
    """
    Definition of Experiment of Stage 4
    """

    def __init__(self, duration_minutes=60):
        super().__init__(duration_minutes)
        return

    def initialize(self):
        """
        Starting experiment with first steps.
        """
        super().initialize()
        self.initialize_touch_screen_helper(DisplayPatterns.FIND_THE_SQUARE)
        # self.touch_screen_helper.display_image()
        self.proceed_to_touch()

    def proceed_to_touch(self):
        """
        Update states to waiting for mouse to interract with tourch screen.
        """
        self.log_msg('Waiting for mouse to touch screen.')
        self.state = States.TOUCH
        self.good_click = False
        self.bad_click = False

    def on_click(self):
        self.good_click = False
        self.bad_click = False
        return 

    def update_state(self):
        if self.state == States.TOUCH:
            if random.uniform(0, 1) >= 0.99:  # TO UPDATE
                self.good_click = True
            if random.uniform(0,1) >= 0.99: # TO UPDATE
                self.bad_click = True
            if self.good_click:
                # self.touch_screen_helper.image_off()
                self.deliver_sequence(qty=20)
                self.proceed_to_ir_break()
            elif self.bad_click:
                # self.touch_screen_helper.image_off()
                self.proceed_to_punish_delay(delay=15)

        elif self.state == States.IR_BREAK: 
            if random.uniform(0, 1) >= 0.95:  # TO UPDATE
                self.ir_break = True
            if self.ir_break == True:
                self.proceed_to_delay_step()

        elif self.state == States.RESET_DELAY: 
            self.delay_time_left -= self.tick
            if self.delay_time_left <= 0:
                self.proceed_to_touch()

        elif self.state == States.PUNISH_DELAY: 
            self.punish_time_left -= self.tick
            if self.punish_time_left <= 0:
                self.proceed_to_delay_step()
