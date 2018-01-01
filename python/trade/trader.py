ind = ">"
fund_I_last_used = None

def setFund(fund):
	global fund_I_last_used
	fund_I_last_used = fund

def getDaysData(tickr):
	global ind
	ind = "." + ind
	import datetime
	import urllib2

	url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+tickr+'/chartdata;type=quote;range=1d/csv'

	today = datetime.datetime.now().strftime( "%m-%d-%y" )

	dfname = "data/" + today + ":" + tickr
	
	import os
	if os.path.exists( dfname ):
		data = open( dfname ).read()
	else:
		print ind + "Retrieving data for %s" % tickr
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

	ind = ind[1:]
	return return_data

def addCash(fund, amt):
	global ind
	ind = "." + ind
	import json
	whatIgot = json.loads( open( "funds/%s" % fund ).read() )
	if "__CASH__" not in whatIgot:
		whatIgot["__CASH__"] = 0
	whatIgot["__CASH__"] += amt

	open( "funds/%s" % fund, 'wb' ).write( json.dumps( whatIgot ) )

	print ind + "Cash successfully added"
	print ind + "Fund %s: %s" % (fund, whatIgot["__CASH__"])
	ind = ind[1:]

def sellAtPrice(tickr, amt, price):
	global fund_I_last_used

	if fund_I_last_used is None:
		raise Exception( "WTF... need a fund" )

	global ind

	import json
	allocation = json.loads( open( "funds/%s" % fund_I_last_used ).read() )

	if tickr not in allocation or amt > allocation[tickr]:
		print ind + "Cannot sell that much. I will sell as much as I can."
		amt = None

	if amt is None:
		amt = allocation[tickr]

	print ind + "Price determined to be %s" % price
	gain = price * amt

	allocation["__CASH__"] += gain
	if tickr not in allocation:
		allocation[tickr] = 0
	allocation[tickr] -= amt

	print ind + "SUCCESSFUL SALE"
	with open("funds/%s" % fund_I_last_used, 'wb') as outf:
		outf.write(json.dumps(allocation))
	print ind + "%s balance: %s" % (tickr, allocation[tickr])
	print ind + "CASH balance: %s" % allocation["__CASH__"]
	ind = ind[1:]

def sellAtTime(tickr, amt, t):
	global ind
	ind = "." + ind

	'''
	if amt is None:
		print ind + "Selling all of %s" % (tickr)
	else:
		print ind + "Selling %s of %s" % (amt, tickr)
	'''


	price = -1
	data = getDaysData(tickr)

	for row in data:
		cols = row.split(",")
		price = float( cols[1] )
		if t < int(cols[0]):
			break

	if price == -1:
		print ind + "No price found. Aborting sell"
		return

	sellAtPrice(tickr, amt, price)

def buyAtPrice(tickr, amt, price):
	global fund_I_last_used

	if fund_I_last_used is None:
		raise Exception( "WTF... need a fund" )

	import json
	allocation = json.loads( open( "funds/%s" % fund_I_last_used ).read() )

	print ind + "Price determined to be %s" % price
	cost = price * amt
	if allocation["__CASH__"] < cost:
		print ind + "Not enough CASH"
		return

	allocation["__CASH__"] -= cost
	if tickr not in allocation:
		allocation[tickr] = 0

	allocation[tickr] += amt
	print ind + "SUCCESSFUL PURCHASE"
	with open("funds/%s" % fund_I_last_used, 'wb') as outf:
		outf.write(json.dumps(allocation))
	print ind + "CASH balance: %s" % allocation["__CASH__"]
	print ind + "%s balance: %s" % (tickr, allocation[tickr])

def buyAtTime(tickr, amt, t):
	global ind
	ind = "." + ind

	price = -1
	data = getDaysData(tickr)

	for row in data:
		cols = row.split(",")
		price = float( cols[1] )
		if t < int(cols[0]):
			break

	if price == -1:
		print ind + "No price found. Aborting buy"
		return

	buyAtPrice(tickr, amt, price)
	ind = ind[1:]