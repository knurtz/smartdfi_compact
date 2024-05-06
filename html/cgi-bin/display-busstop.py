#!/usr/bin/python
# -*- coding: utf-8 -*-

# Check if started as CGI script and if so return content type and enable HTML error output
import os, cgi, cgitb
if 'REQUEST_METHOD' in os.environ:
	cgitb.enable(format="text")
	print("Content-Type: text/plain\r\n")
	
	
import requests
import datetime
import json

import compact

NUM_LINES = 5
STOP_ID = "33000742"
STOP_NAME = "Helmholtzstraße"
MIN_TIME = 0

# get stop info from VVO
def show_departures():

	disp = compact.Display(NUM_LINES)

	try:
		r = requests.post("http://webapi.vvo-online.de/dm?format=json", data = {"stopid": STOP_ID, "limit": 15})
		if r.status_code != 200:
			raise Exception
			
	except:
		disp.lines[0]["text"] = "Server nicht erreichbar"
		return
		

	try:
		deps = r.json()["Departures"]
		
	except:
		disp.lines[0]["text"] = "Fehlerhafte Daten"
		return

	
	now = datetime.datetime.now()
	current_line = 0
	
	# go through all departures
	while deps:
		
		# get next departure
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
			disp.lines[current_line]["text"] = d["LineName"] + " " + d["Direction"]
			if diff_min != 0:
				disp.lines[current_line]["text2"] = str(diff_min)
			else:
				disp.lines[current_line]["text2"] = " "
			disp.lines[current_line]["align"] = "D"
		except:
			continue		
		
		current_line += 1
		if current_line >= NUM_LINES - 1:
			break
			
	disp.lines[NUM_LINES - 1]["text"] = STOP_NAME
	disp.lines[NUM_LINES - 1]["align"] = "M"
			
	disp.create_and_send_message()
        
show_departures()