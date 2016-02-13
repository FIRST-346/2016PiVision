from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

class camera:
   def __init__(self, resolution, shutter):
         self.camera = PiCamera()
         self.camera.resolution = resolution
         self.camera.exposure_compensation = 0
         self.camera.exposure_mode = 'off'
#         self.camera.exposure_speed = 1
         self.camera.shutter_speed = shutter
         self.rawCapture = PiRGBArray(self.camera, size=resolution)
         print "Warming up"
         time.sleep(0.1)
         self.init = True

   def getImage(self):
      return self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)

print "camStream imported"
