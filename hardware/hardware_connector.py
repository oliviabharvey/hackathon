import random

from hardware.led_control import LEDs
from hardware.buzzer_control import BuzzerControl
from hardware.motor_control import MotorControl
from hardware.ir_control import IrLed
from hardware.camera_control import CameraControl

class HardwareConnector():
    """
    Enables interfacting with the various sensors/actuators (except touch screen).
    """

    def __init__(self, debug=False):
        self.debug = debug

        # Initializing LEDs
        self.leds = LEDs(debug=self.debug)
        self.leds.setup()

        # Initializing buzzer
        self.buzzer = BuzzerControl(debug=self.debug)
        self.buzzer.setup()

        # Initializing motor
        self.motor = MotorControl(debug=self.debug)
        self.motor.setup()

        # Initializing IR beam (food tray)
        self.irb = IrLed(debug=self.debug)
        self.irb.setup()

        # Initializing Camera
        self.camera = CameraControl(debug=self.debug)
        self.camera.setup()



    def is_irb_broken(self) -> bool:
        """
        Starting the infrared beam (IRB) and waiting until the beam is broken. Once beam is broken, turn off tray light.

        Outputs:
            - ir_break: Returns True once the beam has been broken.
        """
        if self.debug: 
            ir_break = False
            if random.uniform(0, 1) >= 0.95:
                ir_break = True
            return ir_break
        else: 
            ir_break = self.irb.start_irb()
            self.turn_tray_light_off()
            return ir_break

    def play_tone(self, duration: float):
        """
        Play a buzzer tone for a fixed duration (in seconds).
        """
        # Start playing tone for duration. Asynchronous.
        self.buzzer.play_sound(time=duration)
        return

    def turn_tray_light_on(self):
        """
        Turn on the food tray light.

        Outputs:
            - self.leds.tray_led.light_on(): Return light status. True = On; False = Off
        """
        return self.leds.tray_led.light_on()

    def turn_tray_light_off(self):
        """
        Turn off the food tray light.

        Outputs:
            - self.leds.tray_led.light_off(): Return light status. True = On; False = Off
        """
        return self.leds.tray_led.light_off()

    def turn_experiment_light_on(self):
        """
        Turn on the experiment light. 
        This is an outside light to have a visual indicator that an experience is ongoing.

        Outputs:
            - self.leds.experience_led.light_on(): Return light status. True = On; False = Off
        """
        return self.leds.experience_led.light_on()

    def turn_experiment_light_off(self):
        """
        Turn off the experiment light. 
        This is an outside light to have a visual indicator that an experience is ongoing.

        Outputs:
            - self.leds.experience_led.light_off(): Return light status. True = On; False = Off
        """
        return self.leds.experience_led.light_off()

    def squeeze_syringe(self, qty: int):
        """
        Provide a reward by squeezing the syringe.

        Inputs:
            - qty: Quantity volume (in microliter) of reward to provide.
        """
        # Turn motor to provide a given qty of fluid (in microliter) in food tray. Asynchronous.
        self.motor.provide_reward(microliter=qty)
        return

    def start_camera(self, videoname: str = None):
        """
        Start video camera.

        Inputs:
            - videoname: If a video name is provided, this name will be used. If not, the current datetime will be used.
        """
        self.camera.start(self, videoname)

    def stop_camera(self):
        """
        Stops the video camera and returns the name of the file.

        Outputs:
            - videoname: The name of the video output file.
        """
        videoname = self.camera.stop()
        return videoname


    def stop_hardware(self):
        """
        Reset and stop all hardware components controlled by the hardward connector.
        To be call at the very end of an experiment as all hardward will become unresponsive until next initialization.
        """
        # Ending hardware appropriately
        self.motor.reset_position() #  Reset motor to initial position
        # Stopping hardware approriately
        self.leds.stop_leds()
        self.motor.stop_motor()
        self.irb.stop_ir()
        self.leds.gpio_cleanup()
        self.camera.cleanup()
        
