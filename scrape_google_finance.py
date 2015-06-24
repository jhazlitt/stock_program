#This scrapes balance sheet information from Google Finance

import string
import sys
import sqlite3
import requests
from bs4 import BeautifulSoup

scrapedSheet = []
sheetList = [[]]

conn = sqlite3.connect('/home/john/stock_database.db')
c = conn.cursor()

codeList = c.execute('select exchange, code from symbols;')

for item in codeList:
	scrapedSheet = []
	exchange = str(item[0])
	code = str(item[1])
	print exchange
	print code
	address = 'https://www.google.com/finance?fstype=ii&q=' + exchange + ':' + code + ''
	r = requests.get(address)
	soup = BeautifulSoup(r.content)
#
#	#The table I'm interested in is the third one with id='fs-table', that's why I find the first one and then findNext two more times
	try:
		table = soup.find(id="fs-table").findNext(id='fs-table').findNext(id='fs-table')
	except:
		print 'Table error.'
		continue

	scrapedSheet.append(code)
	header = table.find('tr').findNext('tr').findNext('td')

	try:
		if 'Cash & Equivalents' not in header.text:
			print 'Error detected, ending script.'
			sys.exit()
	except:	
		print 'Cash & Equivalents not found.'
		continue
	
	scrapedValue = header.findNext('td')
	stringValue = str(scrapedValue.text)
	stringValue = stringValue.replace(',','')
	scrapedSheet.append(stringValue)
	#The last row that needs to be scraped is 'Total Common Shares Outstanding', which is why the loop stops there
	while 'Total Common Shares Outstanding' not in scrapedValue.text:
		scrapedValue = scrapedValue.findNext('tr')
		stringValue = str(scrapedValue.findNext('td').findNext('td').text)
		stringValue = stringValue.replace(',','')
		scrapedSheet.append(stringValue)

	#There should be 43 elements in scrapedSheet, otherwise something went wrong
	if len(scrapedSheet) != 43:
#		print '43 balance sheet elements not found, ending script.'
#		sys.exit()
		print 'len is not 43'
		continue
	
	print scrapedSheet
	sheetList.append(scrapedSheet)
sheetList.pop(0)

for balanceSheet in sheetList:
	c.execute('insert into balance_sheets values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',balanceSheet)

conn.commit()
print 'Process complete.'
