'''
Author: your name
Date: 2020-12-03 14:08:06
LastEditTime: 2021-08-15 14:02:34
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Web_crawler_ming\c03_quick_test.py
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/3 14:08
# @Author  : Eiya_ming
# @Email   : eiyaming@163.com
# @File    : c03_quick_test.py

import requests
import re


test_url = "http://m.yn887.com/ynmh/1360/393231.html"

r = requests.get(test_url)
s = r.text.encode(r.encoding).decode('utf-8')
print(s)
t = re.findall("<img src=.*id=\"qTcms_pic\".*",s)

print(t)

