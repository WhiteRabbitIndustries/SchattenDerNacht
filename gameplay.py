#!/usr/bin/env python
    
print "Welcome to imUntergrund!"

# import libraries:     
import time
from time import sleep
import serial
import pygame
import os
import math
from gpsClass import *
from wifiPoller import *
from gameObjectsClass import *
from beaconPoller import *





# import gameplay values from files: 
#import xml for locations, audio files.
gameData = GameData('gamedata.xml')

#print "Game Location Count: "
#print gameData.getLocationCount()

pygame.mixer.init()
# import state/level (so that)

# enabling to start listening. can be powered off when not needed, but should check warmstartup conditiosn




# main loop
print "entering main loop"

gpsp = GpsPoller() #create threaded gps
wifip = wifiPoller()
beaconp = beaconPoller()

try: 
  gpsp.start() #start watching gps values
  wifip.start()

  while True:
    # get gps values
    
    currentCoord = gpsp.getGPS()
    print ""
    print currentCoord

    #state machine
    #go through all states. 
    for x in xrange(0,gameData.getLocationCount()-1):
      #self.locationCount = 0
      # if active, check gps. 
      distance = 0.0
      if gameData.locationList[x].active == True:

        #calc distance based on gps
        distance = float(math.sqrt((gameData.locationList[x].coord['x'] - currentCoord['x'])**2 + (gameData.locationList[x].coord['y'] - currentCoord['y'])**2))
        distance = distance / 0.00001; #translate to meters
        print "Distance to %s is %d." % (gameData.locationList[x].name, distance)


        inBoundBeacon = False

        # get wifi aps for the location, then check if they are in bound
        for a in xrange(0,len(gameData.locationList[x].beacons)):
          #print "in scan", a

          inBoundBeacon = inBoundBeacon or beaconp.inBeaconRange(gameData.locationList[x].beacons[a]['uuid'],gameData.locationList[x].beacons[a]['rssi'])
          
        print inBoundBeacon


        #calc in bound based on wifi ap signals
        inBoundWifi = False
        #print len(gameData.locationList[x].wifiAPs)
        #

        # get wifi aps for the location, then check if they are in bound
        for a in xrange(0,len(gameData.locationList[x].wifiAPs)):
          #print "in scan", a

          inBoundWifi = inBoundWifi or wifip.inWifiRange(gameData.locationList[x].wifiAPs[a]['address'],gameData.locationList[x].wifiAPs[a]['quality'])
          
        print inBoundWifi


        if (distance<gameData.locationList[x].radius) | inBoundWifi | inBoundBeacon:
          # location check in: enter initial state, update prereq of other locaitons/states
          print "onlocation"
          #print "wifi strength: %d" % signalStrength
          gameData.locationList[x].onloc = True
        else: 
          gameData.locationList[x].onloc = False
          
        # if state is active, and if onlocation,
        if gameData.locationList[x].onloc == True:
          # play the current state      
          if gameData.locationList[x].stateList[gameData.locationList[x].currentState].activated == False:
            #unlocklist
            print "unlocking locations with id: "
            unlocklist = gameData.locationList[x].stateList[gameData.locationList[x].currentState].unlocklist
            print unlocklist
            for u in range(0,len(unlocklist)):
              gameData.locationList[unlocklist[u]-1].active = True
              #print unlocklist[u]
            gameData.locationList[x].stateList[gameData.locationList[x].currentState].activated = True
          
          #play audio
          if pygame.mixer.music.get_busy() != True:
            pygame.mixer.music.load(gameData.locationList[x].stateList[gameData.locationList[x].currentState].audiofile)
            pygame.mixer.music.play()




          #for s in xrange(0,gameData.locationList[x].getStateCount()-1):
          #if unlocking for the first time, do these.. 
          # go through states, checking prereq, if true, play actions (only the last one?)

          #play aduio
          #gameData.locationList[x].stateList['a']
        """
        print "pygame playing"

pygame.mixer.music.load("try1.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
    """
        #os.system('mpg123 -q '+'try1.mp3' +' &')


      #pass
      
      
      #if on location, state enable
      #if state reached, trigger enable other states. 







    #gpsp.getTime()

    # calculate position/distance to state
    
    

    # game state machine

    time.sleep(1)
    

except(KeyboardInterrupt, SystemExit):
  print "\nKilling Threads.."
  gpsp.running = False 
  gpsp.join()
  wifip.running = False 
  wifip.join()

print "Done.\nExiting."

#game state machine

    #
  






"""
print "system mpg321 playing"
os.system('mpg123 -q try1.mp3 &')

print "pygame playing"
pygame.mixer.init()
pygame.mixer.music.load("try1.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
"""


      


# broadcast ingame status through wifi
#udp?



