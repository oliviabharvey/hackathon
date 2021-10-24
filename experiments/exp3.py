import time
import random

from experiments.base_exp import BaseExperiment
from utils.enums import *

class Exp3(BaseExperiment):
    """
    Definition of Experiment of Stage 3
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
        self.proceed_to_touch()

    def update_state(self):
        if self.state == States.TOUCH:
            if self.enableAutoClick:
                if random.uniform(0, 1) >= 0.98:
                    self.click_type = ClickTypes.GOOD
                    self.on_click(self.click_type, True)
            if self.click_type == ClickTypes.GOOD:
                self.touch_screen_helper.display_black_screen()
                self.deliver_sequence(qty=20)
                self.proceed_to_ir_break()

        elif self.state == States.IR_BREAK: 
            if self.hardware_connector.is_irb_broken() == True:
                self.on_ir_break()
                self.proceed_to_delay_step()

        elif self.state == States.RESET_DELAY: 
            self.delay_time_left -= self.tick
            if self.delay_time_left <= 0:
                self.proceed_to_touch()
