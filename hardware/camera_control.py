import os
import threading
import time 

import RPi.GPIO as GPIO  # pip install RPi.GPIO
from picamera import PiCamera   # pip install picamera

# TODO:

class CameraControl:
    """
    Enables interfacing with the camera.
    """
    def __init__(self, debug: bool = False):
        self.camera = PiCamera()
        self.videoname = 'test.h264'
        self.debug = bool(debug)


    def setup(self):
        self.camera.sensor_mode = 6
        # self.camera.resolution = 1280,720
        # self.camera.framerate = 25
        self.camera.rotation = 0
        self.camera.hflip = False
        self.camera.vflip = False
        # time.sleep(2) #Camera warm-up time

    def start_recording(self, videoname: str = None):
        if videoname:
            self.videoname = videoname
        self.camera.start_recording(output=self.videoname, format='h264', bitrate=7500000)


    def stop_recording(self):
        self.camera.stop_recording()

    def reset(self):
        self.camera.close()

    def get_mp4(self):
        time.sleep(1)
        os.system('ffmpeg -r 42 -i '+self.videoname+' -c copy '+self.videoname+'.mp4')
        time.sleep(1)
        os.system('rm -f ./' + self.videoname)

"""
When calling this script directly, a small unit test (defined below) is run for debugging purposes.
"""
###################################
## TEST WHEN CALLING THIS SCRIPT ##
###################################
if __name__ == '__main__':
    debug=True
    if debug:
        camera = CameraControl(debug=debug)
        camera.setup()
        camera.start_recording(videoname='test')
        start = time.time()
        camera.camera.wait_recording(10)
        end = time.time()
        print('Time:')
        print(end - start)
        camera.stop_recording()
        camera.reset()
        camera.get_mp4()
    

192.168.0.21