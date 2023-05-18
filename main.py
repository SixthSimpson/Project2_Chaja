#!/usr/bin/env python
#Place above so you don't have to call python from commandline
import csv
import datetime
import os
import argparse
import certifi
import pymongo

myclient = pymongo.MongoClient("mongodb+srv://SixthSimpson:College202023@cluster0.02rh4h3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())

mydb = myclient["Proj2_Database"]
mycol = mydb["container 1"]
mycol2 = mydb["container 2"]


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--files", nargs='+', dest='filename', type=argparse.FileType('r'), help="files to process")
parser.add_argument("-x", "--xytech", type=argparse.FileType('r'), help="files to process", required=True)
parser.add_argument("-v", "--verbose", action="store_true", help="show console output")
parser.add_argument("-o", "--output", action="store_true", help="output to csv/ default to database")

args = parser.parse_args()

# xytech folder handling
xytech_folders = []
for line in args.xytech:
    if "/" in line:
        xytech_folders.append(line)

# go through all files in the input values
for files in args.filename:
    frames = []
    db_parse = files.name.split("_")
    machine = db_parse.pop(0)
    for line in files:
        line_parse = line.split(" ")
        if machine == "Flame":
            current_folder = line_parse.pop(1)
            sub_folder = current_folder
            new_location = ""
        else:
            current_folder = line_parse.pop(0)
            sub_folder = current_folder.replace("/images1/", "")
            new_location = ""

        # Folder replace check
        for xytech_line in xytech_folders:
            if sub_folder in xytech_line:
                new_location = xytech_line.strip()

        first = ""
        last = ""
        pointer = ""
        for numeral in line_parse:
            # Skip <err> and <null>
            if not numeral.strip().isnumeric():
                continue
            # Assign first number
            if first == "":
                first = int(numeral)
                pointer = first
                continue
            # Keeping to range if succession
            if int(numeral) == (pointer + 1):
                pointer = int(numeral)
                continue
            else:
                # Range ends or no succession, output
                last = pointer
                if first == last:
                    str = ("%s %s" % (new_location, first))
                    frames.append(str)
                else:
                    str = ("%s %s-%s" % (new_location, first, last))
                    frames.append(str)
                first = int(numeral)
                pointer = first
                last = ""
            # Working with last number each line
        last = pointer
        if first != "":
            if first == last:
                str = ("%s %s" % (new_location, first))
                frames.append(str)
            else:
                str = ("%s %s-%s" % (new_location, first, last))
                frames.append(str)

    ##tear apart the file name and seperate the machine, user, and the date split the extension into a tuple
    user = db_parse.pop(0)
    d = db_parse.pop(0)
    d1 = os.path.splitext(d)
    date = d1[0]
    sub_date = datetime.datetime.now()
    uid = os.uname().nodename

    if args.output:
        # csv file beginning
        csv_file = 'output.csv'
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Machine', 'User on File', 'Date of File', 'Submitted Date'])
            writer.writerow([machine, user, date, sub_date])
            writer.writerow(['Location and Frames to Fix'])

            for frame in frames:
                writer.writerow(['"' + frame + '"'])

    # put in a col and insert to DB
    mydict1 = {"script runner: ": uid, "machine": machine, "user": user, "date": date, "submitted date": sub_date}
    x = mycol.insert_one(mydict1)

    mydict2 = {"user": user, "date": date, "frames to fix": frames}
    x = mycol2.insert_one(mydict2)

    if args.verbose:
        db_parse = files.name.split("_")
        machine = db_parse.pop(0)
        user = db_parse.pop(0)
        d = db_parse.pop(0)
        d1 = os.path.splitext(d)
        date = d1[0]
        sub_date = datetime.datetime.now()

        # test that data is being stored correctly
        print(machine)
        print(user)
        print(date)
        print(sub_date.strftime("%c"))
        print(uid)
        for frame in frames:
            print(frame)
"""
#query for TDanza work
user = "TDanza"
work1 = []

query = {"user": user}
result1 = mycol2.find(query)

for result in result1:
    work1 += result["frames to fix"]

for x in work1:
    print(x)

#query for stuff before 20230325


#query for usernames for flame users only
query = {"machine": "Flame"}
results4 = mycol.find(query)
# Iterate over the results and print each document
for result in results4:
    if result["machine"] == "Flame":
        print("User: " + result["user"])
"""
