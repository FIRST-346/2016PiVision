class config:
   def __init__(self, fileConfig, networkTable):
      self.config = fileConfig
      self.networkTable = networkTable
      self.networkTable.addGlobalListener(self.valueChanged)
      self.c_listener = ConnectionListener(self)
      self.networkTable.addConnectionListener(self.c_listener)

   def connected(self):
      try:
         i = self.networkTablegetNumber('cameraH_Low')
         if i > 0:
            self.config.cameraH_Low = i
      except KeyError:
         self.networkTableputNumber('cameraH_Low', self.config.cameraH_Low)
      try:
         i = self.networkTablegetNumber('cameraS_Low')
         if i > 0:
            self.config.cameraS_Low = i
      except KeyError:
         self.networkTableputNumber('cameraS_Low', self.config.cameraS_Low)
      try:
         i = self.networkTablegetNumber('cameraV_Low')
         if i > 0:
            self.config.cameraV_Low = i
      except KeyError:
         self.networkTableputNumber('cameraV_Low', self.config.cameraV_Low)

      try:
         i = self.networkTablegetNumber('cameraH_High')
         if i > 0:
            self.config.cameraH_High = i
      except KeyError:
         self.networkTableputNumber('cameraH_High', self.config.cameraH_High)
      try:
         i = self.networkTablegetNumber('cameraS_High')
         if i > 0:
            self.config.cameraS_High = i
      except KeyError:
         self.networkTableputNumber('cameraS_High', self.config.cameraS_High)
      try:
         i = self.networkTablegetNumber('cameraV_High')
         if i > 0:
            self.config.cameraV_High = i
      except KeyError:
         self.networkTableputNumber('cameraV_High', self.config.cameraV_High)


   def valueChanged(key, value, isNew):
      print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))

      changed = False

      if key == "/SmartDashboard/cameraH_Low":
            print("Camera h change check")
            if self.config.cameraH_Low != value:
               self.config.cameraH_Low = value
               changed = True

      if key == "/SmartDashboard/cameraS_Low":
            print("Camera s change check")
            if self.config.cameraS_Low != value:
               self.config.cameraS_Low = value
               changed = True

      if key == "/SmartDashboard/cameraV_Low":
            print("Camera v change check")
            if self.config.cameraV_Low != value:
               self.config.cameraV_Low = value
               changed = True

      if key == "/SmartDashboard/cameraH_High":
            print("Camera h change check")
            if self.config.cameraH_High != value:
               self.config.cameraH_High = value
               changed = True

      if key == "/SmartDashboard/cameraS_High":
            print("Camera s change check")
            if self.config.cameraS_High != value:
               self.config.cameraS_High = value
               changed = True

      if key == "/SmartDashboard/cameraV_High":
            print("Camera v change check")
            if self.config.cameraV_High != value:
               self.config.cameraV_High = value
               changed = True




class ConnectionListener:
    def __init__(self, netConfig):
       self.netConfig = netConfig

    def connected(self, table):
        print("Connected", table)
        self.netConfig.connected();

    def disconnected(self, table):
        print("Disconnected", table)


