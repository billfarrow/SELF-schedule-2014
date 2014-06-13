#!/usr/bin/python

# Copyright 2014 Bill Farrow <bill.farrow@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv
import sys
from string import Template
import cgi

# Write out html snippets to these files
fsession = open('sessions.txt', 'w')
fspeaker = open('speakers.txt', 'w')

# Look up data used to fill in the html tables
sColor = ['grey', 'green', 'orange', 'blue', 'rust', 'red']
sTime = ['9:00 - 10:00', '10:15 - 11:15', '11:30 - 12:30', '12:30 - 1:30', '1:30 - 2:30', '2:45 - 3:45', '4:00 - 5:00', '5:15 - 6:15']

# Templates for the html snippets
tsessionTime = Template('\n</tr>\n<tr>\n<td class="event gray">${time}</td>\n')
tsession = Template('<td class="event ${color}">${topic}<br/><br/><a href="speakers.html#${ref}" title="${speaker}">${speaker}</a></td>\n')
tspeaker = Template('''\
		<h2 class="acc_trigger"><a href="#" name="${ref}">${speaker}</a></h2>
		<div class="acc_container"> 
			<div class="block">
				<p><strong>Title:</strong> ${title}</p>
				<p><strong>Bio:</strong> ${bio}</p>
				<p><strong>Presenting Topic:</strong><u>"${topic}"</u></p>
				<p>${desc}</p>
				<p><strong>Audience:</strong> ${purpose}</p>
			</div>
		</div>\n\n\
''')

print 'Processing SELF RFP CSV file and generating html snippet'
print ' files sessions.txt and speakers.txt for manual editing\n'

# Open the CSV file from Google Drive
with open(sys.argv[1], 'rb') as csvfile:
	skip_header = True
	cTime = 0;
	cTimeCount = 0;
	cSkipCount = 0;
#	skip_header = csv.Sniffer().has_header(csvfile.read(1024))
#	dialect = csv.Sniffer().sniff(csvfile.read(1024))
	dialect = csv.excel
	print dialect
	csvfile.seek(0)
	rfpdata = csv.reader(csvfile, dialect)
	for row in rfpdata:
		if skip_header == True:
			skip_header = False
			continue

		# Extract the info we need from the spreadsheet row
		sSpeaker = cgi.escape(row[0])
		sTopic = cgi.escape(row[1])
		sSlot = row[2]
		sRoom = row[3]
		sDesc = cgi.escape(row[4])
		sPosition = cgi.escape(row[5])
		sBio = cgi.escape(row[6])
		sPurpose = cgi.escape(row[7])

		# If the talk has been allocated a slot, then create html snippets for it
		# If this row is the start of a new time slot, create a new html row
		if sSlot.isdigit() == False:
			cSkipCount += 1
			print 'Skipping Slot ' + sSlot +' : ' + sSpeaker + ' - ' + sTopic
			continue
		
		if cTime != int(sSlot) -1:
			cTime = (int(sSlot) - 1)%8
			print 'cTime = ' + str(cTime) + ' sSlot = ' + sSlot + ' count = ' + str(cTimeCount)
			fsession.write(tsessionTime.substitute(time=sTime[cTime]))
			cTime = int(sSlot) -1
			cTimeCount = 0

		# If the talk has been assigned a room, create the html session table data
		if sRoom.isdigit() and int(sRoom) > 0:
			fsession.write(tsession.substitute(topic=sTopic, ref=sSpeaker.translate(None, ' '),
				speaker=sSpeaker, color=sColor[int(sRoom)]))
			cTimeCount += 1

		# Write out the speakers info, bio, and talk synopsis
		fspeaker.write(tspeaker.substitute(topic=sTopic, ref=sSpeaker.translate(None, ' '), speaker=sSpeaker,
			title=sPosition, bio=sBio, desc=sDesc, purpose=sPurpose))
		
	print 'Skipped ' + str(cSkipCount) + ' unassigned talks\n'
