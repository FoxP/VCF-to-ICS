#!/usr/bin/env python
# -*- coding: utf-8 -*-

#	##### BEGIN GPL LICENSE BLOCK #####
#
#	This program is free software; you can redistribute it and/or
#	modify it under the terms of the GNU General Public License
#	as published by the Free Software Foundation; either version 2
#	of the License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program; if not, write to the Free Software Foundation,
#	Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#	##### END GPL LICENSE BLOCK #####

#	Name :
#				VCF to ICS
#	Author :
#				▄▄▄▄▄▄▄  ▄ ▄▄ ▄▄▄▄▄▄▄
#				█ ▄▄▄ █ ██ ▀▄ █ ▄▄▄ █
#				█ ███ █ ▄▀ ▀▄ █ ███ █
#				█▄▄▄▄▄█ █ ▄▀█ █▄▄▄▄▄█
#				▄▄ ▄  ▄▄▀██▀▀ ▄▄▄ ▄▄
#				 ▀█▄█▄▄▄█▀▀ ▄▄▀█ █▄▀█
#				 █ █▀▄▄▄▀██▀▄ █▄▄█ ▀█
#				▄▄▄▄▄▄▄ █▄█▀ ▄ ██ ▄█
#				█ ▄▄▄ █  █▀█▀ ▄▀▀  ▄▀
#				█ ███ █ ▀▄  ▄▀▀▄▄▀█▀█
#				█▄▄▄▄▄█ ███▀▄▀ ▀██ ▄

# DEPENDENCIES

from string import ascii_letters
from string import digits
import argparse
import logging
import quopri
import random
import time
import sys
import os
import re

# CONFIGURATION

PROGRAM_NAME = "VCF to ICS"
PROGRAM_VERSION = "1.0"

# Command-line interface
argParser = argparse.ArgumentParser(description=PROGRAM_NAME + " " + PROGRAM_VERSION)
argParser.add_argument('-i', '--input', metavar='PATH', help='Input .vcf file path', required=True)
argParser.add_argument('-o', '--output', metavar='PATH', help='Output .ics file path', required=True)
argParser.add_argument('-n', '--name', metavar='NAME', help='Desired calendar name', required=True)
args = vars(argParser.parse_args())

sInputPath = args['input']
sOutputPath = args['output']
sCalendarName = args['name']

# LOGGING

# Default logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Log to console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

# MAIN PROGRAM

if os.path.isfile(sInputPath):
	logger.info("Input file path : " + sInputPath)
else:
	logger.error("Invalid input file path : " + sInputPath)
	sys.exit(1)

# Read VCF file content
fileInput = open(sInputPath, 'r', encoding='utf-8')
sFileContent = fileInput.read()
fileInput.close()

# Separate VCards
sVCards = sFileContent.split("END:VCARD")
iVCardNbr = 0

# Write ICS calendar header
try:
	fileOutput = open(sOutputPath, 'w', encoding='utf-8')
except:
	logger.error("Invalid output file path : " + sOutputPath)
	sys.exit(1)
else:
	logger.info("Output file path : " + sOutputPath)
fileOutput.write("BEGIN:VCALENDAR\nPRODID:-//" + PROGRAM_NAME + "//NONSGML " + sCalendarName + " V1.0//EN\nX-WR-CALNAME:" + sCalendarName + "\nVERSION:2.0\n")

# Parse VCards
for sVCard in sVCards:
	# "BDAY:--12-01" --> ["BDAY:--12-01", "-", "12", "01"]
	# "BDAY:2018-12-01" --> ["BDAY:2018-12-01", "2018", "12", "01"]
	matchBirthday = re.search("BDAY:(\-|\d+)-(\d+)-(\d+)[\s\S]*?", sVCard)
	# "FN:John Doe" --> ["FN:John Doe", "John Doe"]
	# "FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=4A=6F=68=6E=20=44=6F=65" --> ["FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=4A=6F=68=6E=20=44=6F=65", "=4A=6F=68=6E=20=44=6F=65"]
	matchName = re.search("FN(?:\:|;.*:)(.*)[\s\S]*?", sVCard)
	if (matchBirthday is not None) and (matchName is not None):
		# Contact birthday
		if matchBirthday.group(1) == "-":
			# Replace "-" by current year
			# ["BDAY:--12-01", "-", "12", "01"] --> 20181201
			sBirthday = time.strftime("%Y") + matchBirthday.group(2) + matchBirthday.group(3)
		else:
			# ["BDAY:2018-12-01", "2018", "12", "01"] --> 20181201
			sBirthday = matchBirthday.group(1) + matchBirthday.group(2) + matchBirthday.group(3)
		# Contact name
		try:
			# Try to decode Quoted-Printable
			# ["FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:=4A=6F=68=6E=20=44=6F=65", "=4A=6F=68=6E=20=44=6F=65"] --> "John Doe"
			sName = quopri.decodestring(matchName.group(1)).decode('utf-8')
		except:
			# ["FN:John Doe", "John Doe"] --> "John Doe"
			sName = matchName.group(1)

		logger.info(str(sName) + " : " + str(sBirthday))
		iVCardNbr = iVCardNbr + 1

		# Unique ID
		sUID = sBirthday + "-" + ''.join([random.choice(list(ascii_letters + digits)) for _ in range(16)]) + "@VCFtoICS.com"

		# Write ICS event
		fileOutput.write("BEGIN:VEVENT\nDTSTART:" + sBirthday + "\nSUMMARY:" + sName + "\nRRULE:FREQ=YEARLY\nDURATION:P1D\nUID:" + sUID + "\nEND:VEVENT\n")

if (iVCardNbr > 0):
	logger.info(str(iVCardNbr) + " VCards found")
else:
	logger.info("No VCard found")

# Write ICS calendar footer
fileOutput.write("END:VCALENDAR")
fileOutput.close
