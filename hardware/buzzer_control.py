import RPi.GPIO as GPIO  # pip install RPi.GPIO
import threading
import time 

# TODO: Test piezzo script to confirm activation / stop
# TODO: Check if default volume is too / not enough loud

class BuzzerControl:
    """
    Enabling control of the buzzer (frequency, duration and volume)
    """

    def __init__(self,frequency=3000, duration=1, DutyCycle=50, debug=False):
        self.debug = bool(debug)
        # This pin needs to be PWM capable [(GPIO pin# 12,13,18,19])
        self.BuzzerPin = 32 # Physical location (GPIO pin# 12)
        self.DutyCycle = int(DutyCycle) # 0 to 100 - Volume
        self.Frequency = int(abs(frequency))  # Frequency (Hz)
        self.Duration = float(abs(duration))  # Sound duration (sec)
        self.Buzzer = None

    def setup(self):
        GPIO.setmode(GPIO.BOARD)    # Numbers GPIOs by physical location
        # GPIO.setmode(GPIO.BCM)    # Numbers GPIOs by GPIO
        GPIO.setup(self.buzzerPin, GPIO.OUT)
        self.Buzzer = GPIO.PWM(self.BuzzerPin, self.Frequency)
        
    
    def start_sound(self,frequency=self.Frequency,time=self.Duration, volume=self.DutyCycle):
        if self.debug:
            print('Playing sound')
        Buzzer = GPIO.PWM(self.buzzerPin, frequency)
        Buzzer.start(volume)
        time.sleep(time)
        Buzzer.stop()
        #sys.exit() could be a harsh solution if we cumulate too many threads.
        # Could use a _is_running variable? (https://stackoverflow.com/questions/4541190/how-to-close-a-thread-from-within)

    def play_sound(self,frequency=self.Frequency,time=self.Duration, volume=self.DutyCycle)):
        thread = threading.Thread(target=self.start_sound, args=(frequency,time,volume), deamon=True)
        thread.start()

    def stop_buzzer(self):
        GPIO.cleanup()

###################################
## TEST WHEN CALLING THIS SCRIPT ##
###################################
if __name__ == '__main__':
    debug=True
    if debug:
        buzzer = buzzer_control(debug=debug)
        buzzer.setup()

        print('Playing "normal" sound')
        buzzer.start_sound()

        print('Funky stuff...')
        buzzer.start_sound(frequency=440,time=0.5, volume=75)
        buzzer.start_sound(frequency=880,time=0.5, volume=25)
        buzzer.start_sound(frequency=2000,time=0.5, volume=50)

        print('Testing thread')
        buzzer.play_sound()

        print('End of test.')
        GPIO.cleanup()