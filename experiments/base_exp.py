import time
import random
from data.manager import DataManager

from module_touchscreen.touch_screen_helper import TouchScreenHelper
from hardware.hardware_connector import HardwareConnector
from utils.enums import *

TICK = 0.1

class BaseExperiment():

    def __init__(self, cfg, duration_minutes, debug=False):
        self.tick = TICK
        self.cfg = cfg
        self.exp_duration = duration_minutes * 60 # duration in seconds TO UPDATE
        self.debug = debug
        return

    def run_experiment(self):
        """
        Initializes and runs experiment, then perform end of experiment steps.
        """
        self.initialize()
        while not self.is_completed():
            self.update_state()
            time.sleep(self.tick)
        self.on_completion()

    def initialize(self):
        """
        Initiates initial steps of experiment.
        """
        self.start_time = time.time()
        self.log_msg('Starting Experiment')
        self.hardware_connector = HardwareConnector(self.debug)
        self.data_mgr = DataManager(self.cfg)

    def deliver_sequence(self, qty=100):
        """
        Performs full food delivery sequence: turning tray light on, playing tone and delivering food.
        """
        self.tray_light_on()
        self.play_tone() # asynch - we don't wait for tone to finish playing
        self.deliver_food(qty)

    def tray_light_on(self):
        return
    
    def play_tone(self): 
        return

    def deliver_food(self, qty=100):
        self.log_msg(f'Food delivered: {qty}')

    def is_completed(self):
            return time.time() - self.start_time >= self.exp_duration

    def update_state(self):
        return

    def on_ir_break(self):
        self.ir_break = True

    def tray_light_off(self):
        return

    def initialize_touch_screen_helper(self, display_type):
        self.touch_screen_helper = TouchScreenHelper(self, display_type)
        return

    def on_completion(self):
        self.log_msg("Finished!")

    def log_msg(self, msg):
        print(f'Time: {round(time.time() - self.start_time, 1)} s - {str(msg)}')

    def proceed_to_ir_break(self):
        self.log_msg(f'Waiting for mouse to get into food tray.')
        self.state = States.IR_BREAK
        self.ir_break = False

    def proceed_to_delay_step(self):
        self.tray_light_off()
        self.delay_time_left = 10
        self.log_msg(f'Waiting for {self.delay_time_left} seconds.')
        self.state = States.RESET_DELAY

    def proceed_to_punish_delay(self, delay=5):
        self.tray_light_on()
        self.punish_time_left = delay
        self.log_msg(f'Waiting for {self.punish_time_left} seconds due to incorrect touch.')
        self.state = States.PUNISH_DELAY

    def on_click(self, click_type):
        self.click_type = click_type
        return