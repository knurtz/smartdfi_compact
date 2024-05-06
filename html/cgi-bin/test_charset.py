#!/usr/bin/python
# -*- coding: utf-8 -*-

cgi = False

# Check if started as CGI script and if so return content type and enable HTML error output
import os, cgi, cgitb
if 'REQUEST_METHOD' in os.environ:
	cgitb.enable(format="text")
	print("Content-Type: text/plain; charset=utf-8\r\n")    	# plain text is following
	form = cgi.FieldStorage()
	page = int(form["page"].value)
	print("Printing codepages 0x%2x and 0x%2x" % (page * 16, (page + 1) * 16))
	cgi = True

import compact

disp = compact.Display(5)

for line in range(4):
	current_page = page * 16 + line * 8
	disp.lines[line]["text"] = "0x%2x:" % current_page
	
	for x in range(8):
		disp.lines[line]["text"] += " \\%2x" % (current_page + x)

disp.create_and_send_message()
