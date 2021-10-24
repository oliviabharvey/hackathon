import time
import random

from experiments.base_exp import BaseExperiment
from utils.enums import *

class Exp1A(BaseExperiment):
    """
    Definition of Experiment of Stage 1A
    """

    def __init__(self, cfg, duration_minutes=10, debug=False):
        super().__init__(cfg, duration_minutes, debug)
        return

    def initialize(self):
        """
        Starting experiment with first steps.
        """
        super().initialize()
        self.initialize_touch_screen_helper(DisplayPatterns.NONE)

    def update_state(self):
        return