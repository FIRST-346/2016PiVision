"""
This proc will be responsible for watching over the following
1) Configuration changes
   a) If the selected config changes (or a net change occurs) 
      then restart the main proc
2) Process watch
   a) If the main process dies then restart it
   b) Look at rapid fail protection
      eg. process dies 5 times in 1 second, wait 5 seconds before restarting
3) Look for roborio connection
   a) Need some method of communicating that the vision is running to the 
      roborio

"""
