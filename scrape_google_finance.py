#This scrapes balance sheet information from Google Finance

import sys
import sqlite3
import requests
from bs4 import BeautifulSoup

scrapedSheet = []
sheetList = [[]]

#Scrape data
address = 'https://www.google.com/finance?fstype=ii&q=nasdaq:aapl'
r = requests.get(address)
soup = BeautifulSoup(r.content)

#The table I'm interested in is the third one with id='fs-table', that's why I find the first one and then findNext two more times
table = soup.find(id="fs-table").findNext(id='fs-table').findNext(id='fs-table')

scrapedSheet.append('AAPL')
header = table.find('tr').findNext('tr').findNext('td')

if 'Cash & Equivalents' not in header.text:
	print 'Error detected, ending script.'
	sys.exit()

scrapedValue = header.findNext('td')
scrapedSheet.append(scrapedValue.text)
#The last row that needs to be scraped is 'Total Common Shares Outstanding', which is why the loop stops there
while 'Total Common Shares Outstanding' not in scrapedValue.text:
	scrapedValue = scrapedValue.findNext('tr')
	scrapedSheet.append(scrapedValue.findNext('td').findNext('td').text)

#There should be 43 elements in scrapedSheet, otherwise something went wrong
if len(scrapedSheet) != 43:
	print '43 balance sheet elements not found, ending script.'
	sys.exit()

print 'Process complete.'
