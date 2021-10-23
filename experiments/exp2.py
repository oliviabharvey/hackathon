import time
import random

from experiments.base_exp import BaseExperiment
from utils.enums import *

class Experiment2(BaseExperiment):
    """
    Definition of Experiment of Stage 2
    """

    def __init__(self, duration_minutes=60):
        super().__init__(duration_minutes)
        return

    def initialize(self):
        """
        Starting experiment with first steps.
        """
        super().initialize()
        self.initialize_touch_screen_helper(ScreenTypes.TWO_SQUARES)
        # self.touch_screen_helper.display_image()
        self.proceed_to_touch_or_delay()

    def proceed_to_touch_or_delay(self):
        """
        Update states to waiting for mouse to interract with tourch screen, and waiting for timer. 
        """
        self.log_msg('Waiting for mouse to touch screen or 30 sec delay.')
        self.state = States.TOUCH_OR_DELAY
        self.touch_time_start = time.time()
        self.good_click = False

    def on_click(self):
        self.good_click = True
        return 

    def update_state(self):
        if self.state == States.TOUCH_OR_DELAY:
            #if random.uniform(0, 1) >= 0.95:  # TO UPDATE
             #   self.good_click = True
            if self.good_click:
                self.deliver_sequence(qty=60)
                self.proceed_to_delay_step()
            elif time.time() - self.touch_time_start >= 30:
                self.deliver_sequence(qty=20)
                self.proceed_to_delay_step()
        elif self.state == States.RESET_DELAY: 
            self.delay_time_left -= self.tick
            if self.delay_time_left <= 0:
                self.proceed_to_touch_or_delay()
