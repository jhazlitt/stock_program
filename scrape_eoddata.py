#This scrapes symbols from eoddata.com/stocklist/NYSE/

import sys
import requests
from bs4 import BeautifulSoup

stockValues = [[] for i in range(7)]

alphabet = 'abcdefghijklmnopqrstuvwxyz'

for letter in alphabet:

	#Collect data from website
	address = 'http://eoddata.com/stocklist/NYSE/' + letter + '.htm'

	r = requests.get(address)

	soup = BeautifulSoup(r.content)

	table = soup.find(id="ctl00_cph1_divSymbols")

	headers = table.find('tr')

	if 'CodeNameHighLowCloseVolumeChange' not in headers.text:
		print 'Error detected.'
		sys.exit()

	#Put data into 2D array
	scrapeValue = table.findNext('td')

	#The first value after the table is "MEMBER LOGIN", so stop when we have scraped that far
	while scrapeValue.text != 'MEMBER LOGIN':
		for i in range(7):
			stockValues[i].append(scrapeValue.text)
			scrapeValue = scrapeValue.findNext('td')

		scrapeValue = scrapeValue.findNext('td')
		scrapeValue = scrapeValue.findNext('td')
		scrapeValue = scrapeValue.findNext('td')

for i in stockValues:
	print i

print 'Process complete.'

