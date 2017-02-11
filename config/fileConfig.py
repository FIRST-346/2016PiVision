


class config:
   def __init__(self):
      self.ip = '10.3.46.2'
      #Init default values before reading the config file ...
      self.captureResolution = (640,480)
      self.input = "camStream"
      #self.input = "diskStream"
      #self.input = "diskStill"
      self.cameraH_Low = 60
      self.cameraS_Low = 250
      self.cameraV_Low = 250
      self.cameraH_High = 100
      self.cameraS_High = 255
      self.cameraV_High = 200
      self.hsv_low = [40,50,40]
      self.hsv_high = [100,255,200]
      self.writeFrames = False
      self.writeFrames = True
      #self.writeFrame = True
      self.writeFrame = False
      self.imageStillPathIn = "/tmp/test_in.png"
      self.imageStreamPathIn = "/tmp/test_in.avi"
      self.shutter = 4000
      self.whiteBalance = 2.3
      self.minArea = 150
      self.timeout = 100
