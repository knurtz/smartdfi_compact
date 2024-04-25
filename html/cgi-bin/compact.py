#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Check if started as CGI script and if so return content type and enable HTML error output
import os
import cgi
import cgitb
if 'REQUEST_METHOD' in os.environ:
	cgitb.enable(format="text")
	print("Content-Type: text/plain\r\n")    	# plain text is following
    
import requests
import datetime
import json
import serial


NUM_LINES = 5
STOP_ID = "33000115"
STOP_NAME = "Helmholtzstraße"
MIN_TIME = 0
TX_PORT = "/dev/ttyUSB1"
RX_PORT = "/dev/ttyUSB0"
ADDRESS = 2
SWITCH_TIME = 5
SWITCH_DEPS = False


# Create object to store the display text
single_line = {
	"text": " ",
	"text2": " ",
	"align": "L",       # "L" - left bound text, "R" - right bound text, "M" - center text, "D" - double text
	"dynamic": "S",     # "S" - static text, "B" - switch text
	"switch_time": 0
}
	
lines = []
for i in range(0, NUM_LINES):
	lines.append(single_line.copy())

# second object for display content after switching
if SWITCH_DEPS:
	lines_switched = lines.copy()


# get stop info from VVO
def get_departures():

	payload = {"stopid": STOP_ID, "limit": 15}
	try:
		r = requests.post("http://webapi.vvo-online.de/dm?format=json", data = payload)
	except:
		lines[0]["text"] = "Server nicht erreichbar"
		return

	if r.status_code != 200:
		lines[0]["text"] = "Server nicht erreichbar"
		return

	#print(r)

	deps = {}
	try:
		deps = r.json()
		deps = deps["Departures"]
	except:
		lines[0]["text"] = "Fehlerhafte Daten"
		return

	#print(deps)
	
	now = datetime.datetime.now()
	current_line = 0
	
	# go through all departures
	while deps:
		
		# get first departure
		d = deps.pop(0)
	
		# check if departure time is supplied
		if "RealTime" in d:
			time_str = d["RealTime"]
		elif "ScheduledTime" in d:
			time_str = d["ScheduledTime"]
		else:
			continue
		
		# decode time field
		try:
			dep_time = datetime.datetime.fromtimestamp(int(time_str[6:-10]))
		except:
			continue
			
		# get time difference in minutes from now
		diff_min = int((dep_time - now).total_seconds() / 60)
		
		# only show certain departures
		if diff_min < MIN_TIME:
			continue
		
		# try to append new data to text. if it fails, some of the required fields were missing
		try:
			lines[current_line]["text"] = d["LineName"] + " " + d["Direction"]
			lines[current_line]["text2"] = str(diff_min)
			lines[current_line]["align"] = "D"
		except:
			continue		
		
		current_line += 1
		if current_line >= NUM_LINES:
			break
		
		

# send data to display
def create_message():
	
	# start serial message as defined in protocol definition. message is a unicode string (type str)
	message = "10" + 5 * "0" + "F"
	
	# add every line to the message. only static text for now.
	for line, l in enumerate(lines):
		
		# handle double text lines
		# add one line (left aligned) with text, add a second line (right aligned) with text2 later
		if l["align"] == "D":
			l["align"] = "L"
			double_text = True
		else:
			double_text = False
		
		# start at segment 1, number of segments 3 as default
		# "proportional" font as default
		# static text with dummy switch time of one second as default
		message += "0" + str(line + 1) + "0103"	+  l["align"] + "PS01" + l["text"] + "\x17"
		
		# for double text, do the whole thing again for the second part of the line (right aligned)
		if double_text:
			message += "0" + str(line + 1) + "0103RPS01" + l["text2"] + "\x17"
			
	# end message with ETC character
	message += "\x03"
	
	# convert message to latin-1 -> message is a bytestring now (type bytes)
	message = message.encode('latin-1', 'ignore')

	# some characters are defined differently from latin-1
	charset = {
		b"\xe4": b"\x84",		# ä
		b"\xf6": b"\x94",		# ö
		b"\xfc": b"\x81",		# ü
		b"\xc4": b"\x8e",		# Ä
		b"\xd6": b"\x99",		# Ö
		b"\xdc": b"\x9a",		# Ü
		b"\xdf": b"\xe1"		# ß
	}
	
	for i, j in charset.items():
		message = message.replace(i, j)	
		
	# calculate checksum
	checksum = 0
	for char in message:
		checksum ^= char
			
	# apply start byte now, since it is not included in checksum
	message = b"\x02" + message + bytes([checksum])
		
	#print(message.hex(' '))
	return message
	

def send_message(msg):

	send_address = str(ADDRESS).encode('latin-1', 'ignore')
	rec_address = str(ADDRESS + 1).encode('latin-1', 'ignore')
	
	try:
		tx_channel = serial.Serial(port = TX_PORT, baudrate = 9600, bytesize = serial.EIGHTBITS, parity = serial.PARITY_EVEN, stopbits = serial.STOPBITS_ONE, timeout = 5)
		rx_channel = serial.Serial(port = RX_PORT, baudrate = 9600, bytesize = serial.EIGHTBITS, parity = serial.PARITY_EVEN, stopbits = serial.STOPBITS_ONE, timeout = 5)
	
	except:
		print("Error opening serial ports")
		print("Original message:")
		print(msg.hex(' '))
		return
	
	rx_channel.flushInput()
	tx_channel.write(b'\x04')   			# reset connection
	tx_channel.write(b'\x04')
	tx_channel.write(b'\x01' + rec_address + b'\x05')
	
	resp = rx_channel.read(2)				# reads two bytes from serial channel until it timeouts
	if not resp == b'\x10\x30':    
		print("Received no response from display.")
		return

	rx_channel.flushInput()		
	tx_channel.write(msg)
		
	resp = rx_channel.read(2)
	if not resp == b'\x10\x31':
		print("No acknowledge from display after successfully sending data")
	else:
		print("Data acknowledged by display")
		
	tx_channel.write(b'\x04')

	tx_channel.close()
	rx_channel.close()

# main()
get_departures()
send_message(create_message())
