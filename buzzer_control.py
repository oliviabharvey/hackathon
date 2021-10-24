import RPi.GPIO as GPIO  # pip install RPi.GPIO
import time 


# to test motor -> make fake counters
class buzzer_control:

    def __init__(self,frequency=3000, duration=1000, debug_input=False):
        self.buzzerPin = 7 # Physical location (GPIO pin# 4)
        self.frequency = frequency
        self.duration = duration

    def setup():
        print ('Buzzer Initialization...')
        GPIO.setmode(GPIO.BOARD)    # Numbers GPIOs by physical location
        # GPIO.setmode(GPIO.BCM)    # Numbers GPIOs by GPIO
        GPIO.setup(BuzzerPin, GPIO.OUT) 
    
    def sound(frequency=self.frequency,time=self.duration):

        Buzz = GPIO.PWM(BuzzerPin, 440) 
        Buzz.start(50) 
