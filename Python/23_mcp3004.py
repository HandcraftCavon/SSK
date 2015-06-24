#!/usr/bin/env python

import MCP3004 as ADC
import time

while True:
	print ADC.read(0)
	time.sleep(0.5)
