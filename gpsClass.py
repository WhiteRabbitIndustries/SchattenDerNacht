#file  -- gpsClass.py --
import threading
import gps
import time
class GpsPoller(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
    #self.session = gps(mode=WATCH_ENABLE)
    # Listen on port 2947 (gpsd) of localhost
    self.session = gps.gps("localhost", "2947")
    self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    self.current_value = None
    self.running = True 

  def get_current_value(self):
    return self.current_value

  def run(self):
    try:
      while self.running:
        self.current_value = self.session.next()
        time.sleep(1) # tune this, you might not get values that quickly
    except StopIteration:
      pass

  #time acquisiton function from gpsd
  def getTime(self):
    try:
      if hasattr(self.current_value, 'time'):
        print self.current_value.time
    except(AttributeError, KeyError):
      pass

  # gps acquisiton function
  def getGPS(self):
    try:
      #if self.current_value['class'] == 'TPV':
      coord = {'x': 0, 'y': 0}
      if hasattr(self.current_value, 'lat'):
        #print self.current_value.lat
        coord['x'] = self.current_value.lat
      if hasattr(self.current_value, 'lon'):
        #print self.current_value.lon
        coord['y'] = self.current_value.lon
      return coord
    except(AttributeError, KeyError):
      pass

