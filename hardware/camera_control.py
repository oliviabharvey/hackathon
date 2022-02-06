import os
import threading
import time 
from datetime import datetime

import RPi.GPIO as GPIO  # pip install RPi.GPIO
from picamera import PiCamera   # pip install picamera

# Todo: Add to experiment  (start and end)
# Todo: Retrieve video to master and delete local puppet copy.


class CameraControl:
    """
    Enables interfacing with the camera.
    """
    def __init__(self, debug: bool = False, bitrate: int = 200000, hflip: bool = False, vflip: bool = False):
        self.debug = bool(debug)
        self.camera = PiCamera()
        self.bitrate = int(bitrate)
        self.format_out = 'mp4'
        self.format_cache = 'h264'
        self.rotation = 0
        self.hflip = bool(hflip)
        self.vflip = bool(vflip)



    def setup(self):
        """
        Initial setup of all the camera's setting.
        """
        self.camera.sensor_mode = 6 # Camera sensor mode (This (6) is 800x480 resolution)
        self.camera.rotation = self.rotation
        self.camera.hflip = self.hflip
        self.camera.vflip = self.vflip
        
    def start(self, videoname: str = None):
        """
        Start a recording a video.

        Inputs:
            - videoname: if a name is present, the video will be saved with that name. Otherwise current datetime will be used.
        """
        if videoname:
            self.videoname = videoname
        else:
            self.videoname = 'video_' + datetime.now().strftime('%Y%m%dT%H%M%S')
        self.camera.start_recording(output=self.videoname, format='h264', bitrate=self.bitrate)


    def stop(self):
        """
        Stop recording video and convert it to proper fps mp4 format.

        Outputs:
            - videoname: The name of the video output mp4 file.
        """
        self.camera.stop_recording()
        self.get_mp4() # Converting video to mp4, so it can be read easily from any deviceà
        return self.videoname+'.mp4'

    def cleanup(self):
        """
        Release camera resources once we're done using it.
        """
        self.camera.close()

    def get_mp4(self):
        """
        This methods convert a video (the lastest) to mp4 format, while setting proper framerate for video.
        Otherwise, video player think the framerate is 25fps, resulting in longer than reality videos.
        """
        framerate = 42  # This is the pi camera's default FPS
        time.sleep(1)
        os.system('ffmpeg -r '+str(framerate)+' -i '+self.videoname+' -c copy -y '+self.videoname+'.mp4')
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
        camera.start()
        camera.camera.wait_recording(10)
        camera.stop()
        camera.cleanup()
