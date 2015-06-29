import sqlite3
queryText = str(open('sql_queries/strategy1.txt').read().splitlines())
queryText = queryText.replace('[\'','')
queryText = queryText.replace('\']','')

conn = sqlite3.connect('/home/john/stock_database.db')
c = conn.cursor()
c.execute(queryText)
queryResults = c.fetchall()
print queryResults
