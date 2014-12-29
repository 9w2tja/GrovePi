# grovepi.py
# v1.2
# This file provides the basic functions for using the GrovePi
#
# Karan Nayan
# Initial Date: 13 Feb 2014
# Last Updated: 29 Dec 2014
# http://www.dexterindustries.com/
#
# These files have been made available online through
# a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
###############################################################################
import smbus
import time
import math
import RPi.GPIO as GPIO
import struct

rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
	bus = smbus.SMBus(1)
else:
	bus = smbus.SMBus(0)

# I2C Address of Arduino
address = 0x04

# Command Format
# digitalRead() command format header
dRead_cmd = [1]
# digitalWrite() command format header
dWrite_cmd = [2]
# analogRead() command format header
aRead_cmd = [3]
# analogWrite() command format header
aWrite_cmd = [4]
# pinMode() command format header
pMode_cmd = [5]
# Ultrasonic read
uRead_cmd = [7]
# Accelerometer (+/- 1.5g) read
acc_xyz_cmd = [20]
# RTC get time
rtc_getTime_cmd = [30]
# DHT Pro sensor temperature
dht_temp_cmd = [40]

# Grove LED Bar commands
ledBarInit_cmd=[50]      # begin(unsigned char pinClock, unsigned char pinData, bool greenToRed)
ledBarOrient_cmd=[51]    # setGreenToRed(bool greenToRed)
ledBarLevel_cmd=[52]     # setLevel(unsigned char level)
ledBarSetOne_cmd=[53]    # setLed(unsigned char led, bool state)
ledBarToggleOne_cmd=[54] # toggleLed(unsigned char led)
ledBarSet_cmd=[55]       # setBits(unsigned int bits)
ledBarGet_cmd=[56]       # getBits()

# Function declarations of the various functions used for encoding and sending
# data from RPi to Arduino


# Write I2C block
def write_i2c_block(address, block):
	try:
		return bus.write_i2c_block_data(address, 1, block)
	except IOError:
		print "IOError"
		return -1


# Read I2C byte
def read_i2c_byte(address):
	try:
		return bus.read_byte(address)
	except IOError:
		print "IOError"
		return -1


# Read I2C block
def read_i2c_block(address):
	try:
		return bus.read_i2c_block_data(address, 1)
	except IOError:
		print "IOError"
		return -1


# Arduino Digital Read
def digitalRead(pin):
	write_i2c_block(address, dRead_cmd + [pin, 0, 0])
	time.sleep(.1)
	n = read_i2c_byte(address)
	return n


# Arduino Digital Write
def digitalWrite(pin, value):
	write_i2c_block(address, dWrite_cmd + [pin, value, 0])
	return 1


# Setting Up Pin mode on Arduino
def pinMode(pin, mode):
	if mode == "OUTPUT":
		write_i2c_block(address, pMode_cmd + [pin, 1, 0])
	elif mode == "INPUT":
		write_i2c_block(address, pMode_cmd + [pin, 0, 0])
	return 1


# Read analog value from Pin
def analogRead(pin):
	bus.write_i2c_block_data(address, 1, aRead_cmd + [pin, 0, 0])
	time.sleep(.1)
	bus.read_byte(address)
	number = bus.read_i2c_block_data(address, 1)
	return number[1] * 256 + number[2]


# Write PWM
def analogWrite(pin, value):
	write_i2c_block(address, aWrite_cmd + [pin, value, 0])
	return 1


# Read temp from Grove Temp Sensor
def temp(pin):
	a = analogRead(pin)
	resistance = (float)(1023 - a) * 10000 / a
	t = (float)(1 / (math.log(resistance / 10000) / 3975 + 1 / 298.15) - 273.15)
	return t


# Read value from Grove Ultrasonic
def ultrasonicRead(pin):
	write_i2c_block(address, uRead_cmd + [pin, 0, 0])
	time.sleep(.2)
	read_i2c_byte(address)
	number = read_i2c_block(address)
	return (number[1] * 256 + number[2])


