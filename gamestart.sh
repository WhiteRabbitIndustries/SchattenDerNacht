#!/bin/sh
sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock&
# wait

#screen game play
sudo screen -dm python /usr/share/adafruit/webide/repositories/ResDev/imUntergrund/gameplay.py