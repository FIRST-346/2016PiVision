


class config:
   def __init__(self):
      #Init default values before reading the config file ...
      self.captureResolution = (640,480)
      self.input = "diskStill"
      self.hsv_low = [60,30,80]
      self.hsv_high = [100,255,200]
      self.writeFrame = True
      self.imageStillPathIn = "/tmp/test_in.jpg"
      self.imageStillPathOut = "/tmp/test_out.png"
