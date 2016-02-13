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
import numpy as np

#Internal libs
#from input import camStill
from input import camStream
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
      if config.writeFrames:
         movie = file.imageStreamer('/tmp/out.avi',(640*3,480))
         movieIn = file.imageStreamer('/tmp/out_raw.avi', (640,480))

      print "Looking for net config for 5s"
     

      camera = self.getInput(config.input,config.captureResolution, config)
      filter = hsv.hsv(config.hsv_low, config.hsv_high)
      
      simpleImageWriter = file.stillImageWriter()

      print "Entering main loop"

      frames = 0
      millis = time.time()
      for f in camera.getImage():
         millis2 = time.time()
         if config.input == "camStream":
            frame = f.array
         else:
            frame = f

         frames = frames + 1
#Convert colorspace to hsv
	 img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#Filter the image
         hsvImg = filter.filterHSV(img)

         
#Blur the image
         blur = cv2.GaussianBlur(hsvImg, (7,7), 0)
         cont = blur.copy()
         contoursImg = frame.copy()
         result = frame.copy()
         #img2 = cv2.Canny(img2, 100, 200)
         #imageWriter.write(img2)
         contours, _ = cv2.findContours(cont, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
            cv2.rectangle(result, biggest_xy1, biggest_xy2, (255,0,0), 2)
            cv2.drawContours(contoursImg, biggest, -1, (0,255,0), 3)
            moments = cv2.moments(biggest);
            centroidx = int(moments['m10']/moments['m00'])
            centroid = (centroidx , int(moments['m01']/moments['m00']) )
            cv2.circle(result, centroid, 5, (255,255,255))
            hullr = np.zeros((len(biggest), 2), np.float32)

            i = 0
            dir = 1

#If the points start on the right we need to change the start index to be that of the left
            if biggest[0][0][0] > centroidx:
#TODO: If we are starting at the top right and the next point is the left of that then i needs to be 5 not 3
               if biggest[1][0][1] > biggest[7][0][1]:
                  i = 3
               else:
                  i = 5
            
            for pt in biggest:
               hullr[i] = pt[0]
               i = i + dir
               if i >= len(hullr):
                  i = 0
               if i < 0:
                  i = len(hullr)-1

#If the order is reversed we need to reverse points 1-7 while leaving 0 in place
#So if are points are 		[0,1,2,3,4,5,6,7] 
#we ned to reorder to be	[0,7,6,5,4,3,2,1]
#Alternativly we can just swap the target descriptor ... 

            if hullr[7][1] < hullr[1][1]:
#Get the first element
               first = hullr[:1]
#Get the rest of the elements and reverse them
               rest = hullr[1:][::-1]
#Recombine them
               hullr = np.append(first,rest, axis=0)


          

            
            if len(hullr) == len(target_obj):
               retval, rvec, tvec = cv2.solvePnP(target_obj, hullr, K, D)
               cv2.circle(result, (hullr[0][0], hullr[0][1]), 5, (255,255,255))
               cv2.circle(result, (hullr[1][0], hullr[1][1]), 5, (0,0,255))
               cv2.circle(result, (hullr[1][0], hullr[1][1]), 7, (0,0,255))
               cv2.circle(result, (hullr[7][0], hullr[7][1]), 5, (0,255,0))
               cv2.circle(result, (hullr[7][0], hullr[7][1]), 7, (0,255,0))
               cv2.circle(result, (hullr[7][0], hullr[7][1]), 9, (0,255,0))
               print `retval` + " => " + `rvec` + " => " + `tvec`

         
#Write the in frame if we are configured to do so
         if config.writeFrame:
            simpleImageWriter.write(frame, "/tmp/00-in.png")
            simpleImageWriter.write(hsvImg, "/tmp/01-hsv.png")
            simpleImageWriter.write(blur, "/tmp/02-blur.png")
            simpleImageWriter.write(contoursImg, "/tmp/03-contours.png")
            simpleImageWriter.write(result, "/tmp/04-results.png")
         if config.writeFrames:
            sbs = np.zeros((480,640*3, 3),np.uint8)
#np.concatenate((result,frame),axis=1)
            sbs[:480, :640, :3] = result
            sbs[:480, 640:640*2, :3] = frame
            hsvImgC = cv2.cvtColor(hsvImg, cv2.COLOR_GRAY2BGR)
            sbs[:480, 640*2:640*3, :3] = hsvImgC
            movie.writeFrame(sbs)
            movieIn.writeFrame(frame)

         fps = int(round(1000/((time.time()-millis2)*1000)))
         print "Loop bottom " + `fps`

#Clear buffer after we are done ...        
         if config.input == "camStill" or config.input == "camStream":
            camera.rawCapture.truncate(0)
        


m = main()
m.main()
