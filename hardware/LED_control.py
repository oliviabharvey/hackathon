import RPi.GPIO as GPIO  # pip install RPi.GPIO
import time # Only used for debug.

# TODO: Test LED script to confirm activation / stop
# TODO: Confirm if LEDs are Pi (direct) or externally driven (Transitor)


class led_control:
    """
    Enabling control of a single LED.
    """

    def __init__(self, pin, debug=False):
        self.debug = bool(debug)
        self.pin = pin


    def setup(self):
        GPIO.setmode(GPIO.BOARD)    # Numbers GPIOs by physical location
        # GPIO.setmode(GPIO.BCM)    # Numbers GPIOs by GPIO
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin,GPIO.LOW)


    def light_state(self):
        # Check current light status. 1/True if on - 0/False otherwise.
        GPIO.input(self.pin)


    def light_on(self):
        # Turn lights on and output at 1/True
        GPIO.output(self.pin,GPIO.HIGH)
        return self.light_state


    def light_off(self)
        # Turn lights off and output at 0/False
        GPIO.output(self.pin,GPIO.HIGH)
        return self.light_state



class LEDs:
    """
    Enabling control of all LEDs.
    """

    def __init__(self, debug=False):
        self.debug = bool(debug)
        self.ExperienceLEDPin = 29 # Physical location (GPIO pin# 5)
        self.TrayLEDPin = 31 # Physical location (GPIO pin# 6)
        self.BoxLEDPin = 33 # Physical location (GPIO pin# 13)
        self.LEDPins = [self.ExperienceLEDPin, self.TrayLEDPin, self.BoxLEDPin]

        # Initiliazing future LED objects
        self.ExperienceLED = None
        self.TrayLED = None
        self.BoxLED = None

    def setup(self)
        # Initiliazing lEDs
        self.ExperienceLED = led_control(pin=self.ExperienceLEDPin,debug=self.debug)
        self.TrayLED = led_control(pin=self.TrayLEDPin,debug=self.debug)
        self.BoxLED = led_control(pin=self.BoxLEDPin,debug=self.debug)
        
        self.ExperienceLED.setup()
        self.TrayLED.setup()
        self.BoxLED.setup()
        print ('LEDs initialized')



###################################
## TEST WHEN CALLING THIS SCRIPT ##
###################################
if __name__ == '__main__':
    debug=True
    if debug:
        Lights = LEDs(debug=debug)

        print('Turning on Experiment LED')
        Lights.ExperienceLED.light_on()
        time.sleep(500)
        print('Experiment LED is currently: ',Lights.ExperienceLED.light_state())
        time.sleep(500)
        print('Turning off Experiment LED')
        Lights.ExperienceLED.light_off()
        time.sleep(1000)

        print('Turning on TrayLED')
        Lights.TrayLED.light_on()
        time.sleep(500)
        print('Tray LED is currently: ',Lights.TrayLED.light_state())
        time.sleep(500)
        print('Turning off Tray LED')
        Lights.TrayLED.light_off()
        time.sleep(1000)

        print('Turning on Box LED')
        Lights.BoxLED.light_on()
        time.sleep(500)
        print('Box LED is currently: ',Lights.BoxLED.light_state())
        time.sleep(500)
        print('Turning off Box LED')
        Lights.BoxLED.light_off()
        time.sleep(1000)

        print('End of test.')
        GPIO.cleanup()