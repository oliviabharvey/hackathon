import RPi.GPIO as GPIO  # pip install RPi.GPIO
import lirc # pip install lirc - LIRC should be install on system (sudo apt-get install lirc)
"""
1.add to LIRC GPIO connection:
`sudo nano /etc/modules`
Add these 2 lines:
`lirc_dev`
`lirc_rpi gpio_in_pin=18 gpio_out_pin=17` Make sure you match to LED/RECEIVER PINS
2.Then modify:
`sudo nano /etc/lirc/hardware.conf`
Add these 3 lines:
`DRIVER="default"`
`DEVICE="/dev/lirc0"`
`MODULES="lirc_rpi"`
3.Reboot your Pi.
4.Add a remote/key combo. (This will be hardcoded once done. TODO!)
"""
import time
import threading

# TODO: Test Infrared script to confirm activation / stop



class IrLed:
    """
    Enabling control of the infrared LED at 38kHz
    """

    def __init__(self, debug=False, lirc_remote='Remote', lirc_key='Key'):
        self.debug = bool(debug)
        self.ir_led_pin = 11 # Physical location (GPIO pin# 17)
        self.ir_sensor_pin = 12 # Physical location (GPIO pin# 18)
        self.lirc_client = lirc.Client()
        self.lirc_remote = lirc_remote
        self.lirc_key = lirc_key 
        self.state = False  # Beam connected = True, Broken =  False
        self.max_state_trigger = 5  # After X refresh rate (default 10Hz, 5step -> 500ms), confirms the mouse is in place
        self.irb_broken_counter = 0
        self.irb_complete_counter = 0
        self.is_irb_broken = False  # Beam disrupted trigger (mouse is there)
        if self.debug:
            print(self.client.version())
            print(self.lirc_remote)
            print(self.lirc_key)

    def setup(self):
        # Setup Receiver
        GPIO.setmode(GPIO.BOARD)    # Numbers GPIOs by physical location
        # GPIO.setmode(GPIO.BCM)    # Numbers GPIOs by GPIO
        GPIO.setup(self.ir_sensor_pin, GPIO.IN)
        # Start sending IR
        client.send_start(self.lirc_remote, self.lirc_key)
        # Update state
        self.is_irb_broken = False
        self.state = False
        
    
    def check_beam_status(self):
            while not(self.is_irb_broken):
                time.sleep(0.100) # 10Hz refresh rate
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
        return self.is_irb_broken


    def stop_ir(self):
        client.send_stop(self.lirc_remote, self.lirc_key)
        GPIO.cleanup()

    def listener_beam(self):
        thread = threading.Thread(target=self.check_beam_status, args=(), deamon=True)
        thread.start()



client.send_stop()

"""
client.simulate()
Simulate an IR event.

The --allow-simulate command line option to lircd must be active for this command not to fail.
"""