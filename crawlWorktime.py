#! python3
'''

prepare todo:
  * pip3 install selenium
  * pip3 install bea
  1 cp chromedriver to /usr/local/bin

Created on 2018撟�11���29�
@author: kevin.shih
'''
import time
import datetime
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from bs4 import BeautifulSoup
import lineTool
import os
import switchWifi


username = "xxx"
password = 'xxx'

lineNotifyToken = 'xxx'

showBrowser = False

def main():
    doCrawl()
    

def doCrawl():

    if showBrowser:
        driver = webdriver.Chrome("D:\chromedriver")
    else:
        option = webdriver.ChromeOptions()
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('headless')
        option.add_argument('blink-settings=imagesEnabled=false')
        option.add_argument('--disable-gpu')
        #driver = webdriver.Chrome("/home/kevin.shih/chromedriver_linux64/chromedriver", chrome_options=option) # in crontab, i need to tell the chromedriver where it is
        driver = webdriver.Chrome("D:\chromedriver", chrome_options=option) # in crontab, i need to tell the chromedriver where it is

    #switchWifi.doSwithWifi("EHS-3-1-Room")

    driver.get('https://hr.ehsn.coxxx') 

    time.sleep(1)
    
    elem = driver.find_element_by_name('IWEDIT1')
    elem.send_keys(username) 

    time.sleep(1)

    
    # �璅������銝��������撠��蔭 嚗�府��頂蝯梁�����
    driver.find_element_by_id('IWLABEL1').click()
    time.sleep(0.5)
    
    elem = driver.find_element_by_name('IWEDIT2')
    elem.send_keys(password + Keys.RETURN)
    
    time.sleep(1)
    # ���閰� click
    driver.find_element_by_id('IWBUTTONF').click()

    # # ���� html 閫����
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    #switchWifi.doSwithWifi("ETzone")
    
    trs = soup.find(id="IWDBGRID1").findAll("tr")
    tds = trs[-1].findAll("td")
    
    date = tds[3].text.strip()
    onTime = tds[5].text.strip()
    #offTime = tds[7].text.strip()
    #workHour = tds[8].text.strip()
    
    today = str(int(datetime.datetime.now().strftime('%Y')) - 1911) + datetime.datetime.now().strftime('/%m/%d')
    
    # ���������
    if date != today:
        print("warning today is {}, but last date is {}".format(today, date))
    
    msg = "{} 今早打卡時間 {}".format(today, onTime)
    lineTool.lineNotify(lineNotifyToken, msg)
    print(msg)
    
    driver.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        lineTool.lineNotify(lineNotifyToken, e)

