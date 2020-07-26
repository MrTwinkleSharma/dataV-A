import sqlite3 # because we're going to use SQLite Database management system
import json    # because we have to use json later
import ssl     # for handling ssl certificate errors

#creating a connection object to represent database
conn = sqlite3.connect('sqldatabase.sqlite3')

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

	count+=1
	address = line.strip()
	print(address)



