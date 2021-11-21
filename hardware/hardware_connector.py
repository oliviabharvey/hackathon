import random
from hardware.led_control import LEDs
from hardware.buzzer_control import BuzzerControl
from hardware.motor_control import MotorControl
from hardware.ir_control import IrLed

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

        # Initializing IR beam (tray)
        self.ir = IrLed(debug=self.debug)
        self.ir.setup()


    def is_irb_broken(self):
        # return True if infrared beam is broken, False otherwise
        # pour l'instant, c'est à True le temps de voir ce qui se passe
        """if self.debug: 
            ir_break = False
            if random.uniform(0, 1) >= 0.95:
                ir_break = True
            return ir_break
        else: 
            return False"""

        self.ir.is_irb_broken

    def play_tone(self, duration):
        # start playing tone for duration, but do not wait for it to be finished
        # to continue (needs to be asynchronous)
        return self.buzzer.play_sound(time=duration)

    def turn_tray_light_on(self):
        return self.leds.tray_led.light_on()

    def turn_tray_light_off(self):
        return self.leds.tray_led.light_off()

    def squeeze_syringe(self, qty):
        # turn motor to provide a given qty of fluid (in microliter) in food tray.
        # This probably needs to be asynchronous.
        return self.motor.provide_reward(microliter=qty)

    def stop_hardware(self):
        # Ending hardware appropriately
        self.motor.reset() #  Reset motor to initial position
        # Stopping hardware approriately
        self.leds.stop_leds()
        self.buzzer.stop_buzzer()
        self.motor.stop_motor()
        self.ir.stop_ir()
