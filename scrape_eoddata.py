#This scrapes symbols from eoddata.com/stocklist/NYSE/

import sys
import requests
from bs4 import BeautifulSoup

#Collect data from website
address = 'http://eoddata.com/stocklist/NYSE/A.htm'

r = requests.get(address)

soup = BeautifulSoup(r.content)

table = soup.find(id="ctl00_cph1_divSymbols")

headers = table.find('tr')

if 'CodeNameHighLowCloseVolumeChange' not in headers.text:
	print 'Error detected.'
	sys.exit()



#Put data into 2D array
stockValues = [[] for i in range(7)]

scrapeValue = table.findNext('td')

while scrapeValue.text != 'AZZ':
	for i in range(7):
		stockValues[i].append(scrapeValue.text)
		scrapeValue = scrapeValue.findNext('td')

	print scrapeValue.text
	scrapeValue = scrapeValue.findNext('td')
	print scrapeValue.text
	scrapeValue = scrapeValue.findNext('td')
	print scrapeValue.text
	scrapeValue = scrapeValue.findNext('td')
	print scrapeValue.text

for i in stockValues:
	print i
print 'Process complete.'

