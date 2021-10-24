import random

class HardwareConnector():
    """
    Enables interfacting with the various sensors/actuators (except touch screen).
    """

    def __init__(self, debug=False):
        self.debug = debug


    def is_irb_broken(self):
        # return True if broken, False otherwise
        if self.debug: 
            ir_break = False
            if random.uniform(0, 1) >= 0.95:
                ir_break = True
            return ir_break
        else: 
            return False

    def play_tone(self, duration):
        # start playing tone for duration, but do not wait for it to be finished
        # to continue (needs to be asynchronous)
        return

    def turn_tray_light_on(self):
        # no duration, just do it!
        return

    def turn_tray_light_off(self):
        # no duration, just do it!
        return

    def squeeze_seringe(self, qty):
        # turn motor to provide a given qty of fluid (in microliter) in food tray.
        # This probably needs to be asynchronous.
        return
