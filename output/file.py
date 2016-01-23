import cv2

class stillImage:
   def __init__(self, path):
      self.path = path

   def write(self,image):
      cv2.imwrite(self.path, image);
