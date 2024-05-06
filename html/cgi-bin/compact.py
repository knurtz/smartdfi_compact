#!/usr/bin/python
# -*- coding: utf-8 -*-

# Check if started as CGI script and if so return content type and enable HTML error output
import os, cgi, cgitb
if 'REQUEST_METHOD' in os.environ:
	cgitb.enable(format="text")
	print("Content-Type: text/plain\r\n")


import serial
import json


class Display:
	
	def __init__(self, num_lines = 5, tx_port = "/dev/ttyUSB0", rx_port = "/dev/ttyUSB2", address = 10):
	
		self.NUM_LINES = num_lines
		self.TX_PORT = tx_port
		self.RX_PORT = rx_port
		self.ADDRESS = address

		# Object to store display contents
		single_line = {
			"text": " ",
			"text2": " ",
			"font": "P",
			"align": "L",	   	# "L" - left bound text, "R" - right bound text, "M" - center text, "D" - double text
			#"dynamic": "S",	 	# "S" - static text, "B" - switch text
			#"switch_time": 0
		}
	
		self.lines = []
		for i in range(0, self.NUM_LINES):
			self.lines.append(single_line.copy())

		# Second object for display content after switching
		self.lines2 = self.lines.copy()
	

	def create_message(self):
		
		# start serial message as defined in protocol definition. message is a unicode string (type str)
		message = "10" + 5 * "0" + "F"
		
		# add every line to the message. only static text for now.
		for line, l in enumerate(self.lines):
		
			if l["text"] == "":
					l["text"] = " "
					
			if l["text2"] == "":
					l["text2"] = " "
			
			# handle double text lines
			double_text = (l["align"] == "D")
			
			# start at segment 1, number of segments 3 as default -> "0103"
			# static text, switch time 1 second -> "S01"
			message += "0" + str(line + 1) + "0103"	+ ("L" if double_text else l["align"]) + l["font"] + "S01" + l["text"] + "\x17"
			
			# for double text, do the whole thing again for the second part of the line (right aligned)
			if double_text:
				message += "0" + str(line + 1) + "0103R" + l["font"] + "S01" + l["text2"] + "\x17"
				
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
		
		# add all special characters we find to our charset	
		for x in range(len(message) - 2):
			if message[x] == ord("\\"):		# detect backslash
				#print("Found backslash at position %d" % x)
				try:
					hexcode = int(chr(message[x + 1]) + chr(message[x + 2]), base = 16)
					#print("Decoded hex character %d" % hexcode)
					charset[message[x:x + 3]] = bytes([hexcode])
				except:
					pass
		
		#print(charset)
		
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
	

	def send_message(self, msg):

		send_address = str(self.ADDRESS).encode('latin-1', 'ignore')
		rec_address = str(self.ADDRESS + 1).encode('latin-1', 'ignore')
		
		try:
			with (serial.Serial(port = self.TX_PORT, baudrate = 9600, bytesize = serial.EIGHTBITS, parity = serial.PARITY_EVEN, stopbits = serial.STOPBITS_ONE, timeout = 1) as tx_channel,
				  serial.Serial(port = self.RX_PORT, baudrate = 9600, bytesize = serial.EIGHTBITS, parity = serial.PARITY_EVEN, stopbits = serial.STOPBITS_ONE, timeout = 1) as rx_channel):
		
				rx_channel.flushInput()
				
				tx_channel.write(b'\x04')   			# reset connection
				tx_channel.write(b'\x04')
				tx_channel.write(b'\x01' + rec_address + b'\x05')
				
				resp = rx_channel.read(2)				# read two bytes from serial channel until it timeouts
				
				if not resp == b'\x10\x30':	
					#raise Exception("Received no response from display.")
					pass

				rx_channel.flushInput()		
				tx_channel.write(msg)
					
				resp = rx_channel.read(2)
				
				if not resp == b'\x10\x31':
					raise Exception("No acknowledge from display after sending data")
				else:
					print("Success.\r\nData acknowledged by display")
					
				tx_channel.write(b'\x04')
				
				return True
		
		except Exception as err:
			print("Error: ", err)
			#print("Original message:")
			#print(msg.hex(' '))
			return False
		
		
	def create_and_send_message(self):
		if self.send_message(self.create_message()):
			s = json.dumps(self.lines, indent = 4, ensure_ascii = False)
			with open("current_text.json", "w") as f:
				print(s, file = f)
		
