#This scrapes symbols from eoddata.com

import sys
import sqlite3
import requests
from bs4 import BeautifulSoup

scrapedStock = []
stockList = [[]]

#Scrape data by looping through all stock exchanges on eoddata, and each letter in each of those exchanges 
stockExchanges = ['NYSE','AMEX','NASDAQ']
for exchange in stockExchanges:
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	for letter in alphabet:
		address = 'http://eoddata.com/stocklist/' + exchange + '/' + letter + '.htm'

		r = requests.get(address)

		soup = BeautifulSoup(r.content)

		table = soup.find(id="ctl00_cph1_divSymbols")

		headers = table.find('tr')

		if 'CodeNameHighLowCloseVolumeChange' not in headers.text:
			print 'Table does not have the expected headers.  Stopping script.'
			sys.exit()

		#Put data into 2D array
		scrapeValue = table.findNext('td')

		#The first value after the table is "MEMBER LOGIN", so stop when we have scraped that far
		while scrapeValue.text != 'MEMBER LOGIN':
			scrapedStock.append(exchange)
			for i in range(7):
				scrapedStock.append(scrapeValue.text)
				scrapeValue = scrapeValue.findNext('td')
			
			stockList.append(scrapedStock)
			scrapedStock = []

			scrapeValue = scrapeValue.findNext('td')
			scrapeValue = scrapeValue.findNext('td')
			scrapeValue = scrapeValue.findNext('td')

stockList.pop(0)

conn = sqlite3.connect('/home/john/stock_database.db')
c = conn.cursor()
for stock in stockList:
	c.execute('insert into symbols values (?,?,?,?,?,?,?,?)',stock)

conn.commit()
print 'Process complete.'

