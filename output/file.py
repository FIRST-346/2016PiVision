import cv2

class stillImage:
   def __init__(self, path):
      self.path = path

   def write(self,image):
      cv2.imwrite(self.path, image)

class stillImageWriter:
   def write(self, image, path):
      cv2.imwrite(path, image)

class imageStreamer:
   def __init__(self, path,size):
      self.path = path
      fourcc = cv2.cv.CV_FOURCC(*'XVID')
      self.writer = cv2.VideoWriter(path, fourcc, 4.0, size)

   def writeFrame(self, image):
      self.writer.write(image)
