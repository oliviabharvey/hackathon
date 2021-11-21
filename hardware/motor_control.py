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

    def __init__(self, StepDirection=1, WaitTime=3/1000, debug=False, motor_verbose=False):
        self.debug = bool(debug)
        self.motor_verbose = bool(motor_verbose) # That's a lot of output. Set to true only if error driving GPIO pins.
        self.motorPins = (15, 16, 18, 22)  # Physical location (GPIO pin# 22,23,24,25)
        # Define motor step sequence (datasheet)
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
        self.MaxPinSequence = len(self.PinSequence)
        self.CurrentStep = 0
        self.FullRotationCounter = 0
        self.TotalStepCounter = 0
        # Set to 1 (slower - more torque) or 2 (faster - less torque) for clockwise
        # Set to -1 or -2 for anti-clockwise
        self.StepDirection = int(StepDirection)
        # Motor protection
        if (abs(self.StepDirection) > 2) or (self.StepDirection==0):
            pass
            # RAISE ERROR / sys.exit()


    def setup(self):
        #Initialization of pins
        GPIO.setmode(GPIO.BOARD)    # Numbers GPIOs by physical location
        # GPIO.setmode(GPIO.BCM)    # Numbers GPIOs by GPIO
        for pin in self.motorPins:
                GPIO.setup(pin,GPIO.OUT)
                GPIO.output(pin,GPIO.LOW)
        #Initialization of variables (Should force a reset for these values to work)
        self.CurrentStep = 0
        self.FullRotationCounter = 0
        self.TotalStepCounter = 0
        sys.stdout.write('\nMotor initialized')


    def single_step(self,StepDirection=None):
        if StepDirection == None:
            StepDirection = self.StepDirection

        # Make a single (smallest) motor step
        if self.debug:
            if self.motor_verbose:
                sys.stdout.write("\nCurrent Step: " + str(self.CurrentStep))  # Number of PinSequence 
                sys.stdout.write("\nCurrent Pin Sequence: " + str(self.PinSequence[self.CurrentStep]))  # Current pin matrix
                sys.stdout.write("\nNumber of Steps: " + str(self.TotalStepCounter))  # Current pin matrix
                sys.stdout.write("\nNumber of Full Rotation: " + str(self.FullRotationCounter))
            
        self.TotalStepCounter += StepDirection
        self.CurrentStep = self.TotalStepCounter % self.MaxPinSequence  # Modulo of TotalStepCounter gives next step
        self.FullRotationCounter = self.TotalStepCounter // self.MaxPinSequence # Floor division of TotalStepCounter gives next step


        # Turning on/off appropriate pins for the step
        for pin in range(0, 4):
            gpio_pin = self.motorPins[pin]
            if self.PinSequence[self.CurrentStep][pin]!=0:
                if self.debug:
                    if motor_verbose:
                        sys.stdout.write('\nEnable GPIO# ' + str(gpio_pin))
                GPIO.output(gpio_pin, GPIO.HIGH)
            else:
                GPIO.output(gpio_pin, GPIO.LOW)
        # The motor can only take an input every 3ms
        time.sleep(self.WaitTime)
    
        return self.TotalStepCounter


    def full_rotation(self,StepDirection=None):
        if StepDirection == None:
            StepDirection = self.StepDirection
        # Make one full motor rotation
        if self.debug:
            sys.stdout.write('One full motor rotation - Direction: ', StepDirection)
        nb_steps_full = 4096  # 512 times the 8 sequence steps
        if abs(StepDirection) == 2:
            step_to_rotation = int(nb_steps_full/2)
        else:
            step_to_rotation = int(nb_steps_full)
        for i in range(0,step_to_rotation): # MAYBE A WHILE?
            self.single_step(StepDirection)


    def microliter(self, microliter, StepDirection=None):
        # How many turn/step for a microliter
        if StepDirection == None:
            StepDirection = self.StepDirection
        self.full_rotation(2)
        self.full_rotation(-2)
        sys.exit()

    def provide_reward(self, microliter, StepDirection=None):
        if StepDirection == None:
            StepDirection = self.StepDirection
        # Provide the number of microliter as a reward
        thread = threading.Thread(target=self.microliter, args=(microliter,), daemon=False)
        thread.start()


    def reset(self,StepDirection= None):
        if StepDirection == None:
            StepDirection= - self.StepDirection
        # To call at the end of experience to inverse all motor movement
        for i in range(0,self.TotalStepCounter): # MAYBE A WHILE?
            self.single_step(self,StepDirection)

    def stop_motor(self):
        for pin in range(0, 4):
            gpio_pin = self.motorPins[pin]
            GPIO.output(gpio_pin, GPIO.LOW)

    def gpio_cleanup():
        GPIO.cleanup()

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
        sys.stdout.write('\nTesting provide reward')   
        motor.provide_reward(100)

        sys.stdout.write('\nEnd of test.')
        # removed gpio cleanup 
        GPIO.cleanup()