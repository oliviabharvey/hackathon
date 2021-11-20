import RPi.GPIO as GPIO  # pip install RPi.GPIO
from picamera import PiCamera   # pip install picamera
import threading
import time 

# TODO:

def CameraControl():
    """
    Enables interfacing with the camera.
    """
    def __init__(self, debug=False):
        return

    def setup(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.camera.rotation = 0
        self.camera.hflip = False
        self.camera.vflip = False
        time.sleep(0.1) #Camera warm-up time

    def start_recording(self, videoname, debug=False):
        self.camera.start_recording(output='videoname', format='h264', bitrate=2000000, quality=30)

    def stop_recording(self, debug=False):
        self.camera.stop_recording()

    def reset():
        camera.close()