#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/3 14:08
# @Author  : Eiya_ming
# @Email   : eiyaming@163.com
# @File    : c03_quick_test.py

import requests
import os
import re

test_url = "http://www.biquge.info/40_40050"

r = requests.get(test_url, verify=False)
s = r.text.encode(r.encoding).decode('utf-8')
print(s)
print('ss')