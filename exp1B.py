import time
import random

from base_exp import BaseExperiment
from enums import *

class Experiment1B(BaseExperiment):
    """
    Definition of Experiment of Stage 1B
    """

    def __init__(self, duration_minutes=20):
        super().__init__(duration_minutes)
        return

    def initialize(self):
        """
        Starting experiment with first steps.
        """
        super().initialize()
        self.proceed_to_eat_and_exit()
        self.deliver_sequence(qty=150)

    def proceed_to_eat_and_exit(self):
        """
        Update states to waiting for mouse to eat and exit tray.
        """
        self.log_msg('Waiting for mouse to eat food and exit tray')
        self.state = States.EAT_AND_EXIT
        self.need_to_go_in_tray = True

    def update_state(self):
        if self.state == States.EAT_AND_EXIT:
            if self.need_to_go_in_tray and self.has_head_in_tray():
                self.need_to_go_in_tray = False
            elif not self.need_to_go_in_tray and not self.has_head_in_tray():
                self.proceed_to_delay_step()
        elif self.state == States.RESET_DELAY: 
            if not self.has_head_in_tray():
                self.delay_time_left -= self.tick
            if self.delay_time_left <= 0:
                self.deliver_sequence(qty=20)
                self.proceed_to_eat_and_exit()