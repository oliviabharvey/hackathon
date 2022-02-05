import threading
import time
import sys

import RPi.GPIO as GPIO  # pip install RPi.GPIO


class BuzzerControl:
    """
    Enabling control of the buzzer (frequency, duration and volume)
    """

    def __init__(self,frequency: int = 3000, duration: float = 5, DutyCycle: int = 10, debug: bool = False):
        self.debug = bool(debug) 
        # This pin needs to be PWM capable [(GPIO pin# 12,13,18,19])
        self.BuzzerPin = 32 # Physical location (GPIO pin# 12)
        self.DutyCycle = int(DutyCycle) # 0 to 100 - Volume
        self.Frequency = int(abs(frequency))  # Frequency (Hz)
        self.Duration = float(abs(duration))  # Sound duration (sec)
        self.Buzzer = None  # GPIO object to be loaded during setup

    def setup(self):
        """
        Setting pin output (physical pin connection) for buzzer connection.
        """
        GPIO.setmode(GPIO.BOARD)    # Numbers GPIOs by physical location
        # GPIO.setmode(GPIO.BCM)    # Numbers GPIOs by GPIO
        GPIO.setup(self.BuzzerPin, GPIO.OUT)
        self.Buzzer = GPIO.PWM(self.BuzzerPin, self.Frequency)
        sys.stdout.write('\n Buzzer initialized')
        
    
    def start_sound(self, **kwargs):
        """
        Send the signal (duration, frequency, etc.) to the buzzer as a new thread.
        If the kill_thread option is set to true, the thread will kill itself once the sound has been played.

        Inputs:
            - Keyword arguments are mainly for debugging, allowing to test various inputs after the object was initialized.
        """
        if self.debug:
            sys.stdout.write('\nPlaying sound')
        # Default values
        frequency = self.Frequency
        duration = self.Duration
        volume = self.DutyCycle
        kill_thread = False
        # User-specific input override from kwargs
        for item_name, value in kwargs.items():
            if item_name.lower() == 'frequency':
                frequency = value
            elif item_name.lower() == 'duration':
                duration = value
            elif item_name.lower() == 'volume':
                volume = value
            elif item_name.lower() == 'threaded':
                kill_thread = value
        
        # Sending the signal to the buzzer and killing thread after, if enabled.
        self.Buzzer.ChangeFrequency(frequency)
        self.Buzzer.start(volume)
        time.sleep(duration)
        self.Buzzer.stop()
        if kill_thread:
            if self.debug:
                sys.stdout.write('\nKilling buzzer thread now')
            sys.exit() # harsh solution, but easy to implement to kill thread.
            
    def play_sound(self, **kwargs):
        """
        Gouverning start_sound method to start as a new thread.

        Inputs:
            - Keyword arguments are mainly for debugging, allowing to test various inputs after the object was initialized.
        """
        # Default values
        frequency = self.Frequency
        duration = self.Duration
        volume = self.DutyCycle
        kill_thread = True
        # User-specific input override from kwargs
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
        buzzer = BuzzerControl(debug=debug)
        buzzer.setup()
        time.sleep(1)
        sys.stdout.write('\nPlaying "normal" sound')
        buzzer.start_sound()

        # print('Funky stuff...')
        # buzzer.start_sound(frequency=440,duration=1, volume=75)
        # buzzer.start_sound(frequency=880,duration=1, volume=25)
        # buzzer.start_sound(frequency=2000,duration=1, volume=50)

        sys.stdout.write('\nTesting thread')
        buzzer.play_sound()
        time.sleep(8)

        sys.stdout.write('\nEnd of test.')
        GPIO.cleanup()