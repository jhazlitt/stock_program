#This takes stock symbols from the symbols table in stock_database and uses them to construct valid yahoo urls.  It then scrapes the P/E values from the urls and inserts them into stock_pe table in stock_database.db

import sys
import sqlite3
import requests
from bs4 import BeautifulSoup

scrapedRow = []
peList = [[]]
codeList = []

conn = sqlite3.connect('/home/john/stock_database.db')
c = conn.cursor()

codeList = c.execute('select code from symbols;')

for code in codeList:
	code = str(code)
	code = code[3:len(code)-3]
	print code
	
	#Eoddata has some stocks with a dash in them.  Yahoo doesn't know what these are.  If there is a dash in stock code, skip it.
	if '-' in code:
		continue

	address = 'http://finance.yahoo.com/q?s=' + str(code) + ''

	r = requests.get(address)

	soup = BeautifulSoup(r.content)

	table = soup.find(id="table1")
	
	#If table.find('tr') throws an error, that means something is wrong with the stock code or yahoo doesn't have it for some reason.  Skip it.
	try:
		firstValue = table.find('tr')
	except:
		pass

	#This is pretty goofy, it looks through all these rows to find the P/E.  There is probably a better way to write this
	PE = firstValue.findNext('tr').findNext('tr').findNext('tr').findNext('tr').findNext('tr').findNext('tr').findNext('tr').findNext('tr').findNext('tr').findNext('tr').findNext('tr').findNext('tr')

	#Check to make sure PE is actually looking at the P/E row before getting the P/E value
	if 'P/E' not in PE.text:
		print 'Error detected.'
		print code
		print PE.text
		sys.exit()

	PE = PE.findNext('td').text

	scrapedRow.append(code)
	scrapedRow.append(PE)

	print scrapedRow

	peList.append(scrapedRow)
	scrapedRow = []
#conn = sqlite3.connect('/home/john/stock_database.db')
#c = conn.cursor()
#for scrapedPE in peList:
#	c.execute('insert into stock_pe values (?,?,?,?,?,?,?)',stock)
#conn.commit()
print 'Yahoo scrape complete.'

