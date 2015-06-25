import RPi.GPIO as GPIO
import time
import sys

# BCM pin numbering
LedR = 17
LedG = 18
LedB = 27
Beep = 22

ds18b20 = '28-031467805fff'
location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'

def setup():
	global lowl, highl
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LedR, GPIO.OUT)
	GPIO.setup(LedG, GPIO.OUT)
	GPIO.setup(LedB, GPIO.OUT)
	GPIO.setup(Beep, GPIO.OUT)
	if(len(sys.argv) != 3):
		print 'Usage : sudo python 34_temp_monitor.py [temperature lower limit] [upper limit]'
		print 'For example : sudo python 34_temp_monitor.py 29 31'
		quit()
	lowl = sys.argv[1]
	highl = sys.argv[2]
     
	if lowl >= highl:
		print 'Parameters error, lower limit should be less than upper limit'   
		quit()

def beepCtrl(t):
	GPIO.output(Beep, 1)
	time.sleep(t)
	GPIO.output(Beep, 0)
	time.sleep(t)

def tempRead():
	tfile = open(location)
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	return temperature

def ledOn(led):
	GPIO.output(LedR, 1)
	GPIO.output(LedG, 1)
	GPIO.output(LedB, 1)
	if led != 0:
		GPIO.output(led,  0)

def loop():
	while True:
		temp = tempRead()
		print 'The lower limit of temperature : ', lowl
		print 'The upper limit of temperature : ', highl
		print 'Current temperature : ', temp
		if float(temp) < float(lowl):
			ledOn(LedB)
			for i in range(0, 3):
				beepCtrl(0.5)
		if temp >= float(lowl) and temp < float(highl):
			ledOn(LedG)
		if temp >= float(highl):
			ledOn(LedR)
			for i in range(0, 3):
				beepCtrl(0.1)

def destroy():
	ledOn(0)
	GPIO.output(Beep, 1)
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()
