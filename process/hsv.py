import cv2
import numpy

class hsv:
   def __init__(self, hsv_low, hsv_high):
      self.hsv_low = numpy.array((hsv_low[0], hsv_low[1], hsv_low[2]), dtype=numpy.uint8, ndmin=1)
      self.hsv_high = numpy.array((hsv_high[0], hsv_high[1], hsv_high[2]), dtype=numpy.uint8, ndmin=1)

   def filterHSV(self, img):
      #print "Filtering image to " + `self.hsv_low` + " -> " + `self.hsv_high` 
      return cv2.inRange(img, self.hsv_low, self.hsv_high)

