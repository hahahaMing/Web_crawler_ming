#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/23 10:50
# @Author  : Eiya_ming
# @Email   : eiyaming@163.com
# @File    : c02_ad_finding.py

import re

with open('results/崩坏世界的传奇大冒险.txt', 'r', encoding='utf-8')as f:
    s = f.read()

dic = ["笔、趣、阁www。biquge。info",
       "笔％趣％阁www.biｑｕge.info",
       "笔《趣》阁wｗw.ｂｉquｇｅ.ｉｎｆｏ",
       "503 Service Temporarily Unavailable"
       ]

for d in dic:
    s = s.replace(d,"")

t = re.findall(".*b.*", s)

for ss in t:
    print(ss)
