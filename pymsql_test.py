__author__ = 'Tai-An Chen'
import pymysql
conn = pymysql.connect(host='localhost', port=3306,user='yourUser',passwd='yourPasswd',db='yourDB',charset='UTF8')
cur = conn.cursor()
cur.execute("select version()")
for i in cur:
    print(i)
cur.close()
conn.close()