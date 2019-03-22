# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/2/24
# @File: test.py
# @Software: PyCharm
import re
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

# headers = {
#     "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
#     "Cookie": "__jsl_clearance=1551317446.257|0|Z5im7o00MItY4ISK5dq3D;Expires=Thu, 28-Feb-19 02:30:46 GMT;Path=/;"
# }
# url = "http://www.dpac.gov.cn/qczh/qczhgg1/"
# res = requests.get(url).content
# print(res)
# print(res.status_code)
# import dateformatting
#
# a = "02-28"
#
# b = dateformatting.parse(a).strftime("%Y%m%d")
# print(b)
resp = requests.post("http://apidata.chinaz.com/batchapi/GetApiData", data={"taskid": "5d9ebbe6e778469e9ba1feea"}).text
print(resp)
