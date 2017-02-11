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
import math
import time
import cv2
import numpy as np

#Internal libs
from input import camStill
from input import camStream
from input import diskStill
from input import diskStream
from config import fileConfig
from config import netConfig
from process import hsv
from output import file

import sys
from networktables import NetworkTable

def getWeight(point):
   return point.getWeight()

class main:
   def rotate(self, l, x):
      return l[-x:] + l[:-x]


   

   def findCorners(self, frame, points, centroid):
      tlc = centroid
      trc = centroid
      blc = centroid
      brc = centroid
     
      for pt in points:
#Check for top left
         if pt[0][0] < centroid[0] and pt[0][1] < centroid[1]:
            if pt[0][0] < tlc[0]:
               tlc = pt[0]

#Check for top right
         if pt[0][0] > centroid[0] and pt[0][1] < centroid[1]:
            if pt[0][0] > trc[0]:
               trc = pt[0]

#Check for bottom left
         if pt[0][0] < centroid[0] and pt[0][1] > centroid[1]:
            if pt[0][0] < blc[0]:
               blc = pt[0]

#Check for bottom right
         if pt[0][0] > centroid[0] and pt[0][1] > centroid[1]:
            if pt[0][0] > brc[0]:
               brc = pt[0]



      for r in range(3,10):
         cv2.circle(frame, (tlc[0], tlc[1]), r, (255,255,255)) #White
         cv2.circle(frame, (trc[0], trc[1]), r, (0,0,255)) #Red
         cv2.circle(frame, (blc[0], blc[1]), r, (0,255,0)) #Green
         cv2.circle(frame, (brc[0], brc[1]), r, (255,0,0)) #Blue

      ret = np.zeros((4,2), np.float32)
      ret[0] = tlc
      ret[1] = trc
      ret[2] = brc
      ret[3] = blc
      return ret
      

   def getInput(self, type, resolution, config):
      if type == "camStill":
         return camStill.camera(resolution)
      if type == "camStream":
         return camStream.camera(resolution, config.shutter, config.whiteBalance)
      if type == "diskStill":
         return diskStill.camera(resolution, config.imageStillPathIn)
      if type == "diskStream":
         return diskStream.camera(resolution, config.imageStreamPathIn)

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
      self.D = np.array([[0.0, 0.0, 0.0, 0.0]])
      
      # Camera matrix
      self.K = np.array([[alpha_u, 0.0, u0], 
                    [0.0, alpha_v, v0],
                    [0.0, 0.0, 1.0]])
#TODO: Recalculate this to be from the final position on the robot eg if the camera is looking up it will appear trapizodial!
      self.target_obj = np.array ([[-0.833,-0.5,0], #Outer Top Left
                             [-0.666,-0.5,0], #Inner Top Left
                             [-0.666,0.333,0], #Inner Bottom Left
                             [0.666,0.333,0], #Inner Bottom Right
                             [0.666,-0.5,0], #Inner Top Right
                             [0.833,-0.5,0], #Outer Top Right
                             [0.833,0.5,0], #Outer Bottom Right
                             [0.833,-0.5,0]], dtype='f') #Outer Bottom Left
#      self.target_obj_simple = np.array([[-0.833, -0.5, 0],
#                            [-0.833, 0.5, 0],
#                            [0.833, 0.5, 0],
#                            [0.833, -0.5, 0]])
      self.target_obj_simple = np.array([[-0.833, -0.5, 0],
                            [0.833, -0.5, 0],
                            [0.833, 0.5, 0],
                            [-0.833, 0.5, 0]])
      print "Entering main"
      print "Reading file config"
      self.config = fileConfig.config()
      
      #Network table
      NetworkTable.setIPAddress(self.config.ip)
      NetworkTable.setClientMode()
      NetworkTable.initialize()

      self.sd = NetworkTable.getTable("SmartDashboard")

      self.netConf = netConfig.config(self.config,self.sd)
      if self.config.writeFrames:
         self.movie = file.imageStreamer('/tmp/out.avi',(640*3,480))
         self.movieIn = file.imageStreamer('/tmp/out_raw.avi', (640,480))

      print "Looking for net config for 5s"
     

      camera = self.getInput(self.config.input,self.config.captureResolution, self.config)
      self.filter = hsv.hsv(self.config.hsv_low, self.config.hsv_high)
      
      self.simpleImageWriter = file.stillImageWriter()

      print "Entering main loop"
      self.lastValid = self.config.timeout*-1
      self.isValid = False
      self.lastIsValid = False

      frames = 0
      millis = time.time()

      if self.config.input != "diskStream":
         for frame in camera.getImage():
            if self.config.input == "camStream":
               frame = frame.array
            self.processFrame(frame)
            if self.config.input == "camStill" or self.config.input == "camStream":
               camera.rawCapture.truncate(0)
      else:
         while camera.hasMore():
             ret, frame = camera.getImage()
             self.processFrame(frame)

   
   def processFrame(self, frame):

#Convert colorspace to hsv
	 img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#Filter the image
         hsvImg = self.filter.filterHSV(img)

         
