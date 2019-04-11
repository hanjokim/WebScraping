# -*- coding: utf-8 -*-
from urllib.request import urlopen
from urllib.request import HTTPError
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
from timer import *
import re
import os, csv, sys, time
#import datetime

def initPage(headless):
#    global driver
    if (headless):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("--disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        options.add_argument("lang=ko_KR")  # 한국어!
        driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    else:
        driver = webdriver.Chrome("./chromedriver.exe")
    #    driver.maximize_window()
    return driver

def generateURL(region, page):
    searchRegion = urllib.parse.quote_plus(region)
    urlString = "http://www.koreanbar.or.kr/pages/search/search.asp?sido1=" + searchRegion + \
        "&gun1=&dong1=&special1_1=&special1=&searchtype=mname&searchstr=&page=" + str(page)+"#url"
    return urlString


def getPersonalData(targetURL, index, script):
    global driver
    scriptNumber = script[0]
    scriptName = script[1]
    scriptString = script[2]
    
    personalID = []
    personalDataList = []
#    URL = targetURL
#    HTML = urlopen(URL)

    personalID.append(scriptNumber)
    personalID.append(scriptName)
    driver.execute_script(scriptString)
    driver.implicitly_wait(time_to_wait)
    #html = driver.page_source

    detailLawyer = []
    for index in range(1, 12):
        try:
            detailLawyer = driver.find_elements_by_xpath('//*[@id = "detailInfo"]/div[1]/table/tbody/tr['+str(index)+']/td')
            driver.implicitly_wait(time_to_wait)
        except HTTPError as err:
            print(err.code)
            driver.quit()

        if len(detailLawyer) != 0: 
            index += 1
        else:
            break
        for dl in detailLawyer:
            personalDataList.append(str(';'.join(str(dl.text).split('\n'))))
    
    driver.refresh()
    driver.implicitly_wait(time_to_wait)
    return (personalID + personalDataList)

def getScriptList():
    global bsObj
    global page
    global endOfPageList
    scriptList = []

    if endOfPageList: 
        return None

    regex = re.compile(r"(fnc_goDetail.*;)")
    pageContents = bsObj.find("tbody").find_all("tr")
    if len(pageContents) == 0 :
        endOfPageList = True
        return None

    for line in pageContents:
        personalScript = []
        if regex.search(str(line)) is not None:
            personalScript.append(str(line.find("td").get_text()))
            personalScript.append(str(line.find("a").get_text()))
            personalScript.append(regex.search(str(line)).group())
            scriptList.append(personalScript)


    return scriptList


'''
main routine
'''
if __name__ == "__main__":
       # primary variables
    time_to_wait = 13
    regions = ["강원", "경기", "경남", "경북", "광주", "대구", "대전", "부산", "서울", "세종", "울산", "인천", "전남", "전북", "제주", "충남", "충북"] 
    regionNo = 8
    page = 1626
    dataFolder = './WebScraping/'
    dataHeader = ["번호", "이름(목록)", "이름(상세)", "이름(한자)", "생년월일", "소속회", "자격시험", "사무소명", "사무실전화", "사무실팩스", "사무실주소", "이메일", "전문분야"]
    endOfPageList = False
    headless = 1 # Headless Chrome ?
   
    # define data filename
    if not os.path.isdir(dataFolder):
        dataFolder = './'
    csvFileName = dataFolder + regions[regionNo] + '.csv'
    for trial in range(100):
        if os.path.isfile(csvFileName):
            csvFileName = dataFolder + regions[regionNo] + "{0:0>3}".format(trial) + '.csv'
            if trial == 99:
                print("Error: Too many CSV files with same name")
                sys.exit(1)
        else:
            break
    f = open(csvFileName, 'w', encoding='utf-8', newline='')
    csvWriter = csv.writer(f, delimiter=',')
    if page == 1:
        csvWriter.writerow(dataHeader)

    # start timer
    totalTimer = Timer()
    instantTimer = Timer()

    driver = initPage(headless)

    while not endOfPageList:
        target_URL = generateURL(regions[regionNo], page)
        target_HTML = urlopen(target_URL)
        bsObj = BeautifulSoup(target_HTML, "lxml", from_encoding='utf-8')
        driver.get(target_URL)

        scriptList = getScriptList()

        print(">>> Start of Page #", page)
        instantTimer.restart()

        if endOfPageList:
            print("-------------------------\n>>> End of Page : ", page)
            break

        for index in range(len(scriptList)):
            try:
                personalData = getPersonalData(target_URL, index, scriptList[index])
                print(personalData)
                csvWriter.writerow(personalData)
            finally:
                pass
        
        print(">>> End of Page #", page)
        print(">>> Elapsed time for currnet page : ", instantTimer.get_time_hhmmss())
        print(">>> Elapsed time until currnet page : ", totalTimer.get_time_hhmmss())
        time.sleep(time_to_wait)
        page += 1
   
    # get time
    print(">>> Total elapsed time : ", totalTimer.get_time_hhmmss())
    f.close()
    driver.quit()
