#-*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "lxml", from_encoding="utf-8")
        title = bsObj.title
    except AttributeError as e:
        return None
    return title

def getHTML(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "lxml", from_encoding="utf-8")
        document = bsObj.html
    except AttributeError as e:
        return None
    return document

title = getTitle("http://www.pythonscraping.com/pages/page1.html")
document = getHTML("http://www.naver.com")
if title == None:
    print("Title could not be found")
else:
    print(document.prettify())
