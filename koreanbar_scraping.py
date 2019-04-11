# -*- coding: utf-8 -*-
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import re

# 서버 인증서를 무시하기 위한 초기화 작업
#import ssl
#ctx = ssl.create_default_context()
#ctx.check_hostname = False
#ctx.verify_mode = ssl.CERT_NONE

#html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon", context=ctx)

regions = ["강원", "경기", "경남", "경북", "광주", "대구", "대전", "부산", "서울", "세종", "울산", "인천", "전남", "전북", "제주", "충남", "충북"] 

searchRegion = urllib.parse.quote_plus(regions[0])
page = 2
html = urlopen("http://www.koreanbar.or.kr/pages/search/search.asp?sido1="+searchRegion+"&gun1=&dong1=&special1_1=&special1=&searchtype=mname&searchstr=&page="+str(page)+"#url")
bsObj = BeautifulSoup(html, "lxml", from_encoding='utf-8')
#print(bsObj.prettify())
regex = re.compile(r"(fnc_goDetail.*;)")
for line in bsObj.find("tbody").find_all("tr"):
    if regex.search(str(line)) is not None:
        print(line.find("td").get_text(), regex.search(str(line)).group())

scriptList = []

regex = re.compile(r"(fnc_goDetail.*;)")
for line in bsObj.find("tbody").find_all("tr"):
    personalScript = []
    if regex.search(str(line)) is not None:
        personalScript.append(str(line.find("td").get_text()))
        personalScript.append(regex.search(str(line)).group())
        scriptList.append(personalScript)
print(scriptList)