# -*- coding: utf-8 -*-
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
import re

#TEST_URL = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'

headless = 0 # Headless Chrome ?
if (headless):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    options.add_argument("lang=ko_KR")  # 한국어!
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
else:
    driver = webdriver.Chrome("./chromedriver.exe")

''' driver.get(TEST_URL)
driver.execute_script(
    "Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
driver.execute_script(
    "Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
driver.execute_script(
    "const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")

user_agent = driver.find_element_by_css_selector('#user-agent').text
plugins_length = driver.find_element_by_css_selector('#plugins-length').text
languages = driver.find_element_by_css_selector('#languages').text
webgl_vendor = driver.find_element_by_css_selector('#webgl-vendor').text
webgl_renderer = driver.find_element_by_css_selector('#webgl-renderer').text
print('User-Agent: ', user_agent)
print('Plugin length: ', plugins_length)
print('languages: ', languages)
print('WebGL Vendor: ', webgl_vendor)
print('WebGL Renderer: ', webgl_renderer)
 '''

regions = ["강원", "경기", "경남", "경북", "광주", "대구", "대전", "부산", "서울", "세종", "울산", "인천", "전남", "전북", "제주", "충남", "충북"] 

searchRegion = urllib.parse.quote_plus(regions[1])
page = 1

target_URL = "http://www.koreanbar.or.kr/pages/search/search.asp?sido1="+searchRegion + \
    "&gun1=&dong1=&special1_1=&special1=&searchtype=mname&searchstr=&page=" + \
    str(page)+"#url"

driver.get(target_URL)
#html = driver.page_source
#bsObj = BeautifulSoup(html, "lxml", from_encoding='utf-8')

#driver.find_element_by_xpath('//*[@id="rightW"]/div[2]/table/tbody/tr[1]/td[3]/a[2]').click()

#print(bsObj.prettify())
#print(bsObj.find("tbody").find_all("tr"))
#for personal_detail in bsObj.find("div", {"id":"detailInfo"}).find_all("td"):
#    if personal_detail is not None:
#        print(' '.join(personal_detail.get_text().split()))

#detailHeader = driver.find_elements_by_tag_name("th")
#for item in detailHeader:
#    print(item.text)

#detailLawyer = driver.find_elements_by_tag_name("td")
#for item in detailLawyer:
#    print(item.text)


personalDataList = []

script = "fnc_goDetail('+L8uE7Yhyy9WdB9E8JNm9w==');"
driver.execute_script(script)
driver.implicitly_wait(3)
html = driver.page_source
bsObj = BeautifulSoup(html, "lxml", from_encoding='utf-8')

index = 1
detailLawyer = []
while(index):
    detailLawyer = driver.find_elements_by_xpath('//*[@id = "detailInfo"]/div[1]/table/tbody/tr['+str(index)+']/td')
    for dl in detailLawyer:
        personalDataList.append(dl.text)
    if len(detailLawyer): 
        index += 1
    else:
        index == 0

driver.quit()



