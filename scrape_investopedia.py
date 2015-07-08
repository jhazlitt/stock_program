#This takes stock symbols from the symbols table in stock_database and uses them to construct valid investopedia urls.  It then scrapes the sector and industry values from the urls and inserts them into stock_industry table in stock_database.db

import sys
import sqlite3
import requests
from bs4 import BeautifulSoup

scrapedRow = []
industryList = [[]]
codeList = []

conn = sqlite3.connect('/home/john/stock_database.db')
c = conn.cursor()

codeList = c.execute('select code from symbols;')

for code in codeList:
	code = str(code)
	code = code[3:len(code)-3]
	print code
	
	#Eoddata has some stocks with a dash in them.  Investopedia doesn't know what these are.  If there is a dash in stock code, skip it.
	if '-' in code:
		continue
	#Request the page and find Sector and Industry
	address = 'http://www.investopedia.com/markets/stocks/' + str(code) + '/'
	r = requests.get(address)
	soup = BeautifulSoup(r.content)
	sector = ''
	industry = ''
	for tag in soup.find_all('td','txt'):
		if "Sector: " in tag.text:
			sector = tag.text[8:]
			print sector
		elif "Industry: " in tag.text:
			industry = tag.text[10:]
			print industry
	
	if sector == '' or industry == '':
		print "Error finding data.  Continuing."
		continue

	scrapedRow.append(code)
	scrapedRow.append(sector)
	scrapedRow.append(industry)
	print scrapedRow

#	myInput = input("Press Enter to continue...")
#	if myInput == 'q':
#		exit()

	industryList.append(scrapedRow)
	scrapedRow = []

#For some reason industryList keeps a blank record at the beginning, I just delete it
industryList.pop(0)	

#Insert data into SQL database
conn = sqlite3.connect('/home/john/stock_database.db')
c = conn.cursor()
for scrapedIndustry in industryList:
	c.execute('insert into stock_industry values (?,?,?)',scrapedIndustry)
conn.commit()
print 'Investopedia scrape complete.'

