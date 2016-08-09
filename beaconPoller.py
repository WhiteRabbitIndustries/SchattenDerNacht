#file  -- wifiPoller.py --
import threading
import sys
import subprocess
import time
import blescan
import sys

import bluetooth._bluetooth as bluez



class beaconPoller(threading.Thread):

  parsed_beacons=[]
  running = True

  def __init__(self):
    threading.Thread.__init__(self)
    self.beaconsList =[]
    self.running = True 

    dev_id = 0
    try:
      self.sock = bluez.hci_open_dev(dev_id)
      print "ble thread started"

    except:
      print "error accessing bluetooth device..."
      sys.exit(1)

    blescan.hci_le_set_scan_parameters(self.sock)
    blescan.hci_enable_le_scan(self.sock)


  def stop(self):
    print "Beacons STOPPED"
    self.running = False

  def run(self):
    try:
      while self.running:

        if self.running is False:
          print "Beacons stopped"
          return
        
        self.beaconsList = blescan.getBeacons(self.sock, 10)
        print "Beacons List: ", self.beaconsList  
        time.sleep(2) # tune this, you might not get values that quickly


        #self.running = false;
    except StopIteration:
      pass

  def inBeaconRange(self, uuid, rssi):
    try:
      # scan through 
  
      print "Traget UUID: ", uuid 
  
      for beacon in self.beaconsList:
      
        if beacon['uuid'] == uuid and beacon['rssi'] > rssi:
          print "UUID: ", beacon['uuid'] 
          print "RSSI: ", beacon['rssi'] 
          return True
      
      return False

    except StopIteration:
      pass

