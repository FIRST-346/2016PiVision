import time
import cv2

class camera:
   def __init__(self, resolution):
         self.resolution = resolution
         print "Warming up"
         time.sleep(0.1)
         self.init = True

   def getImage(self):
     print "Getting image from file"
     self.image = cv2.imread("/tmp/test_in.png")
     return [ self.image ]

print "camStill imported"
