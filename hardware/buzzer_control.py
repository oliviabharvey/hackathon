import RPi.GPIO as GPIO  # pip install RPi.GPIO
import time 

# TODO: Test piezzo script to confirm activation / stop
# TODO: Check if default volume is too / not enough loud

class buzzer_control:
    """
    Enabling control of the buzzer (frequency, duration and volume)
    """

    def __init__(self,frequency=3000, duration=1000, DutyCycle=50, debug=False):
        self.debug = bool(debug)
        # This pin needs to be PWM capable [(GPIO pin# 12,13,18,19])
        self.BuzzerPin = 32 # Physical location (GPIO pin# 12)
        self.DutyCycle = int(DutyCycle) # 0 to 100 - Volume
        self.Frequency = int(abs(frequency))  # Frequency (Hz)
        self.Duration = int(abs(duration))  # Sound duration (ms)
        self.Buzzer = None

    def setup(self):
        GPIO.setmode(GPIO.BOARD)    # Numbers GPIOs by physical location
        # GPIO.setmode(GPIO.BCM)    # Numbers GPIOs by GPIO
        GPIO.setup(self.buzzerPin, GPIO.OUT)
        self.Buzzer = GPIO.PWM(self.BuzzerPin, self.Frequency)
        
    
    def play_sound(self,frequency=self.Frequency,time=self.Duration, volume=self.DutyCycle):
        if debug:
            print('Playing sound')
        Buzzer = GPIO.PWM(self.buzzerPin, frequency)
        Buzzer.start(volume)
        time.sleep(time)
        Buzzer.stop()


###################################
## TEST WHEN CALLING THIS SCRIPT ##
###################################
if __name__ == '__main__':
    debug=True
    if debug:
        buzzer = buzzer_control(debug=debug)
        buzzer.setup()

        print('Playing "normal" sound')
        buzzer.play_sound()

        print('Funky stuff...')
        buzzer.play_sound(frequency=440,time=500, volume=75)
        buzzer.play_sound(frequency=880,time=500, volume=25)
        buzzer.play_sound(frequency=2000,time=500, volume=50)

        print('End of test.')
        GPIO.cleanup()