#!/usr/bin/python
# -*- coding: utf-8 -*-

# Check if started as CGI script and if so return content type and enable HTML error output
import os, cgi, cgitb
if 'REQUEST_METHOD' in os.environ:
	cgitb.enable(format="text")
	print("Content-Type: text/plain\r\n")


import random
import requests
from bs4 import BeautifulSoup

import compact

def show_joke():

	disp = compact.Display(5)

	try:
				
		# Get joke from spitzenwitze.de
		# todo: randomly choose category
		# todo: automatically get max page number
		r = requests.get("https://www.spitzenwitze.de/witze/flachwitze/page/%d" % random.randint(1, 107), headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"})
		if r.status_code != 200:
			raise Exception("Witzeserver nicht erreichbar")
			
		soup = BeautifulSoup(r.text, 'html.parser')
		
		# Get list of jokes on this page
		jokes = list(soup.find_all(attrs = {"class": "entry-content"}))
		random.shuffle(jokes)
		
		# go through all jokes, check max length of 20 characters per line
		for joke in jokes:
		
			joke = joke.find("p").string
			if joke == "":
				continue
		
			disp.clear_lines()
			current_line = 0
			too_long = False
			
			joke = joke.replace("\n", " ").replace("–", "-").replace("„", "\"").replace("“", "\"").split(" ")
			print(joke)
				
			# Try to fit the joke on the screen, 20 characters at a time
			# New lines are always respected
			# todo: Also add a new line for hyphen ( - ) and „ ... “
			
			for word in joke:
			
				if len(disp.lines[current_line]["text"]) + len(word) > 20:
					current_line += 1
					
					# Text gets too long, try with next joke
					if current_line >= 5:
						too_long = True
						break
						
				disp.lines[current_line]["text"] += word + " "
				
			if not too_long:
				success = True
				break
			else:
				continue
		
		if not success:
			raise Exception("Alle Witze zu lang")
			
	except Exception as err:
		disp.clear_lines()
		disp.lines[0]["text"] = str(err)
		disp.lines[0]["align"] = "M"
		
		raise(err)
			
	disp.create_and_send_message()
        
show_joke()