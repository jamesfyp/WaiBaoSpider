# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/2/24
# @File: test.py
# @Software: PyCharm

import time
from urllib import quote
import requests
#
# a = "2018-07-01 00:00:00"
# b = "2018-12-31 00:00:00"
#
#
# c = int(time.mktime(time.strptime(a, "%Y-%m-%d %H:%M:%S")))
# d = int(time.mktime(time.strptime(b, "%Y-%m-%d %H:%M:%S")))
# print(c)
# print(d)
headers = {"User-Agent":"Instagram 81.0.0.10.92 (iPhone11,2; iOS 12_1_4; zh_CN; zh-Hans-CN; scale=3.00; gamut=wide; 1125x2436; 142340302)",}

res = requests.get("https://scontent-icn1-1.cdninstagram.com", headers=headers).text

print(res)