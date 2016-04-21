# coding=utf-8
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import sys
import re
import unicodedata
import time
sys.path.insert(0, '../')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}

""" set unicode """
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

pornstarts=set()

f=open("pornstarts.txt","w")
for i in range(1,15):
    mainlink = "http://www.bignaturals.com/big-boobs/home"
    sublink1="_"
    sublink2=".htm?id=gbat"
    resultlink=""
    if i==1:
        resultlink=mainlink+sublink2
    else:
        resultlink=mainlink+sublink1+str(i)+sublink2

    #get political news link, news link changes everyday
    main_res=requests.get(resultlink,headers=headers)
    soup=BeautifulSoup(main_res.text,"lxml")
    sections=soup.find_all("section")

    for section in sections:
        articles=section.find_all("article",recursive=False)
        for article in articles:
            h5=article.find_all("h5",recursive=False)
            anchors=h5[0].find("a")
            pornstar_name=anchors.contents[0]
            print pornstar_name
            pornstarts.add(pornstar_name)


for pornstar in pornstarts:
    f.write(pornstar+"\n")


f.close()
