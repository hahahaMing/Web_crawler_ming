#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/22 10:41
# @Author  : Eiya_ming
# @Email   : eiyaming@163.com
# @File    : c01_bhsjdcqdmx.py

from crawlers.novels import biquge

cw = biquge("11_11245")
cw.main_crawler()