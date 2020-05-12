#!/usr/bin/env python
import json
import time
import sqlite3
import sys
import datetime
import argparse

parser = argparse.ArgumentParser(description="Print a list of seen clients")
parser.add_argument("--in", action="store", dest="infile", required=True, help='Input file ')
parameters = parser.parse_args()


epoch_time = int(time.time())
#print("epoch")
#print(epoch_time)
#print("back time")
back_time = (epoch_time-360)
#print(back_time) back time is how many seconds to go back - in this example we are looking for devices seen in last 3min
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def readSqliteTable():
    try:
        sqliteConnection = sqlite3.connect(parameters.infile)
        cursor = sqliteConnection.cursor()
        #print("Connected to SQLite")
        #print(back_time)
        sqlite_select_query = "SELECT * from devices where (last_time>? AND last_time>first_time+120)"
        #this looks for devices seen in last 3 min aka back_time and seen at least 2 min after seeing for the very first time
        #this ensures that people driving by and in range for less than 2 minutes are not picked up
        cursor.execute(sqlite_select_query,(back_time,))
        records = cursor.fetchall()
        #print("Total rows are:  ", len(records))
        #print("Printing each row")
        for row in records:
            #print("Zero: ", row[4])
            f1=open('./temp.json', 'w+')
            f1.write(row[14])
            f1.close()
            # Opening JSON file
            f = open('./temp.json',)

            # returns JSON object as
            # a dictionary
            jiggadata = json.load(f)
            whatdevice = ""
            # Iterating through the json
            # let's get the manufacturer which is buried in device.devices a JSON BLOB
            for i in jiggadata['kismet.device.base.manuf']:
                whatdevice = whatdevice + i
            # Closing file
            f.close()
            print(row[4],whatdevice)
            print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            #print("The SQLite connection is closed")

readSqliteTable()
