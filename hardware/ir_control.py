import RPi.GPIO as GPIO  # pip install RPi.GPIO
import time
import sys

# TODO: Test Infrared script to confirm activation / stop


class IrLed:
    """
    Enabling control of the infrared LED beam sensor (both the source LED light) and the receiver)
    """
    def __init__(self, debug: bool = False, irb_verbose: bool = False):
        self.debug = bool(debug)
        self.irb_verbose = bool(irb_verbose)
        self.ir_led_pin = 11 # Physical location (GPIO pin# 17)
        self.ir_sensor_pin = 12 # Physical location (GPIO pin# 18)
        self.state = False  # Beam connected = True, Broken =  False
        self.max_state_trigger = 5  # After X refresh rate (default 10Hz, 5step -> 500ms), confirms the mouse is in place
        self.irb_broken_counter = 0  # Counter to say how long was the beam broken. Increases by 1 every timestep the beam is broken.
        self.irb_complete_counter = 0  # Counter to say how long was the beam NOT broken. Increases by 1 every timestep the beam is continous.
        self.is_irb_broken = False  # Beam disrupted trigger (mouse is there). Activated once max_state_trigger is achieve.

    def setup(self):
        """
        Setting pin output (physical pin connection) for the infrared beam.
        Setting initial state as unbroken.
        """
        # Setup Receiver
        GPIO.setmode(GPIO.BOARD)    # Numbers GPIOs by physical location
        # GPIO.setmode(GPIO.BCM)    # Numbers GPIOs by GPIO
        GPIO.setup(self.ir_led_pin, GPIO.OUT)
        GPIO.setup(self.ir_sensor_pin, GPIO.IN)
        # Update state
        self.is_irb_broken = False
        self.state = False
        sys.stdout.write('\n IR beam initialized')

    def check_beam_status(self) -> bool:
        """
        Continuously checking if the beam as been broken.
        If the beam has been broken (500ms of being continously broken), we assume the beam 
        was effectively broken and the object (e.g. a mouse) is there.

        Outputs:
            - is_irb_broken: Returns True when the beam is broken.
        """
        step = 0.100 # 10Hz refresh rate
        while True:
            time.sleep(step) # 10Hz refresh rate
            self.state = bool(GPIO.input(self.ir_sensor_pin))
            if self.state:  # If beam is complete
                self.irb_broken_counter = 0
                self.irb_complete_counter += 1
                # After set time (default 500ms), change the state of the beam.
                if self.irb_complete_counter >= self.max_state_trigger:
                    self.is_irb_broken = False
            else:  # If beam is broken
                self.irb_complete_counter = 0
                self.irb_broken_counter += 1
                # After set time (default 500ms), change the state of the beam.
                if self.irb_broken_counter >= self.max_state_trigger:
                    self.is_irb_broken = True
                    break
            # While debugging print beam status every 500 ms
            if self.debug:
                if self.irb_verbose:
                    sys.stdout.write('\nIs Beam Broken: ' + str(self.is_irb_broken))
        return self.is_irb_broken

    def start_irb(self) -> bool:
        """
        Gouverning method to start the infrared beam (IRB), and then listen until the beam was broken.
        When broken, return a true statement.

        Outputs:
            - is_irb_broken: Returns True when the beam is broken.
        """
        is_irb_broken = False
        self.start_ir()
        # Start the listener - Will stop when beam is broken (True)
        is_irb_broken = self.check_beam_status()
        if self.debug:
            sys.stdout.write('\nBeam was Broken: ' + str(self.is_irb_broken))
        return is_irb_broken

    def start_ir(self) -> bool:
        """
        Start the infrared LED, sending a signal to the receiver.

        Outputs:
            - Boolean status of the LED (Open = True)
        """
        GPIO.output(self.ir_led_pin,GPIO.HIGH)
        return bool(GPIO.input(self.ir_led_pin))

    def stop_ir(self) -> bool:
        """
        Stop the infrared LED, stopping any signal at the receiver.

        Outputs:
            - Boolean status of the LED (Close = False)
        """
        GPIO.output(self.ir_led_pin,GPIO.LOW)
        return bool(GPIO.input(self.ir_led_pin))

    def check_ir(self):
        self.setup()
        self.start_ir()
        self.state = bool(GPIO.input(self.ir_sensor_pin))
        if self.state == True:
            sys.stdou.write("\nIR beam works")
        else:
            sys.stdout.write("\nIR beam fails")      

    def gpio_cleanup(self):
        """
        Remove ALL GPIO pins from memory, even if sets elsewhere. To be called once at the end of the script.
        """
        GPIO.cleanup()


"""
When calling this script directly, a small unit test (defined below) is run for debugging purposes.
"""
###################################
## TEST WHEN CALLING THIS SCRIPT ##
###################################
if __name__ == '__main__':
    debug=True
    if debug:
        irb = IrLed(debug=debug)
        irb.setup()
        sys.stdout.write('\nTry to break the beam: place something between IR LED and receiver.\nStatus is printed every 100ms.')
        sys.stdout.write('\nTest will last beam is broken.')
        time.sleep(1)
        irb.start_irb()
        sys.stdout.write('\nEnd of test.')
        GPIO.cleanup()