#Blur the image to smooth out the rough edges
         blur = cv2.GaussianBlur(hsvImg, (3,3), 1)
         blur = cv2.GaussianBlur(hsvImg, (7,7), 1)
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
            print "Looking at " + `len(approx)`
            if len(approx) >= 8 and len(approx) <= 10 and not(area <  self.config.minArea):
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

            corners = self.findCorners(result, biggest, centroid)

            i = 0
            dir = 1

#If the points start on the right we need to change the start index to be that of the left
#            if biggest[0][0][0] > centroidx:
#TODO: If we are starting at the top right and the next point is the left of that then i needs to be 5 not 3
#               if biggest[1][0][1] > biggest[7][0][1]:
#                  i = 3
#               else:
#                  i = 5
#            
#            for pt in biggest:
#               hullr[i] = pt[0]
#               i = i + dir
#               if i >= len(hullr):
#                  i = 0
#               if i < 0:
#                  i = len(hullr)-1

#If the order is reversed we need to reverse points 1-7 while leaving 0 in place
#So if are points are 		[0,1,2,3,4,5,6,7] 
#we ned to reorder to be	[0,7,6,5,4,3,2,1]
#Alternativly we can just swap the target descriptor ... 

#            if hullr[7][1] < hullr[1][1]:
#Get the first element
#               first = hullr[:1]
#Get the rest of the elements and reverse them
#               rest = hullr[1:][::-1]
#Recombine them
#               hullr = np.append(first,rest, axis=0)


            

            
            if len(corners) == len(self.target_obj_simple):
               retval, rvec, tvec = cv2.solvePnP(self.target_obj_simple, corners, self.K, self.D)
               self.lastValid = time.time()*1000
               self.isValid = True
               self.lastTargetT = tvec
               self.lastTargetR = rvec
               self.putTarget()
               self.putValid()
               if self.config.writeFrames:
                  cv2.putText(result,"xyz", (80,20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),2)
                  cv2.putText(result,`tvec[0][0]`, (80,40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),2)
                  cv2.putText(result,`tvec[1][0]`, (80,60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),2)
                  cv2.putText(result,`tvec[2][0]`, (80,80), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),2)

                  cv2.putText(result,"rot", (80,120), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),2)
                  cv2.putText(result,`rvec[0][0]`, (80,140), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),2)
                  cv2.putText(result,`rvec[1][0]`, (80,160), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),2)
                  cv2.putText(result,`rvec[2][0]`, (80,180), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),2)
                  print `retval` + " => " + `rvec` + " => " + `tvec`
           
         
#Write the in frame if we are configured to do so
         if self.config.writeFrame:
            simpleImageWriter.write(frame, "/tmp/00-in.png")
            simpleImageWriter.write(hsvImg, "/tmp/01-hsv.png")
            simpleImageWriter.write(blur, "/tmp/02-blur.png")
            simpleImageWriter.write(contoursImg, "/tmp/03-contours.png")
            simpleImageWriter.write(result, "/tmp/04-results.png")
         if self.config.writeFrames:
            sbs = np.zeros((480,640*3, 3),np.uint8)
#np.concatenate((result,frame),axis=1)
            sbs[:480, :640, :3] = result
            sbs[:480, 640:640*2, :3] = frame
            hsvImgC = cv2.cvtColor(hsvImg, cv2.COLOR_GRAY2BGR)
            sbs[:480, 640*2:640*3, :3] = hsvImgC
            self.movie.writeFrame(sbs)
            self.movieIn.writeFrame(frame)

         
         delta = (time.time()*1000) - self.lastValid
         #print `delta`

         if self.isValid and delta > self.config.timeout:
#Targeting Timeout, clear the info
            self.isValid = False
            self.putValid()
         millis = time.time()
         print "Loop bottom " + `millis`
         self.sd.putNumber("camera_time", millis);

#Clear buffer after we are done ...        
         
        
   def putValid(self):
      if self.isValid != self.lastIsValid:
         print "Putting valid: " + `self.isValid` + " " + `self.lastIsValid`
         self.sd.putBoolean("camera_isValid", self.isValid);
      self.lastIsValid = self.isValid


   def putTarget(self):
      print `self.lastTargetT[2][0]`
      self.sd.putNumber("camera_last_target_x", self.lastTargetT[0][0])
      self.sd.putNumber("camera_last_target_y", self.lastTargetT[1][0])
      self.sd.putNumber("camera_last_target_z", self.lastTargetT[2][0])
      
      self.sd.putNumber("camera_last_target_rot_x", self.lastTargetR[0][0])
      self.sd.putNumber("camera_last_target_rot_y", self.lastTargetR[1][0])
      self.sd.putNumber("camera_last_target_rot_z", self.lastTargetR[2][0])

class weightedPoint:
   def __init__(self, point, centroid):
      dx = point[1:] - centroid[0],
      dy = point[1] - centroid[1]
      dta = point - centroid
      dta = dta**2
      ret = 0
      for r in dta:
         ret = ret + r
      self.weight = ret


   def getWeight(self):
      return self.weight

m = main()
m.main()
