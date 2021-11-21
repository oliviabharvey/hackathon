import time
import random
from data.manager import DataManager
import sys

from module_touchscreen.touch_screen_helper import TouchScreenHelper
from hardware.hardware_connector import HardwareConnector
from utils.enums import *

TICK = 0.1

class BaseExperiment():

    def __init__(self, cfg, duration_minutes, debug=False, enableAutoClick=False):
        self.tick = TICK
        self.cfg = cfg
        self.exp_duration = duration_minutes * 60 # duration in seconds TO UPDATE
        self.debug = debug
        self.enableAutoClick = enableAutoClick
        return

    def run_experiment(self):
        """
        Initializes and runs experiment, then perform end of experiment steps.
        """
        try:
            self.initialize()
            while not self.is_completed():
                self.update_state()
                time.sleep(self.tick)
            self.on_completion()
        except:
            import sys            
            self.log_msg("Exception occured : "+ str(sys.exc_info())) 
            if self.debug :
                raise     
        
            self.data_mgr.update_status('error')
            self.data_mgr.write_dict(self.cfg['results'])

    def initialize(self):
        """
        Initiates initial steps of experiment.
        """
        self.start_time = time.time()
        self.log_msg('Starting Experiment')
        self.data_mgr = DataManager(self.cfg)
        self.data_mgr.update_status('running')
        self.hardware_connector = HardwareConnector(self.debug)
        self.hardware_connector.turn_experiment_light_on()


    def deliver_sequence(self, qty=100):
        """
        Performs full food delivery sequence: turning tray light on, playing tone and delivering food.
        """
        self.tray_light_on()
        self.play_tone() # asynch - we don't wait for tone to finish playing
        self.deliver_food(qty)

    def tray_light_on(self):
        self.hardware_connector.turn_tray_light_on() 
        return
    
    def play_tone(self):
        self.hardware_connector.play_tone(duration=5) 
        return

    def deliver_food(self, qty=100):
        self.hardware_connector.squeeze_syringe(qty)
        self.hardware_connector.play_tone(duration=2)
        self.hardware_connector.turn_tray_light_on()
        self.log_msg(f'Food delivered: {qty}')
        self.data_mgr.update(TimeStamps.FEED)

    def is_completed(self):
            return time.time() - self.start_time >= self.exp_duration

    def update_state(self):
        return

    def on_ir_break(self):
        self.ir_break = True
        self.data_mgr.update(TimeStamps.EAT)

    def tray_light_off(self):
        self.hardware_connector.turn_tray_light_off() 
        return

    def initialize_touch_screen_helper(self, display_type):
        self.touch_screen_helper = TouchScreenHelper(self, display_type)
        self.touch_screen_helper.display_black_screen()
        time.sleep(10)
        return

    def on_completion(self):
        self.touch_screen_helper.imageCreator.reset_canvas()
        self.touch_screen_helper.imageCreator.root.destroy()
        if self.touch_screen_helper.isListenerStarted:
            self.touch_screen_helper.listener_ref.stop()
        self.log_msg("Finished!")
        self.data_mgr.compute_end_of_experiment_statistics(self.start_time, self.touch_screen_helper.get_number_reversals())
        self.data_mgr.update_status('completed')
        self.data_mgr.write_dict(self.cfg['results'])
        self.hardware_connector.turn_experiment_light_off()

    def on_error(self):
        import sys            
        self.log_msg("Exception occured : "+ sys.exc_info()) 
        if self.debug:
            raise     
       
        self.data_mgr.update_status('error')
        self.data_mgr.write_dict(self.cfg['results'])

    def log_msg(self, msg):
        m, s = divmod((time.time() - self.start_time), 60)
        sys.stdout.write(f'\n Time: {round(m)} min {round(s,1)} s - {str(msg)}'.replace('0 min ', ''))

    def proceed_to_touch(self):
        """
        Update states to waiting for mouse to interract with tourch screen.
        """
        self.log_msg('Waiting for mouse to touch screen.')
        self.state = States.TOUCH
        self.click_type = ClickTypes.NONE
        self.show_next_image()

    def proceed_to_ir_break(self):
        self.log_msg(f'Waiting for mouse to get into food tray.')
        self.state = States.IR_BREAK
        self.ir_break = False

    def proceed_to_delay_step(self):
        
        self.tray_light_off()
        self.delay_time_left = 10
        if self.debug:
            self.delay_time_left = 5
        self.log_msg(f'Waiting for {self.delay_time_left} seconds.')
        self.state = States.RESET_DELAY

    def proceed_to_punish_delay(self, delay=5):
        #self.tray_light_on()
        self.punish_time_left = delay
        if self.debug:
            self.punish_time_left = 5
        self.log_msg(f'Waiting for {self.punish_time_left} seconds due to incorrect touch.')
        self.state = States.PUNISH_DELAY

    def on_click(self, click_type, good_collision):
        self.click_type = click_type # wheter the mouse is rewarded: GOOD = reward
        rewarded = click_type == ClickTypes.GOOD
        success = good_collision
        self.data_mgr.update(TimeStamps.TOUCH, {'rewarded': rewarded, 'success': success})
        return

    def show_next_image(self):
        self.touch_screen_helper.show_next_image()
        self.data_mgr.start_trial()
        self.data_mgr.update(TimeStamps.DISPLAY)