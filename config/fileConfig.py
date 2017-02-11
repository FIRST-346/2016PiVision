


class config:
   def __init__(self):
      self.ip = '10.3.46.20'
      #Init default values before reading the config file ...
      self.captureResolution = (640,480)
      #self.input = "diskStill"
      self.input = "diskStill"
      self.cameraH_Low = 60
      self.cameraS_Low = 30
      self.cameraV_Low = 80
      self.hsv_low = [60,30,80]
      self.hsv_high = [100,255,200]
      self.writeFrame = True
      self.imageStillPathIn = "/tmp/test_in.jpg"
      self.imageStillPathOut = "/tmp/test_out.png"
