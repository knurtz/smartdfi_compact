#!/usr/bin/python

# Check if started as CGI script and if so return content type and enable HTML error output
import os, cgi, cgitb
if 'REQUEST_METHOD' in os.environ:
	cgitb.enable(format="text")
	print("Content-Type: text/plain\r\n")    	# plain text is following

form = cgi.FieldStorage() 

text_left = [
	form.getvalue('line1-left'),
	form.getvalue('line2-left'),
	form.getvalue('line3-left'),
	form.getvalue('line4-left'),
	form.getvalue('line5-left')
]

text_right = [
	form.getvalue('line1-right'),
	form.getvalue('line2-right'),
	form.getvalue('line3-right'),
	form.getvalue('line4-right'),
	form.getvalue('line5-right')
]

font = [
	form.getvalue('line1-font'),
	form.getvalue('line2-font'),
	form.getvalue('line3-font'),
	form.getvalue('line4-font'),
	form.getvalue('line5-font')
]

align = [
	form.getvalue('line1-align'),
	form.getvalue('line2-align'),
	form.getvalue('line3-align'),
	form.getvalue('line4-align'),
	form.getvalue('line5-align')
]

print("Success")
print(text_left)
print(text_right)
print(font)
print(align)

# todo: set fields accordingly
