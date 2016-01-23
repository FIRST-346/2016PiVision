"""
This will handle the main vision processing
The following steps will happen
1) Read Config
2) Main Loop
   a) Get image from input (configurable)
   b) Process image with opencv
   c) Output tracking info (and maybe an image) to the output (configurable)


"""
#External Libs
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#Internal libs
from input import camStill
from input import camStream
from config import fileConfig
from process import hsv


class main:
   def getInput(self, type, resolution):
      if type == "camStill":
         return camStill.camera(resolution)
      if type == "camStream":
         return camStream.camera(resolution)

   def main(self):
      print "Entering main"
      print "Reading file config"
      config = fileConfig.config()
      #Todo get this from config
      hsv_low = [0,0,0]
      hsv_high = [1,1,1]
      captureResolution = (640,480)
      captureType = "camStream"
      print "Looking for net config for 5s"
      camera = self.getInput(config.captureType,config.captureResolution)
      filter = hsv.hsv()
      print "Entering main loop"
      #Loop here
      frames = 0
      millis = time.time()
      for frame in camera.getImage():
         millis2 = time.time()
         #time.sleep(0.1)
         frames = frames + 1
         print "Main loop start"
         print "Getting input image " + `frames`
	 img = frame #camera.getImage()
         print "Applying filter x of y"
         img2 = filter.filterHSV(img, hsv_low, hsv_high)
         print "Running HSV filter"
         print "Running glyph tracking"
         print "Outputting x of y"
         fps = int(round(1000/((time.time()-millis2)*1000)))
         print "Loop bottom " + `fps`
         camera.rawCapture.truncate(0)



m = main()
m.main()
