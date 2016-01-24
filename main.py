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
         img2 = cv2.GaussianBlur(img2, (5,5), 0)
         #img3 = cv2.GaussianBlur(img, (5,5), 0)
         #img2 = cv2.Canny(img2, 100, 200)
         contours, _ = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
         contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
         biggest_area = -1
         biggest = None
         biggest_xy1 = 0,0
         biggest_xy2 = 0,0
         biggest2_area = -1
         biggest2 = None
         biggest2_xy1 = 0,0
         biggest2_xy2 = 0,0
         for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01*perimeter, True)
            print "Looking at " + `len(approx)`
            x,y,w,h = cv2.boundingRect(contour)
            aspect = float(w)/float(h)
            print "x: " + `x` + " y: " + `y` + " w: " + `w` + " h: " + `h` + " a: " + `aspect`
            if len(approx) == 8:
               if w*h > biggest_area:
                  biggest2_area = biggest_area
                  biggest2 = biggest
                  biggest2_xy1 = biggest_xy1
                  biggest2_xy2 = biggest_xy2

                  biggest_area = w*h
                  biggest = approx
                  biggest_xy1 = (x-5,y-5)
                  biggest_xy2 = (x+w+5,y+h+5)
               else:
                  if w*h >= biggest2_area:
                     biggest2_area = w*h
                     biggest2 = approx
                     biggest2_xy1 = (x-5,y-5)
                     biggest2_xy2 = (x+w+5,y+h+5)
#            if len(approx) == 8:
         print "Biggest is " + `biggest`
         print "Biggest2 is " + `biggest2`
         if biggest != None:
            cv2.rectangle(frame, biggest_xy1, biggest_xy2, (255,0,0), 2)
         if biggest2 != None:
            cv2.rectangle(frame, biggest2_xy1, biggest2_xy2, (255,255,255), 2)
         print "Running HSV filter"
         print "Running glyph tracking"
         print "Outputting x of y"
         fps = int(round(1000/((time.time()-millis2)*1000)))
         print "Loop bottom " + `fps`
         if type == "camStill" or type == "camStream":
            camera.rawCapture.truncate(0)
         if config.writeFrame:
            imageWriter.write(frame)



m = main()
m.main()
