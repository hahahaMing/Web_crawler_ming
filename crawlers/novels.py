#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/22 10:39
# @Author  : Eiya_ming
# @Email   : eiyaming@163.com
# @File    : novels.py

##总结同一个小说网站的爬取方法，这样以后爬取小说只需修改网站中的小说编码即可
# 建立类的方法依据页面配置，一个方法对应一个页面，一个页面尽量只访问一次
import requests
import os
import re
import pickle
import time


## 笔趣阁 http://m.biquge.info/
class biquge():

    def __init__(self, novel_number):
        self.novel_number = novel_number
        self.demo_manu_page_url = "http://www.biquge.info/" + novel_number
        self.novel_name = ""
        self.chapter_url_list = []
        self.file_path = ""
        self.content = ""
        self.ad_strs = []
        self.last_success_log_path = ""

    def get_str_from_jumps(self, url):
        r = requests.get(url, verify=False)
        s = r.text.encode(r.encoding).decode('utf-8')
        rst = "http://www.biquge.info"
        if "window.location" in s:
            rst = self.get_str_from_jumps(rst + s.split('window.location=')[1].split('"')[1])
        return s

    def demo_manu_page_work(self):
        """
        使用 demo_manu_page_url
        得到：
        小说的名字
        小说的目录页的列表
        小说的总章节数
        :return:
        """
        # r = requests.get(self.demo_manu_page_url, verify=False)
        s = self.get_str_from_jumps(self.demo_manu_page_url)
        print(s)

        # 小说的名字
        tmp = re.findall('<meta property="og:title" content=.*/>', s)
        self.novel_name = tmp[0].split('"')[-2]
        print(self.novel_name)
        self.file_path = 'results/' + self.novel_name + '.txt'
        self.last_success_log_path = 'temp/' + self.novel_number + '.pkl'
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

    def text_page_work(self, chapter_url):
        # r = requests.get(chapter_url, verify=False)
        # s = r.text.encode('ISO-8859-1').decode('utf-8')

        s = self.get_str_from_jumps(chapter_url)
        print("web got.")
        # print(s)

        # 章节名
        try:
            title = s.split('<h1>')[1].split('</h1>')[0]
        except:
            print(s)
        # print(title)
        # self.content = self.content + title + '\n'
        print('title got.')
        content = s.split("<!--go-->")[1].split('<!--over-->')[0]
        content = content.replace('&nbsp;', ' ')
        content = content.replace('<br/><br/>', '\n\n')
        content = self.ad_blocking(content)
        print('content got.')
        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(title + '\n')
            f.write(content + '\n')
            print('write done.')
        # self.content = self.content + content
        # print(content)

    def ad_blocking(self, s):
        ad_dic = ["笔、趣、阁www。biquge。info",
                  "笔％趣％阁www.biｑｕge.info",
                  "笔《趣》阁wｗw.ｂｉquｇｅ.ｉｎｆｏ",
                  ]
        for ad in ad_dic:
            s = s.replace(ad, "")

        return s

    def main_crawler(self):

        # 断点续传


        # 存 目录对应url列表到json文件
        # 存 上次卡住的位置
        # 如果存在断点文件与json文件，就续传一下，否则开新文件
        chapter_count = 0
        average_time = 0
        self.demo_manu_page_work()
        resume = False
        if os.path.exists(self.last_success_log_path):
            resume = True
            print("读取到现有的json文件。")
            with open(self.last_success_log_path, 'rb')as f:
                last_page_info, last_chapter_url = pickle.load(f)
                print('读取文件：' + self.last_success_log_path)
        rest_chapter_num = len(self.chapter_url_list)

        for page_info, chapter_url in self.chapter_url_list:
            if resume:
                if last_page_info == page_info and last_chapter_url == chapter_url:
                    resume = False
                else:
                    continue
            else:
                print(page_info + ">>>>>>章节页处理中")

                time_start = time.time()

                while True:
                    try:
                        self.text_page_work(chapter_url)
                        print(page_info + "<<<<<<" + chapter_url + ">>>>>>章节页处理成功！！！！！！！！！！！！！")

                        time_end = time.time()
                        average_time = (average_time * chapter_count + time_end - time_start) / (chapter_count + 1)
                        chapter_count += 1
                        rest_time_prediction = average_time * (rest_chapter_num - 1)
                        print('本章用时：', time_end - time_start, '; 预计剩余时间：', rest_time_prediction, '.')
                        # 存本次写成功对应list的位置
                        with open(self.last_success_log_path, 'wb')as f:
                            pickle.dump([page_info, chapter_url], f, True)
                        break
                    except:
                        print(page_info + "<<<<<<" + chapter_url + ">>>>>>章节页处理失败！！！！！！！！！！！！！")

            rest_chapter_num -= 1
