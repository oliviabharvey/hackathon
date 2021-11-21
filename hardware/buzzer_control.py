import RPi.GPIO as GPIO  # pip install RPi.GPIO
import threading
import time
import sys


class BuzzerControl:
    """
    Enabling control of the buzzer (frequency, duration and volume)
    """

    def __init__(self,frequency=3000, duration=5, DutyCycle=10, debug=False):
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
        GPIO.setup(self.BuzzerPin, GPIO.OUT)
        self.Buzzer = GPIO.PWM(self.BuzzerPin, self.Frequency)
        
    
    def start_sound(self, **kwargs):
        if self.debug:
            print('Playing sound')
        # Default values
        frequency = self.Frequency
        duration = self.Duration
        volume = self.DutyCycle
        kill_thread = False
        # User-specific input overide
        for item_name, value in kwargs.items():
            if item_name.lower() == 'frequency':
                frequency = value
            elif item_name.lower() == 'duration':
                duration = value
            elif item_name.lower() == 'volume':
                volume = value
            elif item_name.lower() == 'threaded':
                kill_thread = True
        
        self.Buzzer.ChangeFrequency(frequency)
        self.Buzzer.start(volume)
        time.sleep(duration)
        self.Buzzer.stop()
        if kill_thread:
            if self.debug:
                print('Killing buzzer thread now')
            sys.exit() # harsh solution, but easy to implement to kill thread.
            # Could use a _is_running variable? (https://stackoverflow.com/questions/4541190/how-to-close-a-thread-from-within)

    def play_sound(self, **kwargs):
        # Default values
        frequency = self.Frequency
        duration = self.Duration
        volume = self.DutyCycle
        kill_thread = True
        # User-specific input overide
        for item_name, value in kwargs.items():
            if item_name.lower() == 'frequency':
                frequency = value
            elif item_name.lower() == 'duration':
                duration = value
            elif item_name.lower() == 'volume':
                volume = value
            elif item_name.lower() == 'threaded':
                if value == False:
                    kill_thread = False
        # Starting thread for buzzer
        thread = threading.Thread(target=self.start_sound, kwargs={'frequency':frequency,'duration':duration,'volume':volume,'threaded':kill_thread}, daemon=True)
        thread.start()

    def stop_buzzer(self):
        GPIO.cleanup()

###################################
## TEST WHEN CALLING THIS SCRIPT ##
###################################
if __name__ == '__main__':
    debug=True
    if debug:
        buzzer = BuzzerControl(debug=debug)
        buzzer.setup()
        time.sleep(1)
        print('Playing "normal" sound')
        buzzer.start_sound()

        # print('Funky stuff...')
        # buzzer.start_sound(frequency=440,duration=1, volume=75)
        # buzzer.start_sound(frequency=880,duration=1, volume=25)
        # buzzer.start_sound(frequency=2000,duration=1, volume=50)

        print('Testing thread')
        buzzer.play_sound()
        time.sleep(8)

        print('End of test.')
        #GPIO.cleanup()