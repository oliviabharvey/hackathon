import time
import random

from experiments.base_exp import BaseExperiment
from utils.enums import *

class Exp2(BaseExperiment):
    """
    Definition of Experiment of Stage 2
    """

    def __init__(self, cfg, duration_minutes=60, debug=False, enableAutoClick=False):
        super().__init__(cfg, duration_minutes, debug, enableAutoClick)
        return

    def initialize(self):
        """
        Starting experiment with first steps.
        """
        super().initialize()
        self.initialize_touch_screen_helper(DisplayPatterns.FIND_THE_SQUARE)
        self.touch_screen_helper.show_next_image()
        self.proceed_to_touch_or_delay()

    def proceed_to_touch_or_delay(self):
        """
        Update states to waiting for mouse to interract with tourch screen, and waiting for timer. 
        """
        self.log_msg('Waiting for mouse to touch screen or 30 sec delay.')
        self.state = States.TOUCH_OR_DELAY
        self.touch_time_start = time.time()
        self.click_type = ClickTypes.NONE
        self.touch_screen_helper.show_next_image()

    def update_state(self):
        if self.state == States.TOUCH_OR_DELAY:
            if self.enableAutoClick:
                if random.uniform(0, 1) >= 0.95:
                    self.click_type = ClickTypes.GOOD
            if self.click_type == ClickTypes.GOOD:
                self.touch_screen_helper.display_black_screen()
                self.deliver_sequence(qty=60)
                self.proceed_to_ir_break()
            elif time.time() - self.touch_time_start >= 30:
                self.touch_screen_helper.display_black_screen()
                self.deliver_sequence(qty=20)
                self.proceed_to_ir_break()
        elif self.state == States.IR_BREAK: 
            if self.hardware_connector.is_irb_broken() == True:
                self.proceed_to_delay_step()
        elif self.state == States.RESET_DELAY: 
            self.delay_time_left -= self.tick
            if self.delay_time_left <= 0:
                self.proceed_to_touch_or_delay()
