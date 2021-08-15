'''
Author: your name
Date: 2021-04-12 15:28:46
LastEditTime: 2021-08-15 14:34:06
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Web_crawler_ming\qqq.py
'''
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys    #键盘导入类


browser = webdriver.Firefox()

browser.get("https://www.jd.com/")

browser.find_element_by_xpath("//*[@id=\"ttbar-login\"]/a[1]").click()

sleep(2)

sleep(0)