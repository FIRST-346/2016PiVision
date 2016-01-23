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
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import time
import cv2

#Internal libs
#from input import camStill
#from input import camStream
from input import diskStill
from config import fileConfig
from process import hsv
from output import file

class main:
   def getInput(self, type, resolution, config):
      if type == "camStill":
         return camStill.camera(resolution)
      if type == "camStream":
         return camStream.camera(resolution)
      if type == "diskStill":
         return diskStill.camera(resolution, config.imageStillPathIn)

   def main(self):
      print "Entering main"
      print "Reading file config"
      config = fileConfig.config()
      
      print "Looking for net config for 5s"
     

      camera = self.getInput(config.input,config.captureResolution, config)
      filter = hsv.hsv(config.hsv_low, config.hsv_high)

      imageWriter = file.stillImage(config.imageStillPathOut)
      print "Entering main loop"

      frames = 0
      millis = time.time()
      for frame in camera.getImage():
         millis2 = time.time()
         #time.sleep(0.1)
         frames = frames + 1
         print "Main loop start"
         print "Getting input image " + `frames`
	 img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
         print "Applying filter x of y"
         img2 = filter.filterHSV(img)
         print "Running HSV filter"
         print "Running glyph tracking"
         print "Outputting x of y"
         fps = int(round(1000/((time.time()-millis2)*1000)))
         print "Loop bottom " + `fps`
         if type == "camStill" or type == "camStream":
            camera.rawCapture.truncate(0)
         if config.writeFrame:
            imageWriter.write(img2)



m = main()
m.main()
