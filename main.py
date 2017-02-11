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
import numpy as np

#Internal libs
#from input import camStill
#from input import camStream
from input import diskStill
from config import fileConfig
from config import netConfig
from process import hsv
from output import file

import sys
from networktables import NetworkTable


class main:
   def rotate(self, l, x):
      return l[-x:] + l[:-x]

   def findBounds(self, points):
      #Find Centroid
      #Find 4 points with longest distance from centroid
      x = 1
      

   def getInput(self, type, resolution, config):
      if type == "camStill":
         return camStill.camera(resolution)
      if type == "camStream":
         return camStream.camera(resolution, config.shutter)
      if type == "diskStill":
         return diskStill.camera(resolution, config.imageStillPathIn)

   def main(self):
      # Focal length, sensor size (mm and px)
      f = 3.6 # mm
      pix_width = 640.0 # sensor size has 2592px in width
      pix_height = 480.0 # sensor size has 1944px in width
      sensor_width = 3.67 # mm
      sensor_height = 2.74 # mm
      
      # set center pixel
      u0 = int(pix_width / 2.0)
      v0 = int(pix_height / 2.0)
      
      # determine values of camera-matrix
      mu = pix_width / sensor_width # px/mm
      alpha_u = f * mu # px
      
      mv = pix_height / sensor_height # px/mm
      alpha_v = f * mv # px
      
      # Distortion coefs 
      D = np.array([[0.0, 0.0, 0.0, 0.0]])
      
      # Camera matrix
      K = np.array([[alpha_u, 0.0, u0], 
                    [0.0, alpha_v, v0],
                    [0.0, 0.0, 1.0]])
#TODO: Recalculate this to be from the final position on the robot eg if the camera is looking up it will appear trapizodial!
      target_obj = np.array ([[-0.833,-0.5,0], #Outer Top Left
                             [-0.666,-0.5,0], #Inner Top Left
                             [-0.666,0.333,0], #Inner Bottom Left
                             [0.666,0.333,0], #Inner Bottom Right
                             [0.666,-0.5,0], #Inner Top Right
                             [0.833,-0.5,0], #Outer Top Right
                             [0.833,0.5,0], #Outer Bottom Right
                             [0.833,-0.5,0]], dtype='f') #Outer Bottom Left
      #target_obj = np.array([[-0.833, -0.5, 0],
      #                      [-0.833, 0.5, 0],
      #                      [0.833, 0.5, 0],
      #                      [0.833, -0.5, 0]])
      print "Entering main"
      print "Reading file config"
      config = fileConfig.config()
      
      #Network table
      NetworkTable.setIPAddress(config.ip)
      NetworkTable.setClientMode()
      NetworkTable.initialize()

      sd = NetworkTable.getTable("SmartDashboard")

      netConf = netConfig.config(config,sd)

      print "Looking for net config for 5s"
     

      camera = self.getInput(config.input,config.captureResolution, config)
      filter = hsv.hsv(config.hsv_low, config.hsv_high)

      imageWriter = file.stillImage(config.imageStillPathOut)
      imageWriter2 = file.stillImage(config.imageStillPathOut2)
      imageWriter3 = file.stillImage(config.imageStillPathOut3)
      print "Entering main loop"

      frames = 0
      millis = time.time()
      for f in camera.getImage():
         millis2 = time.time()
         if config.input == "camStream":
            frame = f.array
         else:
            frame = f
         #time.sleep(0.1)
         frames = frames + 1
         #print "Main loop start"
        # print "Getting input image " + `frames`
	 img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
         #print "Applying filter x of y"
         img2 = filter.filterHSV(img)
         if config.writeFrame:
            imageWriter2.write(img2)
         img3 = cv2.GaussianBlur(img2, (7,7), 0)
         img2 = cv2.GaussianBlur(img2, (7,7), 0)
         #img2 = cv2.Canny(img2, 100, 200)
         #imageWriter.write(img2)
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
            if cv2.isContourConvex(approx):
               #print "Contour is convex"
               continue
            x,y,w,h = cv2.boundingRect(contour)
            aspect = float(w)/float(h)
            area = cv2.contourArea(approx)
            if len(approx) == 8 and not(area <  config.minArea):
               #print "Area is " + `area` + " " + `cv2.isContourConvex(approx)` + " " + `not(cv2.isContourConvex(approx))`
               
               if w*h > biggest_area:
                  biggest_area = w*h
                  biggest = approx
                  biggest_xy1 = (x-5,y-5)
                  biggest_xy2 = (x+w+5,y+h+5)
              
 
         if biggest != None:
            cv2.rectangle(frame, biggest_xy1, biggest_xy2, (255,0,0), 2)
            cv2.drawContours(frame, biggest, -1, (0,255,0), 3)
            moments = cv2.moments(biggest);
            centroidx = int(moments['m10']/moments['m00'])
            centroid = (centroidx , int(moments['m01']/moments['m00']) )
            cv2.circle(frame, centroid, 5, (255,255,255))
#            hull = cv2.convexHull(biggest)
            hullr = np.zeros((len(biggest), 2), np.float32)

            cv2.drawContours(frame, biggest, -1, (255,0,0), 10)

            i = 0
            dir = 1

            if biggest[0][0][0] > centroidx:
               print "First point is the top right need to flip our pointses" + `biggest[0][0]`
               i = 3
            
            for pt in biggest:
               hullr[i] = pt[0]
               i = i + dir
               if i >= len(hullr):
                  i = 0
               if i < 0:
                  i = len(hullr)-1

            print `hullr`            
            if hullr[7][1] < hullr[1][1]:
               print "We need to flip our elements except point 0"
               first = hullr[:1]
               print "Point 0: " + `first`
               rest = hullr[1:][::-1]
               print "And the rest: " + `rest`
               hullr = np.append(first,rest, axis=0)
               print "And it all back together: " + `hullr`
#               hullr = hullr[0]+hullr[:8][::-1]


          

            
            if len(hullr) == len(target_obj):
#               print "Solving for: " + `target_obj`
#               print `hullr`
               retval, rvec, tvec = cv2.solvePnP(target_obj, hullr, K, D)
               cv2.circle(frame, (hullr[0][0], hullr[0][1]), 5, (255,255,255))
               cv2.circle(frame, (hullr[1][0], hullr[1][1]), 5, (0,0,255))
               cv2.circle(frame, (hullr[1][0], hullr[1][1]), 7, (0,0,255))
               cv2.circle(frame, (hullr[7][0], hullr[7][1]), 5, (0,255,0))
               cv2.circle(frame, (hullr[7][0], hullr[7][1]), 7, (0,255,0))
               cv2.circle(frame, (hullr[7][0], hullr[7][1]), 9, (0,255,0))
               print `retval` + " => " + `rvec` + " => " + `tvec`
            else:
               print "Target has more points then target! " + `len(hullr)` 
               cv2.drawContours(frame, biggest, -1, (0,255,255), 3)
               imageWriter.write(frame)
               imageWriter2.write(img3)
         
#         if biggest2 != None:
#            cv2.rectangle(frame, biggest2_xy1, biggest2_xy2, (255,255,255), 2)
#            cv2.drawContours(frame, biggest2, -1, (0,0,255), 3)
#TODO: Determine the outermost points
#TODO: Determine the orientation of the points

         fps = int(round(1000/((time.time()-millis2)*1000)))
         print "Loop bottom " + `fps`
         if config.input == "camStill" or config.input == "camStream":
            #print "Clearing buffer"
            camera.rawCapture.truncate(0)
         if config.writeFrame:
            imageWriter.write(frame)



m = main()
m.main()
