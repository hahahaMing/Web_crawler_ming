from operator import le
from numpy import less
import pyautogui
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys  #键盘导入类

OUTPUT_FOLDER = r'D:\SelfStudy\Git\mldn'

driver = webdriver.Chrome()

driver.get("https://www.mldn.cn/my/course/231")

driver.find_element_by_id("login_username").send_keys("19946251182")

driver.find_element_by_id("login_password").send_keys("mldn326033")

driver.find_element_by_xpath("//*[@id=\"login-form\"]/div[4]/button").click()


class ImgHref:
        def __init__(self,pageNum,herf,folderName) -> None:
            self.pageNum = pageNum
            self.herf = herf
            self.folderName = folderName
        def fold(self)->None:
            driver.get(self.herf)
            # TODO: autogui完成右键另存为操作
            pass

class NoteHref:

    def __init__(self, folderName, herf) -> None:
        self.folderName = folderName
        self.herf = herf

    

    def downloadGraphs(self) -> None:
        driver.get(self.herf)
        time.sleep(10)
        # 滚动内部页
        driver.switch_to.frame('task-content-iframe')
        iframe = driver.find_elements_by_tag_name("iframe")[0]
        driver.switch_to.frame(iframe)

        docPlayer = driver.find_element_by_id("page-container")
        print(docPlayer.size)
        driver.execute_script('document.getElementById(\'page-container\').scrollTop=10000')
        # 收集所有图片链接
        imgDivs = driver.find_elements_by_tag_name("img")
        pageCount = 0
        imgHerfs = []
        for imgDiv in imgDivs:
            imgHerfs.append(ImgHref(pageCount,imgDiv.get_attribute("src"),self.folderName))
            print(str(pageCount) + " " + str(imgDiv.get_attribute("src")))

        for imgHerf in imgHerfs:
            imgHerf.fold()


# driver.execute_script('window.scrollBy(0,588)')
count = 0
height = 0
# 滚动以找到所有页面
while True:
    newHeight = driver.execute_script('return document.body.scrollHeight;')
    if newHeight > height:
        driver.execute_script('window.scrollBy(0,1000)')
        time.sleep(0.1)
        height += 1000
    else:
        print("滚动条已经处于页面最下方!")
        break
lessons = driver.find_elements_by_class_name("title")

print(lessons[-1].location)
print(len(lessons))





noteList = []
for lesson in lessons:
    if "【在线笔记】" in lesson.text:
        noteList.append(NoteHref(lesson.text,lesson.get_attribute("href")))
        print(str(count) + " " + str(lesson.get_attribute("href")))
        print(str(count) + " " + str(lesson.text))

        count += 1


for note in noteList:
    note.downloadGraphs()
time.sleep(10)

driver.quit()
