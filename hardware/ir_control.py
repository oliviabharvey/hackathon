import RPi.GPIO as GPIO  # pip install RPi.GPIO
import time

# TODO: Test Infrared script to confirm activation / stop


class IrLed:
    """
    Enabling control of the infrared LED beam sensor
    """
    def __init__(self, debug=False):
        self.debug = bool(debug)
        self.ir_led_pin = 11 # Physical location (GPIO pin# 17)
        self.ir_sensor_pin = 12 # Physical location (GPIO pin# 18)
        self.state = False  # Beam connected = True, Broken =  False
        self.max_state_trigger = 5  # After X refresh rate (default 10Hz, 5step -> 500ms), confirms the mouse is in place
        self.irb_broken_counter = 0
        self.irb_complete_counter = 0
        self.is_irb_broken = False  # Beam disrupted trigger (mouse is there)      

    def setup(self):
        # Setup Receiver
        GPIO.setmode(GPIO.BOARD)    # Numbers GPIOs by physical location
        # GPIO.setmode(GPIO.BCM)    # Numbers GPIOs by GPIO
        GPIO.setup(self.ir_led_pin, GPIO.OUT)
        GPIO.setup(self.ir_sensor_pin, GPIO.IN)
        # Update state
        self.is_irb_broken = False
        self.state = False

    def check_beam_status(self):
        timer = 0
        debug_timer = 11 # 10 sec debug session
        step = 0.100 # 10Hz refresh rate
        while timer < debug_timer:
            time.sleep(step) # 10Hz refresh rate
            # import pdb; pdb.set_trace()
            self.state = bool(GPIO.input(self.ir_sensor_pin))
            if self.state:  # If beam is complete
                self.irb_broken_counter = 0
                self.irb_complete_counter += 1
                if self.irb_complete_counter >= self.max_state_trigger:
                    self.is_irb_broken = False
            else:  # If beam is broken
                self.irb_complete_counter = 0
                self.irb_broken_counter += 1
                if self.irb_broken_counter >= self.max_state_trigger:
                    self.is_irb_broken = True
                    break
            # While debugging print beam status every 500 ms
            if self.debug:
                timer += step
                print('Is Beam Broken: ', self.is_irb_broken)
        return self.is_irb_broken

    def start_irb(self):
        is_irb_broken = False
        self.start_ir()
        # Start the listener - Will stop when beam is broken (True)
        is_irb_broken = self.check_beam_status()
        if self.debug:
            print('Stopped. Final Was Beam Broken: ', is_irb_broken)
        return is_irb_broken

    def start_ir(self):
        GPIO.output(self.ir_led_pin,GPIO.HIGH)
        return bool(GPIO.input(self.ir_led_pin))

    def stop_ir(self):
        GPIO.output(self.ir_led_pin,GPIO.LOW)
        return bool(GPIO.input(self.ir_led_pin))

###################################
## TEST WHEN CALLING THIS SCRIPT ##
###################################
if __name__ == '__main__':
    debug=True
    if debug:
        irb = IrLed(debug=debug)
        irb.setup()
        print('Try to break the beam. Status is printed every 100ms.')
        print('Test will last 10 sec. Breaking beam will stop test.')
        time.sleep(1)
        irb.start_irb()
        print('End of test.')
        GPIO.cleanup()