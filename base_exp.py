import time
import random

from enum import Enum

TICK = 0.1

class BaseExperiment():

    def __init__(self, duration_minutes):
        self.exp_duration = duration_minutes * 60 # duration in seconds TO UPDATE
        return

    def run_experiment(self):
        """
        Initializes and runs experiment, then perform end of experiment steps.
        """
        self.initialize()
        while not self.is_completed():
            self.update_state()
            time.sleep(TICK)
        self.on_completion()

    def initialize(self):
        """
        Initiates food delivery sequence. 
        """
        self.start_time = time.time()
        self.log_msg('Starting Experiment')

    def deliver_sequence(self, qty=100):
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

    def has_head_in_tray(self):
        return random.choice([True, False]) # TO UPDATE

    def tray_light_off(self):
        return

    def on_completion(self):
        print('finished!!')

    def log_msg(self, msg):
        print(f'Time: {round(time.time() - self.start_time, 1)} s - {str(msg)}')


