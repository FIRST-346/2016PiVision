import time
import cv2


class camera:
   def __init__(self, resolution, path):
         self.resolution = resolution
         self.path = path
         print "Warming up"
         time.sleep(0.1)
         self.init = True
         self.cap = cv2.VideoCapture(path)

   def getImage(self):
     return self.cap.read()

   def hasMore(self):
      return self.cap.isOpened()

print "camStill imported"
