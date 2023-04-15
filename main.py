#!/usr/bin/env python
#Place above so you don't have to call python from commandline
import csv
import time
import os
import argparse
import pymongo

myclient = pymongo.MongoClient("mongodb+srv://SixthSimpson:College202023@cluster0.02rh4h3.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["Proj2_Database"]
mycol = mydb["container 1"]
mycol2 = mydb["container 2"]


parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=argparse.FileType('r'), help="files to process")
parser.add_argument("--xytech", type=argparse.FileType('r'), help="files to process")
parser.add_argument("--verbose", action="store_true", help="show verbose")

args = parser.parse_args()
dir = "Work"

#flag for verbose
if args.verbose:
    xytech_folders = []
    for line in args.xytech:
        if "/" in line:
            xytech_folders.append(line)

    for line in args.filename:
        line_parse = line.split(" ")
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
                # Range ends or no sucession, output
                last = pointer
                if first == last:
                    print("%s %s" % (new_location, first))
                else:
                    print("%s %s-%s" % (new_location, first, last))
                first = int(numeral)
                pointer = first
                last = ""
            # Working with last number each line
        last = pointer
        if first != "":
            if first == last:
                print("%s %s" % (new_location, first))
            else:
                print("%s %s-%s" % (new_location, first, last))


#if verbose is not flagged
else:
    #xytech folder handling
    xytech_folders = []
    for line in args.xytech:
        if "/" in line:
            xytech_folders.append(line)

    frames = []
    for line in args.filename:
        line_parse = line.split(" ")
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
                # Range ends or no sucession, output
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
    db_parse = args.filename.name.split("_")
    machine = db_parse.pop(0)
    user = db_parse.pop(0)
    d = db_parse.pop(0)
    d1 = os.path.splitext(d)
    date = d1[0]
    sub_date = time.localtime()

    #test that data is being stored correctly
    print(machine)
    print(user)
    print(date)
    print(','.join(str(x) for x in sub_date))
    # uid = os.getuid()
    # print(uid)

    #put in a col and insert to DB
    mydict1 = {"machine": machine, "user": user, "date": date, "submitted date": sub_date}
    x = mycol.insert_one(mydict1)

    mydict2 = {"user": user, "date": date, "frames to fix": frames}
    x = mycol2.insert_one(mydict2)

    # csv file beggining
    csv_file = 'output.csv'
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Machine', 'User on File', 'Date of File', 'Submitted Date'])
        writer.writerow([machine, user, date, sub_date])
        writer.writerow(['Location and Frames to Fix'])

        for frame in frames:
            writer.writerow(frame)

    for frame in frames:
        print(frame)
    print("not verbose")