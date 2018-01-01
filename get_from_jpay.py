import os
import json

def unescape(s):
	a = s.replace("&lt;", "<")
	a = a.replace("&gt;", ">")
	# this has to be last:
	a = a.replace("&amp;", "&")
	return a

alls = os.listdir( "/home/alec/jpay_scrapes" )
lasts = sorted( alls )[-1]

a = open( "/home/alec/jpay_scrapes/%s" % lasts ).read()
a = json.loads( a )
a = unescape( a[1] )

a = a.replace( "&lt;", "<" )
a = a.replace("&amp;", "&")
a = a.replace("&gt;", ">")

a = a[1:-1]

first_indent = -1

commands = []
command = []

for line in a.split("\n"):
	indent = 0
	trash_line = line
	while len(trash_line) > 0 and trash_line[0] == " ":
		indent += 1
		trash_line = trash_line[1:]


	if first_indent < 0:
		first_indent = indent
	elif indent <= first_indent:
		# add the lines we have to an array of commands...

		commands.append( command )
		command = []

	command.append( line )
		
print json.dumps( commands )
