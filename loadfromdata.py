import sqlite3 # because we're going to use SQLite Database management system
import json    # because we have to use json later
import ssl     # for handling ssl certificate errors
import sys     # because we are using time.sleep()
import time 
import http
#for handling url and requesting JSON file
import urllib.request, urllib.parse, urllib.error




api_key = False
# If you have a Google Places API key, enter it here

if api_key is False:
    api_key = 42
    serviceurl = "http://py4e-data.dr-chuck.net/json?"
else :
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"


#creating a connection object to represent database
conn = sqlite3.connect('sqldatabase.sqlite')

#this conn object is used to create a cursor which is useful to execute any SQL command
cur = conn.cursor()

#let's create a TABLE 
cur.execute('''CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

#ignoring ssl certificate errors to disable security check
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


fh = open('where.data','r')
count = 0
for line in fh:
	if count >200 :
		print("Recieved 200 Location restart to recieve more and SQL will auto update this")
		break

	address = line.strip()
	print(address)
	#selecting the address from table
	cur.execute('''SELECT geodata from Locations WHERE address = ?''', (memoryview(address.encode()), ))

	#if that address is already in list then continue otherwise start inserting into database

	try :
		data = cur.fetchone()[0]
		print("Found in Database", address)
		continue
	except:
		pass

	#creating a dictionary to be passed in request 
	params = dict()
	params["address"] = address
	params["key"] = api_key
	url = serviceurl + urllib.parse.urlencode(params)

	print('Retrieving', url)
	uh = urllib.request.urlopen(url, context=ctx)
	data = uh.read().decode()
	print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
	count+=1
	try:
   	    js = json.loads(data)

	except:
		print(data)  # We print in case unicode causes an error
		continue

	if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
		print('==== Failure To Retrieve ====')
		print(data)
		break


	cur.execute('''INSERT INTO Locations (address, geodata) VALUES(?,?)''', (memoryview(address.encode()), (memoryview(data.encode()))))
	conn.commit()
	if count % 10 == 0:
		print("Pausing for a bit.....")
		time.sleep(5)




	

print("Run geodump.py to read the data from the database so you can vizualize it on a map.")







