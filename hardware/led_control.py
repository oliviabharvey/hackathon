import RPi.GPIO as GPIO  # pip install RPi.GPIO
import time # Only used for debug.
import sys

class LEDControl:
    """
    Class enabling control of a single LED.
    """

    def __init__(self, pin: int, debug: bool = False):
        self.debug = bool(debug)
        self.pin = int(pin)
        self.state = False

    def setup(self):
        """
        Setting pin output (physical pin connection) LED lighting (not the infrared LED).
        Setting initial LED state as OFF.
        """
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin,GPIO.LOW)
        self.state = False


    def update_light_state(self) -> bool:
        """
        Retrieve light state (True/On or False/Off).
        Outputs:
            - self.state: State of the LED.  Return True if on; False is off.
        """
        # Check current light status. True if on - False otherwise.
        self.state = bool(GPIO.input(self.pin))
        return self.state
        

    def light_on(self):
        """
        Turn on the light. Sends the new light status to confirm. 
        Outputs:
            - self.state: State of the LED.  Return True if on; False is off.
        """
        # Turn lights on and output at True
        GPIO.output(self.pin,GPIO.HIGH)
        self.update_light_state()
        return self.state

    def light_off(self):
        """
        Turn off the light. Sends the new light status to confirm. 
        Outputs:
            - self.state: State of the LED.  Return True if on; False is off.
        """
        # Turn lights off and output at False
        GPIO.output(self.pin,GPIO.LOW)
        self.update_light_state()
        return self.state



class LEDs:
    """
    Class enabling control of multiple LEDs. Overarching multiple object from the LEDControl class.
    """

    def __init__(self, debug: bool = False):
        self.debug = bool(debug)
        # Setup GPIO control for the led
        GPIO.setmode(GPIO.BOARD)    # Numbers GPIOs by physical location
        # GPIO.setmode(GPIO.BCM)    # Numbers GPIOs by GPIO
        self.ExperienceLEDPin = 29 # Physical location (pin #29, GPIO pin# 5)
        self.TrayLEDPin = 31 # Physical location (pin #31, GPIO pin# 6)
        self.BoxLEDPin = 33 # Physical location (pin #33, GPIO pin# 13)
        self.LEDPins = [self.ExperienceLEDPin, self.TrayLEDPin, self.BoxLEDPin]

        # Initiliazing future LED objects
        self.experience_led = None
        self.tray_led = None
        self.box_led = None

    def setup(self):
        """
        Setting pin output (physical pin connection) for all three lighting LED (excluding infrared LED).
        A LEDControl class object is created for each light.
        """
        # Initiliazing lEDs
        self.experience_led = LEDControl(pin=self.ExperienceLEDPin,debug=self.debug)
        self.tray_led = LEDControl(pin=self.TrayLEDPin,debug=self.debug)
        self.box_led = LEDControl(pin=self.BoxLEDPin,debug=self.debug)
        
        self.experience_led.setup()
        self.tray_led.setup()
        self.box_led.setup()
        sys.stdout.write('\nLEDs initialized')

    def stop_leds(self):
        """
        Methods to quickly turn off all LEDs at the end of an experiment
        """
        self.experience_led.light_off()
        self.tray_led.light_off()
        self.box_led.light_off()

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
        lights = LEDs(debug=debug)
        lights.setup()
        time.sleep(1)
        sys.stdout.write('\nTurning on Experiment LED')
        lights.experience_led.light_on()
        time.sleep(0.200)
        sys.stdout.write('\nExperiment LED is currently: %s' % lights.experience_led.state)
        time.sleep(0.500)
        sys.stdout.write('\nTurning off Experiment LED')
        lights.experience_led.light_off()
        time.sleep(0.200)
        sys.stdout.write('\nExperiment LED is currently: %s' % lights.experience_led.state)
        time.sleep(0.700)

        sys.stdout.write('\nTurning on tray_led')
        lights.tray_led.light_on()
        time.sleep(0.200)
        sys.stdout.write('\nTray LED is currently: %s' % lights.tray_led.state)
        time.sleep(0.500)
        sys.stdout.write('\nTurning off Tray LED')
        lights.tray_led.light_off()
        time.sleep(0.200)
        sys.stdout.write('\nTray LED is currently: %s' % lights.tray_led.state)
        time.sleep(0.700)

        sys.stdout.write('\nTurning on Box LED')
        lights.box_led.light_on()
        time.sleep(0.200)
        sys.stdout.write('\nBox LED is currently: %s' % lights.box_led.state)
        time.sleep(0.500)
        sys.stdout.write('\nTurning off Box LED')
        lights.box_led.light_off()
        time.sleep(0.200)
        sys.stdout.write('\nBox LED is currently: %s' % lights.box_led.state)
        time.sleep(0.700)

        sys.stdout.write('\nEnd of test.')
        lights.gpio_cleanup()