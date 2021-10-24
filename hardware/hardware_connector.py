import random
#import led_control
#import buzzer_control
#import motor_control
#import ir_control

class HardwareConnector():
    """
    Enables interfacting with the various sensors/actuators (except touch screen).
    """

    def __init__(self, debug=False):
        self.debug = debug

        # Initializing LEDs
        """self.leds = led_control.LEDs(debug=self.debug)
        self.leds.setup()

        # Initializing buzzer
        self.buzzer = buzzer_control.BuzzerControl(debug=self.debug)
        self.buzzer.setup()

        # Initializing motor
        self.motor = motor_control.MotorControl(debug=self.debug)
        self.motor.setup()

        # Initializing IR beam (tray)
        self.ir = ir_control.IrLed(debug=self.debug)
        self.ir.setup()"""




    def is_irb_broken(self):
        # return True if infrared beam is broken, False otherwise
        if self.debug: 
            ir_break = False
            if random.uniform(0, 1) >= 0.95:
                ir_break = True
            return ir_break
        else: 
            return False

      #  self.ir.is_irb_broken

    def play_tone(self, duration):
        # start playing tone for duration, but do not wait for it to be finished
        # to continue (needs to be asynchronous)
        #self.buzzer.play_sound(self, time=duration)
        return

    def turn_tray_light_on(self):
        #self.leds.tray_led.light_on()
        return

    def turn_tray_light_off(self):
        #self.leds.tray_led.light_off()
        return

    def squeeze_syringe(self, qty):
        # turn motor to provide a given qty of fluid (in microliter) in food tray.
        # This probably needs to be asynchronous.
        #self.motor.provide_reward(microliter=qty)
        return

    """def stop_hardware(self):
        # Ending hardware appropriately
        self.motor.reset() #  Reset motor to initial position
        # Stopping hardware approriately
        self.leds.stop_leds()
        self.buzzer.stop_buzzer()
        self.motor.stop_motor()
        self.ir.stop_ir()
    """