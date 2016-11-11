#!/usr/bin/python

import psycopg2
from psycopg2.extensions import AsIs

try:
    conn = psycopg2.connect("dbname='fruits' user='python' host='172.20.21.192' password='qwe123'")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()
cur2 = conn.cursor()
try:
     #cur2.execute("""SELECT * from fruits_stat""")
     cur.execute("select column_name from information_schema.columns where table_schema = 'public' and table_name='fruits_stat'")
     	
except:
    print "I can't do the select!"

print "\nShow me the databases:"


#cur2.execute("""SELECT * from fruits_stat""")

#rows = cur2.fetchall()
#for row in rows:
#    print row

column_names = [row[0] for row in cur]
cur.close()
for row in column_names:
    cur2.execute("""SELECT %s from fruits_stat""",[AsIs(row)])
    rows = cur2.fetchall()
    mystring = ' '.join(map(str, (rows)))
    print mystring
#    for row1 in rows:
#	row1=row1[:-1]
#	print row1
    print row+" "+str(rows)
cur2.close()

cur3 =  conn.cursor()
cur3.execute("""SELECT apple from fruits_stat""")
res = cur3.fetchall()
#print res
cur3.close()
