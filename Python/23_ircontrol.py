#!/usr/bin/python

import pylirc, time
import RPi.GPIO as GPIO

Rpin = 17
Gpin = 18
Bpin = 27
blocking = 0;

def setup():
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(Rpin, GPIO.OUT)
   GPIO.setup(Gpin, GPIO.OUT)
   GPIO.setup(GPIO, GPIO.OUT)
   pylirc.init("pylirc", "./conf", blocking)

def RGB(config):
   print config

def loop():
   # Very intuitive indeed
#      if(not blocking):
#         print "."
#         time.sleep(1)
   while True:
      s = pylirc.nextcode(1)
      while(s):
         for (code) in s:
            print "Command: %s, Repeat: %d" % (code["config"], code["repeat"])
            
#            if(code["config"] == "blocking"):
#               blocking = 1
#               pylirc.blocking(1)
#
#            elif(code["config"] == "nonblocking"):
#               blocking = 0
#               pylirc.blocking(0)

            RGB(code["config"])

         # Read next code?
         if(not blocking):
            s = pylirc.nextcode(1)
         else:
            s = []

def destroy():
   pylirc.exit()

if __name__ == '__main__':
   try:
      setup()
      loop()
   except KeyboardInterrupt:
      destroy()

