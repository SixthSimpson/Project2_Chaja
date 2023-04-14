#!/usr/bin/env python
#Place above so you don't have to call python from commandline
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename", type=argparse.FileType('r'), help="files to process")
parser.add_argument("xytech", type=argparse.FileType('r'), help="files to process")
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
        sub_folder = current_folder.replace("/images1/starwars", "")
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
    xytech_folders = []
    for line in args.xytech:
        if "/" in line:
            xytech_folders.append(line)
    print(xytech_folders)

    new_location =[]
    for line in args.filename:
        line_parse = line.split(" ")
        current_folder = line_parse.pop(0)
        sub_folder = current_folder.replace("/images1/starwars", "")
        new_location = ""
        # Folder replace check
        for xytech_line in xytech_folders:
            if sub_folder in xytech_line:
                new_location = xytech_line.strip()

    print("not verbose")