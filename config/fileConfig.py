


class config:
   def __init__(self):
      self.ip = '10.3.46.20'
      #Init default values before reading the config file ...
      self.captureResolution = (640,480)
      self.input = "camStream"
      #self.input = "diskStill"
      self.cameraH_Low = 60
      self.cameraS_Low = 30
      self.cameraV_Low = 80
      self.hsv_low = [60,30,80]
      self.hsv_high = [100,255,200]
      self.writeFrames = True
      #self.writeFrame = True
      self.writeFrame = False
      self.imageStillPathIn = "/tmp/test_in.png"
      self.shutter = 5000
      self.minArea = 150
