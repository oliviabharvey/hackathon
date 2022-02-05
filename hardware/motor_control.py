import RPi.GPIO as GPIO  # pip install RPi.GPIO
import sys
import threading
import time
import sys

# TODO: Thread motor if need not to wait. (can be long)
# TODO: Measure microliter per turn/step and create a function that calls the motor per microliter.


class MotorControl:
    """
    Enables interfacing with the motor.
    """

    def __init__(self, StepDirection: int = 1, WaitTime: float = 3/1000, debug: bool = False, motor_verbose: bool = False):
        self.debug = bool(debug)
        self.motor_verbose = bool(motor_verbose) # That's a lot of output. Set to true only if error driving GPIO pins.
        self.motorPins = (15, 16, 18, 22)  # Physical location (GPIO pin# 22,23,24,25)
        # Define motor step sequence (from motor datasheet)
        self.PinSequence = [
            [1,0,0,1], 
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1]
            ]

        self.WaitTime = float(WaitTime)  #In seconds -> 3ms minimum
        if self.WaitTime  < 3/1000:
            self.WaitTime = 3/1000
        self.MaxPinSequence = len(self.PinSequence)
        self.CurrentStep = 0  # What is the current GPIO pin sequence to move the motor.
        self.FullSequence = 0  # How many full motor PinSequence were completed (clockwise and counterclockwise rotation cancel out)
        self.TotalStepCounter = 0  # How many steps were completed (clockwise and counterclockwise rotation cancel out)
        # Set to 1 (slower - more torque) or 2 (faster - less torque) for clockwise
        # Set to -1 or -2 for anti-clockwise
        self.StepDirection = int(StepDirection)
        # Motor protection from invalid inputs
        if self.StepDirection > 2:
            self.StepDirection = int(2)
        elif self.StepDirection < -2:
            self.StepDirection = int(-2)
        elif self.StepDirection==0:
            self.StepDirection = int(1)



    def setup(self):
        """
        Setting pin output (physical pin connection) for all 4 motor connectors.
        """
        #Initialization of pins
        GPIO.setmode(GPIO.BOARD)    # Numbers GPIOs by physical location
        # GPIO.setmode(GPIO.BCM)    # Numbers GPIOs by GPIO
        for pin in self.motorPins:
                GPIO.setup(pin,GPIO.OUT)
                GPIO.output(pin,GPIO.LOW)
        #Initialization of variables
        self.CurrentStep = 0
        self.FullSequence = 0
        self.TotalStepCounter = 0
        sys.stdout.write('\nMotor initialized')


    def single_step(self,StepDirection: int = None):
        """
        Moving the step motor by a single step. There are 4096 steps in one rotation.

        Inputs: 
            - StepDirection: Positive value (1 [slower] or 2 [faster]) for clockwise rotation, 
                             negative value (-1 [slower] or -2 [faster]) for anti-clockwise rotation
        Outputs:
            - self.TotalStepCounter: Current motor position, in motor steps (based on initial state of 0)
        """
        if StepDirection == None:
            StepDirection = self.StepDirection

        # Make a single (smallest) motor step
        if self.debug:
            if self.motor_verbose:
                sys.stdout.write("\nCurrent Step: " + str(self.CurrentStep))  # Number of PinSequence 
                sys.stdout.write("\nCurrent Pin Sequence: " + str(self.PinSequence[self.CurrentStep]))  # Current pin matrix
                sys.stdout.write("\nNumber of Steps: " + str(self.TotalStepCounter))  # Current pin matrix
                sys.stdout.write("\nNumber of Full Sequence completed " + str(self.FullSequence))
        self.TotalStepCounter += StepDirection
        self.CurrentStep = self.TotalStepCounter % self.MaxPinSequence  # Modulo of TotalStepCounter gives next step
        self.FullSequence = self.TotalStepCounter // self.MaxPinSequence # Floor division of TotalStepCounter gives next step

        # Turning on/off appropriate pins for the step
        for pin in range(0, 4):
            gpio_pin = self.motorPins[pin]
            if self.PinSequence[self.CurrentStep][pin]!=0:
                if self.debug:
                    if self.motor_verbose:
                        sys.stdout.write('\nEnable GPIO# ' + str(gpio_pin))
                GPIO.output(gpio_pin, GPIO.HIGH)
            else:
                GPIO.output(gpio_pin, GPIO.LOW)
        # The motor can only take an input every 3ms
        time.sleep(self.WaitTime)
    
        return self.TotalStepCounter


    def full_rotation(self,StepDirection: int = None):
        """
        Move the motor by a full turn. This method is based on the single_step method.

        Inputs: 
            - StepDirection: Positive value (1 [slower] or 2 [faster]) for clockwise rotation, 
                             negative value (-1 [slower] or -2 [faster]) for anti-clockwise rotation
        """
        if StepDirection == None:
            StepDirection = self.StepDirection
        # Make one full motor rotation
        if self.debug:
            sys.stdout.write('\nOne full motor rotation - Direction: ' + str(StepDirection))
        nb_steps_full = 4096  # 512 times the 8 sequence steps
        if abs(StepDirection) == 2:
            step_to_rotation = int(nb_steps_full/2)
        else:
            step_to_rotation = int(nb_steps_full)
        for i in range(0,step_to_rotation):
            self.single_step(StepDirection)


    def microliter(self, microliter: int, StepDirection: int = None, kill_thread: bool = True):
        """
        Send a number of microliter of liquid using the motor to push a syringe. 
        This function contains the calibration in variable `steps_per_uL`
        1 full motor turn (4096 steps) = X microliter.
        If this function is threaded, it can kill its thread once the motor as turned.

        Inputs:
            - microliter: The volume of liquid to provide
            - StepDirection: Positive value (1 [slower] or 2 [faster]) for clockwise rotation, 
                             negative value (-1 [slower] or -2 [faster]) for anti-clockwise rotation
            - kill_thread: If true, this function will kill its thread after liquid volume is delivered.
        """
        if StepDirection == None:
            StepDirection = self.StepDirection
        # How many turn/step for a microliter
        # This was not a exactly measure, but 1 turn (4096 steps) gives about 60uL.
        # To confirm
        steps_per_uL = 4096/60
        steps_for_qty = int(steps_per_uL * microliter)
        if abs(StepDirection) == 2:
            step_to_rotation = int(steps_for_qty/2)
        else:
            step_to_rotation = int(steps_for_qty)
        # iterator to rotate the motor a fixed amount of time
        for i in range(0,step_to_rotation):
            self.single_step(StepDirection)
        if kill_thread:
            if self.debug:
                sys.stdout.write('\nKilling motor thread now')
            sys.exit()

    def provide_reward(self, microliter: int,StepDirection:int = None, kill_thread: bool = True, daemon: bool = False):
        """
        Gouverning microliter method to start as a new thread. 

        Inputs:
            - microliter: The volume of liquid to provide
            - StepDirection: Positive value (1 [slower] or 2 [faster]) for clockwise rotation, 
                             negative value (-1 [slower] or -2 [faster]) for anti-clockwise rotation
            - kill_thread: If true, this function will kill its thread after liquid volume is delivered.
            - daemon: If true, this function will start as thread as daemon. 
                      This means that the sub-thread will abruptly end if the main thread ends.
        """
        if StepDirection == None:
            StepDirection = self.StepDirection
        # Provide the number of microliter as a reward
        thread = threading.Thread(target=self.microliter, args=(microliter,), daemon=daemon)
        thread.start()


    def reset_position(self,StepDirection: int = None):
        """
        Reset motor to initial position based on the total movement.

        Inputs: 
            - StepDirection: Positive value (1 [slower] or 2 [faster]) for clockwise rotation, 
                             negative value (-1 [slower] or -2 [faster]) for anti-clockwise rotation
        """
        sys.stdout.write('\nReseting motor to initial position...')
        if StepDirection == None:
            StepDirection = - self.StepDirection
        # To call at the end of experience to inverse all motor movement
        for i in range(0,self.TotalStepCounter): # MAYBE A WHILE?
            self.single_step(StepDirection=StepDirection)

    def stop_motor(self):
        """
        Stop motor by setting all GPIO pins voltage to 0.
        """
        for pin in range(0, 4):
            gpio_pin = self.motorPins[pin]
            GPIO.output(gpio_pin, GPIO.LOW)

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
        motor = MotorControl(debug=debug)
        motor.setup()
        time.sleep(1)
        sys.stdout.write('\nTurning clockwise slow - 8 steps')  #You will barely notice the motor move.
        for i in range(0,8): # MAYBE A WHILE?
            motor.single_step(1)

        sys.stdout.write('\nTurning clockwise full turn - slow')
        motor.full_rotation(1)
        time.sleep(1)

        sys.stdout.write('\nTurning counterclockwise full turn - fast')
        motor.full_rotation(-2)
        time.sleep(1)

        sys.stdout.write('\nTesting threaded motor')   
        motor.provide_reward(20)
        time.sleep(5) # Main waiting for thread to end (~5 sec per 20uL)

        sys.stdout.write('\nTesting position reset')
        motor.reset_position()

        sys.stdout.write('\nEnd of test.')
        # removed gpio cleanup 
        GPIO.cleanup()