def get_days_data( tickr ):
	import datetime
	import urllib2
	print "Data for %s already retrieved" % tickr

	url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+tickr+'/chartdata;type=quote;range=1d/csv'

	today = datetime.datetime.now().strftime( "%m-%d-%y" )

	dfname = "data/" + today + ":" + tickr
	
	import os
	if os.path.exists( dfname ):
		data = open( dfname ).read()
	else:
		print "Retrieving data for %s from web" % tickr
		data = urllib2.urlopen( url ).read()
		with open( dfname, 'wb' ) as ofile:
			ofile.write( data )

	data = data.split( "\n" )
	return_data = []
	for d in data:
		cols = d.split(",")
		if len(cols) < 6:
			continue

		# if everything can't be conerted to a float, continue
		thissucks = False
		for c in cols:
			try:
				float(c)
			except:
				thissucks = True
		if thissucks:
			continue

		return_data.append( d )

	return return_data

import os
funds = os.listdir( 'funds' )

import json
for fund in funds:
	components = open( "funds/%s" % fund ).read()
	components = json.loads( components )
	for tickr in components:
		get_days_data( tickr )
