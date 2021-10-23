import time
import random

from enum import Enum

TICK = 0.1

class States(Enum):
    """
    Defines all possible states
    """
    EAT_AND_EXIT = 1
    DELAY = 2

class Experiment1B():
    """
    Definition of Experiment of Stage 1B
    """

    def __init__(self):
        self.exp_duration = 20 * 60 # duration in seconds
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
        self.proceed_to_eat_and_exit()
        self.deliver_sequence(qty=150)

    def proceed_to_eat_and_exit(self):
        self.log_msg('Waiting for mouse to eat food and exit tray')
        self.state = States.EAT_AND_EXIT
        self.need_to_go_in_tray = True

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
        if self.state == States.EAT_AND_EXIT:
            if self.need_to_go_in_tray and self.has_head_in_tray():
                self.need_to_go_in_tray = False
            elif not self.need_to_go_in_tray and not self.has_head_in_tray():
                self.proceed_to_delay_step()
        elif self.state == States.DELAY: 
            if not self.has_head_in_tray():
                self.delay_time_left -= TICK
            if self.delay_time_left <= 0:
                self.deliver_sequence(qty=20)
                self.proceed_to_eat_and_exit()

    def has_head_in_tray(self):
        return random.choice([True, False]) # TO UPDATE

    def proceed_to_delay_step(self):
        self.tray_light_off()
        self.delay_time_left = 10
        self.log_msg(f'Waiting for {self.delay_time_left} seconds while mouse is out of tray')
        self.state = States.DELAY

    def tray_light_off(self):
        return

    def on_completion(self):
        print('finished!!')

    def log_msg(self, msg):
        print(f'Time: {round(time.time() - self.start_time, 1)} s - {str(msg)}')

