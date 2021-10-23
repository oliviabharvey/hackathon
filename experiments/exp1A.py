import time
import random

from experiments.base_exp import BaseExperiment
from utils.enums import *

class Experiment1A(BaseExperiment):
    """
    Definition of Experiment of Stage 1A
    """

    def __init__(self, duration_minutes=10):
        super().__init__(duration_minutes)
        return

    def initialize(self):
        """
        Starting experiment with first steps.
        """
        super().initialize()

    def update_state(self):
        return