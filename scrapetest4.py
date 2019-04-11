# -*- coding=utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# 서버 인증서를 무시하기 위한 초기화 작업
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon", context=ctx)
bsObj = BeautifulSoup(html, "lxml", from_encoding='utf-8')
for link in bsObj.find("div", {"id":"bodyContent"}).find_all("a", href=re.compile(r"^(/wiki/)((?!:).)*$")):
    if 'href' in link.attrs:
        print(link.attrs['href'])
