#!/usr/bin/env python
import json
import time
import sqlite3
import sys
import datetime
import argparse

parser = argparse.ArgumentParser(description="Print a list of connected clients for the given")
parser.add_argument("--in", action="store", dest="infile", required=True, help='Input file ')
parameters = parser.parse_args()


epoch_time = int(time.time())
#print("epoch")
#print(epoch_time)
#print("back time")
back_time = (epoch_time-360)
#print(back_time)
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
        cursor.execute(sqlite_select_query,(back_time,))
        records = cursor.fetchall()
        #print("Total rows are:  ", len(records))
        #print("Printing each row")
        for row in records:
            #print("Zero: ", row[4])
            #sniffing = json.dumps(row[14])
            #print(row[14].toJSON())
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
            # list
            for i in jiggadata['kismet.device.base.manuf']:
                whatdevice = whatdevice + i
            # Closing file
            f.close()
            print(row[4],whatdevice)
            #print(sniffing)
            #print("1: ", row[1]) 
            #print("2: ", row[2])
            #print("3: ", row[3])
            #print("4: ", row[4])
            #print("5: ", row[5])
            #print("6: ", row[6])
            #print("7: ", row[7])
            #print("8: ", row[8])
            #print("9: ", row[9])
            #print("10: ", row[10])
            #print("11: ", row[11])
            #print("12: ", row[12])
            #print("13: ", row[13])
            #print("14: ", row[14])
            #y=json(row[14])
            #print(y)
            print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            #print("The SQLite connection is closed")

readSqliteTable()