# Read Grove Accelerometer (+/- 1.5g) XYZ value
def acc_xyz():
	write_i2c_block(address, acc_xyz_cmd + [0, 0, 0])
	time.sleep(.1)
	read_i2c_byte(address)
	number = read_i2c_block(address)
	if number[1] > 32:
		number[1] = - (number[1] - 224)
	if number[2] > 32:
		number[2] = - (number[2] - 224)
	if number[3] > 32:
		number[3] = - (number[3] - 224)
	return (number[1], number[2], number[3])


# Read from Grove RTC
def rtc_getTime():
	write_i2c_block(address, rtc_getTime_cmd + [0, 0, 0])
	time.sleep(.1)
	read_i2c_byte(address)
	number = read_i2c_block(address)
	return number


# Read and return temperature and humidity from Grove DHT Pro
def dht(pin, module_type):
	write_i2c_block(address, dht_temp_cmd + [pin, module_type, 0])

	# Delay necessary for proper reading fron DHT sensor
	time.sleep(.6)
	try:
		read_i2c_byte(address)
		number = read_i2c_block(address)
		if number == -1:
			return -1
	except (TypeError, IndexError):
		return -1
	# data returned in IEEE format as a float in 4 bytes
	f = 0
	# data is reversed
	for element in reversed(number[1:5]):
		# Converted to hex
		hex_val = hex(element)
		#print hex_val
		try:
			h_val = hex_val[2] + hex_val[3]
		except IndexError:
			h_val = '0' + hex_val[2]
		# Convert to char array
		if f == 0:
			h = h_val
			f = 1
		else:
			h = h + h_val
	# convert the temp back to float
	t = round(struct.unpack('!f', h.decode('hex'))[0], 2)

	h = ''
	# data is reversed
	for element in reversed(number[5:9]):
		# Converted to hex
		hex_val = hex(element)
		# Print hex_val
		try:
			h_val = hex_val[2] + hex_val[3]
		except IndexError:
			h_val = '0' + hex_val[2]
		# Convert to char array
		if f == 0:
			h = h_val
			f = 1
		else:
			h = h + h_val
	# convert back to float
	hum = round(struct.unpack('!f', h.decode('hex'))[0], 2)
	return [t, hum]


# Grove LED Bar - initialise
# begin(unsigned char pinClock, unsigned char pinData, bool greenToRed)
def ledbar_init(pin,orientation):
	write_i2c_block(address,ledBarInit_cmd+[pin,0,0])
	return 1

# Grove LED Bar - set orientation
# setGreenToRed(bool greenToRed)
def ledbar_orientation(pin,orientation):
	write_i2c_block(address,ledBarOrient_cmd+[pin,orientation,0])
	return 1

# Grove LED Bar - set level
# setLevel(unsigned char level)
def ledbar_setLevel(pin,level):
	write_i2c_block(address,ledBarLevel_cmd+[pin,level,0])
	return 1

# Grove LED Bar - set single led
# setLed(unsigned char led, bool state)
def ledbar_setLed(pin,led,state):
	write_i2c_block(address,ledBarSetOne_cmd+[pin,led,state])
	return 1

# Grove LED Bar - toggle single led
# toggleLed(unsigned char led)
def ledbar_toggleLed(pin,led):
	write_i2c_block(address,ledBarToggleOne_cmd+[pin,led,0])
	return 1

# Grove LED Bar - set all leds
# setBits(unsigned int bits)
def ledbar_setBits(pin,state):
	byte1 = state & 255
	byte2 = state >> 8
	write_i2c_block(address,ledBarSet_cmd+[pin,byte1,byte2])
	return 1

# Grove LED Bar - get current state
# getBits()
def ledbar_getBits(pin):
	write_i2c_block(address,ledBarGet_cmd+[pin,0,0])
	time.sleep(.2)
	read_i2c_byte(0x04)
	block = read_i2c_block(0x04)
	return block[1] ^ (block[2] << 8)
