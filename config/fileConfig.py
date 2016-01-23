


class config:
   def __init__(self):
      #Init default values before reading the config file ...
      self.captureResolution = (640,480)
      self.input = "diskStill"
      self.hsv_low = [0,0,0]
      self.hsv_high = [1,1,1]
      self.writeFrame = True
      self.imageStillPath = "/tmp/test_out.png"
