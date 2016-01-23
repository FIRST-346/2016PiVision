import time
import cv2


class camera:
   def __init__(self, resolution, path):
         self.resolution = resolution
         self.path = path
         print "Warming up"
         time.sleep(0.1)
         self.init = True

   def getImage(self):
     print "Getting image from file"
     self.image = cv2.imread(self.path)
     return [ self.image ]

print "camStill imported"
