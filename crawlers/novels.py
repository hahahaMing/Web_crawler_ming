#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/22 10:39
# @Author  : Eiya_ming
# @Email   : eiyaming@163.com
# @File    : novels.py

##总结同一个小说网站的爬取方法，这样以后爬取小说只需修改网站中的小说编码即可
# 建立类的方法依据页面配置，一个方法对应一个页面，一个页面尽量只访问一次
import urllib.request
import requests
import os
import re
import time


## 笔趣阁 http://m.biquge.info/
class biquge():

    def __init__(self, novel_number):
        self.novel_number = novel_number
        self.demo_manu_page_url = "http://www.biquge.info/" + novel_number
        self.novel_name = ""
        self.manu_url_list = []
        self.chapter_url_list = []
        self.file_path = ""
        self.content = ""

        self.chapter_total = 0
        pass

    def demo_manu_page_work(self):
        """
        使用 demo_manu_page_url
        得到：
        小说的名字
        小说的目录页的列表
        小说的总章节数
        :return:
        """
        r = requests.get(self.demo_manu_page_url, verify=False)
        s = r.text.encode('ISO-8859-1').decode('utf-8')
        # ecd = r.encoding
        # print(s)
        # print(ecd)

        # 小说的名字
        tmp = re.findall('<meta property="og:title" content=.*/>', s)
        self.novel_name = tmp[0].split('"')[-2]
        print(self.novel_name)
        self.file_path = 'results/' + self.novel_name + '.txt'
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(self.novel_name + '\n')

        # 小说章节页列表
        tmp = re.findall('<dd><a href=.* title=.*>.*</a></dd>', s)
        # print(tmp)
        for str in tmp:
            tmp_url = "http://www.biquge.info/" + self.novel_number + '/' + str.split('"')[1]
            tmp_tag = str.split('"')[3]
            self.chapter_url_list.append([tmp_tag, tmp_url])
        # print(self.chapter_url_list)

        # # 小说的目录页的列表
        # tmp = re.findall('<option value=.*>.*</option>', s)
        # # print(tmp)
        # for str in tmp:
        #     tmp_url = "http://m.biquge.info/" + str.split('"')[1]
        #     tmp_tag = str.split('>')[1].split('<')[0]
        #     self.manu_url_list.append([tmp_tag, tmp_url])
        # print(self.manu_url_dict)

    def manu_page_work(self, manu_url):
        """
        得到：章节对应 url的 list

        :param manu_url:
        :return:
        """
        # print(manu_url)
        r = requests.get(manu_url, verify=False)
        s = r.text.encode('ISO-8859-1').decode('utf-8')
        # print(s)
        # print("*********************************")
        str_chapters = s.split("<div class=\"intro\">正文</div>")[1].split("</ul>")[0]
        # print(str_chapters)
        tmp = re.findall("<li><a href=.*>.*</a></li>", str_chapters)
        # print(tmp)
        for str_tmp in tmp:
            tmp_url = "http://m.biquge.info" + str_tmp.split('"')[1]
            tmp_tag = str_tmp.split(">")[2].split("<")[0]
            self.chapter_url_list.append([tmp_tag, tmp_url])
        print(self.chapter_url_list)

    def text_page_work(self, chapter_url):
        r = requests.get(chapter_url, verify=False)
        s = r.text.encode('ISO-8859-1').decode('utf-8')
        print("web got.")
        # print(s)

        # 章节名
        title = s.split('<h1>')[1].split('</h1>')[0]
        # print(title)
        # self.content = self.content + title + '\n'
        print('title got.')
        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(title + '\n')

        content = s.split("<!--go-->")[1].split('<!--over-->')[0]
        print('content got.')
        content = content.replace('&nbsp;', ' ')
        content = content.replace('<br/><br/>', '\n\n')
        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(content + '\n')
            print('write done.')
        # self.content = self.content + content
        # print(content)

    def main_crawler(self):
        self.demo_manu_page_work()

        for page_info, chapter_url in self.chapter_url_list:
            print(page_info + ">>>>>>章节页处理中")
            # self.text_page_work(chapter_url)
            # time.sleep(1)
            while (True):
                try:
                    self.text_page_work(chapter_url)
                    break
                except:
                    print(page_info + ">>>>>>章节页处理失败！！！！！！！！！！！！！")

        # file_path = 'results/' + self.novel_name + '.txt'
        # with open(file_path, 'w', encoding='utf-8') as f:
        #     f.write(self.content)
        # self.text_page_work('http://www.biquge.info/11_11245/5249657.html')
