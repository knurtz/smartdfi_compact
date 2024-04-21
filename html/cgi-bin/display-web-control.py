#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
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

for i in range(0,5):
	
	pass	


print "Content-type:text/plain\r\n"
print "Success"
print text_left
print text_right
print font
print align
