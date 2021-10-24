import RPi.GPIO as GPIO  # pip install RPi.GPIO
import time 

# TODO: Test piezzo script to confirm activation / stop
# TODO: 

class buzzer_control:

    def __init__(self,frequency=3000, duration=1000, DutyCycle=50, debug_input=False):
        # This pin needs to be PWM capable [(GPIO pin# 12,13,18,19])
        self.BuzzerPin = 32 # Physical location (GPIO pin# 12)
        self.DutyCycle = int(DutyCycle) # 0 to 100 - Volume
        self.Frequency = int(abs(frequency))  # Frequency (Hz)
        self.Duration = int(abs(duration))  # Sound duration (ms)
        self.Buzzer = None

    def setup(self):
        print ('Buzzer Initialization...')
        GPIO.setmode(GPIO.BOARD)    # Numbers GPIOs by physical location
        # GPIO.setmode(GPIO.BCM)    # Numbers GPIOs by GPIO
        GPIO.setup(buzzerPin, GPIO.OUT)
        self.Buzzer = GPIO.PWM(self.BuzzerPin, self.Frequency)
    
    def play_sound(frequency=self.Frequency,time=self.Duration, volume=self.DutyCycle):

        Buzzer = GPIO.PWM(buzzerPin, frequency)
        Buzzer.start(volume)
        time.sleep(time)
        Buzzer.stop()

    def reset (): # To call at the end of experience
        GPIO.cleanup()