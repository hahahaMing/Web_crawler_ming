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
import functools


## 笔趣阁 http://m.biquge.info/
class biquge():

    def __init__(self, novel_number):
        """
        初始化一些公共变量
        :param novel_number: 笔趣阁小说编号，在url里有体现。
        """
        self.novel_number = novel_number
        self.demo_manu_page_url = "http://www.biquge.info/" + novel_number
        self.novel_name = ""
        self.chapter_url_list = []
        self.file_path = ""
        self.folder_path = ""
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

    def manu_page_work(self):
        """
        使用 manu_page_url
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
        print("小说名称：", self.novel_name)
        # 建立最终输出文件
        self.file_path = 'results/' + self.novel_name + '.txt'
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(self.novel_name + '\n')
        # 建立临时文件夹
        self.folder_path = 'results/' + self.novel_name
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)

        # 小说章节页列表
        tmp = re.findall('<dd><a href=.* title=.*>.*</a></dd>', s)
        # print(tmp)
        for str in tmp:
            tmp_url = "http://www.biquge.info/" + self.novel_number + '/' + str.split('"')[1]
            tmp_tag = str.split('"')[3]
            self.chapter_url_list.append([tmp_tag, tmp_url])

        # print(self.chapter_url_list)

    def text_page_work(self, chapter_url, tmp_filename):
        # r = requests.get(chapter_url, verify=False)
        # s = r.text.encode('ISO-8859-1').decode('utf-8')

        s = self.get_str_from_jumps(chapter_url)
        print("web got.")
        # 章节名
        title = ''
        try:
            title = s.split('<h1>')[1].split('</h1>')[0]
        except:
            print(s)
        if len(title) == 0:
            print('title got failed.')
        else:
            print('title got.')
        # 处理正文
        content = s.split("<!--go-->")[1].split('<!--over-->')[0]
        content = content.replace('&nbsp;', ' ')
        content = content.replace('<br/><br/>', '\n\n')
        content = content.replace(title, '')
        content = self.ad_blocking(content)
        print('content got.')
        with open(tmp_filename, 'w', encoding='utf-8') as f:
            f.write(title + '\n')
            f.write(content + '\n')
            print('write done.')

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
        # 每一章节形成一个txt文件，总共放在一个文件夹里面，最后再合并
        chapter_count = 0
        average_time = 0
        self.manu_page_work()

        rest_chapter_num = len(self.chapter_url_list)

        for file_id, [page_info, chapter_url] in enumerate(self.chapter_url_list):
            tmp_filename = self.folder_path + '/' + str(file_id) + '.txt'
            # 已经存在本章txt，跳过
            if os.path.exists(tmp_filename):
                with open(tmp_filename, 'r', encoding='utf-8')as f:
                    s = f.read()
                    s = s.replace(page_info, '')
                    if len(s) > 10:
                        print(page_info + ">>>>>>章节已有，跳过。")
                        rest_chapter_num -= 1
                        continue
            # 否则，处理本章节
            print(page_info + ">>>>>>章节页处理中")
            # 计时开始
            time_start = time.time()
            while True:
                try:
                    self.text_page_work(chapter_url, tmp_filename)
                    print(page_info + "<<<<<<" + chapter_url + ">>>>>>章节页处理成功！！！！！！！！！！！！！")
                    rest_chapter_num -= 1
                    time_end = time.time()  # 计时结束
                    average_time = (average_time * chapter_count + time_end - time_start) / (chapter_count + 1)
                    chapter_count += 1
                    rest_time_prediction = average_time * rest_chapter_num
                    print('本章用时：', time_end - time_start, 's, average_time', average_time, 's\nrest_chapter_num,',
                          rest_chapter_num, ', 预计剩余时间：', rest_time_prediction, 's.')
                    break
                except:
                    print(page_info + "<<<<<<" + chapter_url + ">>>>>>章节页处理失败！！！！！！！！！！！！！")

    def add_together(self):
        # 把所有txt拼在一起
        txt_list = os.listdir(self.folder_path)
        l = len(txt_list)
        print(l)
        with open(self.file_path, 'w', encoding='utf-8')as final_f:
            final_f.write('\n')
        with open(self.file_path, 'a', encoding='utf-8')as final_f:
            for i in range(l):
                with open(self.folder_path + '/' + str(i) + '.txt', 'r', encoding='utf-8')as f:
                    print(self.folder_path + '/' + str(i) + '.txt')
                    s = f.read()
                    final_f.write(s)
                    final_f.write('\n')
