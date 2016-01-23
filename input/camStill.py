from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

class camera:
   def __init__(self, resolution):
         self.camera = PiCamera()
         self.camera.resolution = resolution
         self.rawCapture = PiRGBArray(self.camera, size=resolution)
         print "Warming up"
         time.sleep(0.1)
         self.init = True

   def getImage(self):
     print "Getting camera image"
     self.rawCapture.truncate(0)
     self.camera.capture(self.rawCapture, format="bgr")
     self.image = self.rawCapture.array
     return [ self.image ]

print "camStill imported"
