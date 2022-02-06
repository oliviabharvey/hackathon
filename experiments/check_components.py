import time
import random

from experiments.base_exp import BaseExperiment
from utils.enums import *
from hardware.motor_control import MotorControl
from hardware.ir_control import IrLed

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
        sys.stdout.write("\nChecking all components")
        sys.stdout.write("\nInitializing tests and turning experiment light on")
        super().initialize() # calls the initalization method within the superclass BaseExperiment
        time.sleep(2)
        # Check buzzer
        sys.stdout.write('\nChecking buzzer')
        self.hardware_connector.play_tone(duration=2)
        time.sleep(2)
        # Check light of the tray
        sys.stdout.write('\nChecking tray light')
        self.hardware_connector.turn_tray_light_on()
        time.sleep(2)
        # Check motor
        sys.stdout.write('\nChecking motor')
        motor = MotorControl()
        motor.setup()
        sys.stdout.write('\nTurning clockwise full turn')
        motor.full_rotation(2)
        time.sleep(1)
        sys.stdout.write('\nTurning counterclockwise full turn')
        motor.full_rotation(-2)
        time.sleep(1)
        # Check IR
        sys.stdout.write("\nChecking IR")
        irled = IrLed()
        irled.check_ir()

    def update_state(self):
        return