import spidev
import time

#Establish SPI connection with Bus 0, Device 0
spi = spidev.SpiDev()
spi.open(0,0)

def read(channel):
	#Perform SPI transaction and store returned bits in 'r'
	r = spi.xfer([1, (8+channel)<<4, 0])
	#Filter data bits from returned bits
	adcout = ((r[1]&3) << 8) + r[2]
	#Return value from 0-1023
	return adcout

def loop():
	while True:
		print read(0)
		time.sleep(1)

if __name__ == "__main__":
	loop()
