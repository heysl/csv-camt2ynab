#!/usr/bin/python
# -*- coding: utf-8 -*-
#Konvertiere SpaKa-CSV in YNAB CSV:
from __future__ import print_function
import csv
from sys import argv, version_info
from datetime import date


scriptname, csv_input = argv


#dynamischer Dateiname:
today = date.today()
csv_output = "Import_" + str(today.day) + "_" + str(today.month) + "_" + str(today.year) + ".csv"

#Quelldatei:
if version_info[0] < 3:
	infile = open(csv_input, 'rb')
else:
	infile = open(csv_input, 'r')
# a, b, c, d, e, f, g, h, i, j, k
#"Auftragskonto";"Buchungstag";"Valutadatum";"Buchungstext";"Verwendungszweck";"Beguenstigter/Zahlungspflichtiger";"Kontonummer";"BLZ";"Betrag";"Waehrung";"Info"
reader = csv.reader(infile, delimiter = ';', quotechar ='"')

#Zieldatei:
if version_info[0] < 3:
	outfile = open(csv_output, 'wb')
else:
	outfile = open(csv_output, 'w')
writer = csv.writer(outfile)

#Header aus Quelldatei ignorieren:
next(reader, None)

#Header schreiben:
#Date,Payee,Category,Memo,Outflow,Inflow
writer.writerow( ('Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow') )

#Zeilen schreiben:
i = 0
for row in reader:
	i = i+1
	#Spalten der SpaKa-csv mappen:
	col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16, col17 = map(str, row)

	#************ Konvertieren der Spalten ************
	#Datumsformat (hier string) anpassen:
	date = col2.replace('.', '/')
	payee = col12.replace(',', ' ')
	category = ''
	memo = col5
	#YNAB braucht amerikanisches Waehrungsformat:
	betrag = col15.replace(',', '.')
	#Wert in Quell-Spalte "Betrag" aufteilen in die Spalten "Outflow" (wenn negativ) und "Inflow" (wenn positiv):
	if betrag[0] == '-':
		outflow = betrag.replace('-', '')
		inflow = ''
	else:
		outflow = ''
		inflow = betrag
	#************ ************ ************ ************
	#Nur in der YNAB-csv benoetigten Spalten:
	writer.writerow([date, payee, category, memo, outflow, inflow])


#Dateien freigeben:
infile.close()
outfile.close()
#print("Done! Wrote %d Columns to File: %s") % (i, csv_output)
print("Done!")
