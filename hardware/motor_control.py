import RPi.GPIO as GPIO  # pip install RPi.GPIO
import time 

# TODO: Test motor/script to confirm activation / reset
# TODO: Measure microliter per turn/step and create a function that calls the motor per microliter.


class motor_control:
    """
    Enables interfacting with the motor.
    """

    def __init__(self, StepDirection=1, WaitTime=4, debug=False):
        self.debug = bool(debug)
        self.motorPins = (12, 16, 18, 22)  # Physical location (GPIO pin# 18,23,24,25)
        # Define motor step sequence as shown in manufacturers datasheet
        self.PinSequence =   [[1,0,0,1],
                             [1,0,0,0],
                             [1,1,0,0],
                             [0,1,0,0],
                             [0,1,1,0],
                             [0,0,1,0],
                             [0,0,1,1],
                             [0,0,0,1]]

        self.WaitTime = int(WaitTime)  #In ms -> 3ms minimum
        self.MaxPinSequence = len(self.PinSequence)
        self.CurrentStep = 0
        self.FullRotationCounter = 0
        self.TotalStepCounter = 0
        # Set to 1 (slower - more torque) or 2 (faster - less torque) for clockwise
        # Set to -1 or -2 for anti-clockwise
        self.StepDirection = int(StepDirection)
        # Motor protection
        if (abs(self.StepDirection) > 2) or (self.StepDirection==0):
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
        print ('Motor initialized')


    def single_step(self,StepDirection=self.StepDirection):
        if self.debug:
        print ("Current Step: ",self.CurrentStep)  # Number of PinSequence 
        print ("Current Pin Sequence: ",self.PinSequence[CurrentStep])  # Current pin matrix
        print ("Number of Steps: ",self.TotalStepCounter)  # Current pin matrix
        print ("Number of Full Rotation: ",self.FullRotationCounter)
        
        self.TotalStepCounter += StepDirection
        self.CurrentStep = self.TotalStepCounter % self.MaxPinSequence  # Modulo of TotalStepCounter gives next step
        self.FullRotationCounter = self.TotalStepCounter // self.MaxPinSequence # Floor division of TotalStepCounter gives next step


        # Turning on/off appropriate pins for the step
        for pin in range(0, 4):
        pin = self.motorPins[pin]
        if self.PinSequence[self.CurrentStep][pin]!=0:
            if self.debug:
            print " Enable GPIO %i" %(pin)
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)
        # The motor can only take an input every 3ms
        time.sleep(self.WaitTime)
    
    return self.TotalStepCounter

    def full_rotation(self,StepDirection=self.StepDirection):
        if abs(StepDirection) == 2
        step_to_rotation = 4
        else step_to_rotation = 8
        for i in range(0,step_to_rotation): # MAYBE A WHILE?
        single_step(self,StepDirection)

    def reset(self,StepDirection= -self.StepDirection): # To call at the end of experience
        for i in range(0,self.TotalStepCounter): # MAYBE A WHILE?
        self.single_step(self,StepDirection)

###################################
## TEST WHEN CALLING THIS SCRIPT ##
###################################
if __name__ == '__main__':
    debug=True
    if debug:
        motor = motor_control(debug=debug)
        motor.setup()

        print('Turning clockwise slow - 8 steps, 1 full turn...')
        for i in range(0,8): # MAYBE A WHILE?
            motor.single_step(1)
            time.sleep(1000)
        
        print('Turning clockwise fast - 4 steps, 1 full turn...')
        for i in range(0,4): # MAYBE A WHILE?
            motor.single_step(2)
            time.sleep(1000)
        
        print('Turning counterclockwise fast - 8 steps, 1 full turn...')
        for i in range(0,8): # MAYBE A WHILE?
            motor.single_step(-1)
            time.sleep(1000)
        
        print('Turning counterclockwise fast - 4 steps, 1 full turn...')
        for i in range(0,4): # MAYBE A WHILE?
            motor.single_step(-2)
            time.sleep(1000)

        print('Turning clockwise full turn - slow')
            motor.full_rotation(1)
            time.sleep(1000)

        print('Turning counterclockwise full turn - fast')
            motor.full_rotation(-2)
            time.sleep(1000)   

        print('End of test.')
        GPIO.cleanup()