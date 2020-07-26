import sqlite3
import json
import codecs

#creating connection with SQL database
conn = sqlite3.connect('sqldatabase.sqlite')
cur = conn.cursor()

#creating a list of addresses and geodata and accessing only geodata using row[1]
cur.execute('SELECT * FROM Locations')

#opening file at write mode with codecs
fhand = codecs.open('where.js', 'w', "utf-8")
fhand.write("myData = [\n")
count = 0

#iterating one by one in cursor and accessing geodata
for row in cur :

    data = str(row[1].decode())
    try: js = json.loads(data)
    except: continue

    #continue if status is not OK for requested address

    if not('status' in js and js['status'] == 'OK') : continue

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0 : continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'", "")
    try :
        print(where, lat, lng)

        count = count + 1
        if count > 1 : fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")
