import time
import random

from experiments.base_exp import BaseExperiment
from utils.enums import *

class Prl1(BaseExperiment):
    """
    Definition of Experiment of Stage PRL
    """

    def __init__(self, cfg, duration_minutes=60, debug=False, enableAutoClick=False):
        super().__init__(cfg, duration_minutes, debug, enableAutoClick)
        return

    def initialize(self):
        """
        Starting experiment with first steps.
        """
        super().initialize()
        self.initialize_touch_screen_helper(DisplayPatterns.LEFT_OR_RIGHT_WITH_RANDOMNESS)
        self.touch_screen_helper.show_next_image()
        self.proceed_to_touch()

    def proceed_to_touch(self):
        """
        Update states to waiting for mouse to interract with tourch screen.
        """
        self.log_msg('Waiting for mouse to touch screen.')
        self.state = States.TOUCH
        self.click_type = ClickTypes.NONE
        self.touch_screen_helper.show_next_image()

    def update_state(self):
        if self.state == States.TOUCH:
            if self.enableAutoClick:
                if random.uniform(0, 1) >= 0.99:
                    self.click_type = ClickTypes.GOOD
                if random.uniform(0,1) >= 0.99:
                    self.click_type = ClickTypes.BAD
            if self.click_type == ClickTypes.GOOD:
                self.touch_screen_helper.display_black_screen()
                self.deliver_sequence(qty=20)
                self.proceed_to_ir_break()
            elif self.click_type == ClickTypes.BAD:
                self.touch_screen_helper.display_black_screen()
                self.proceed_to_punish_delay()

        elif self.state == States.IR_BREAK: 
            if self.hardware_connector.is_irb_broken() == True:
                self.proceed_to_delay_step()

        elif self.state == States.RESET_DELAY: 
            self.delay_time_left -= self.tick
            if self.delay_time_left <= 0:
                self.proceed_to_touch()

        elif self.state == States.PUNISH_DELAY: 
            self.punish_time_left -= self.tick
            if self.punish_time_left <= 0:
                self.proceed_to_delay_step()
