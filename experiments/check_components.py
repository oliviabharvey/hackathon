import time
import random

from experiments.base_exp import BaseExperiment
from utils.enums import *

class CheckComponents(BaseExperiment):
    """
    Check that all components work before doing an experiment
    """

    def __init__(self, cfg, duration_minutes=1, debug=False, enableAutoClick=False):
        super().__init__(cfg, duration_minutes, debug, enableAutoClick)
        return

    def initialize(self):
        """
        Starting experiment with first steps.
        """
        super().initialize()
        self.initialize_touch_screen_helper(DisplayPatterns.NONE)

    def update_state(self):
        return