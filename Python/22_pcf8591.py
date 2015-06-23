#!/usr/bin/env python
import PCF8591

def loop():
	while True:
		PCF8591.write(PCF8591.read(0))

def destroy():
	PCF8591.write(0)

if __name__ == "__main__":
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
