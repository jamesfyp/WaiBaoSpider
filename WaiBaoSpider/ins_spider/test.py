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

headers = {
    "cookie": 'mid=XGqhzQAEAAEBgt1eCyWsMrMB-I8a; shbid=7432; shbts=1550935947.7486203; rur=ASH; csrftoken=bRenW0F7mNbxrfJo40IT3RmtYdkpgevS; ds_user_id=6693855049; sessionid=6693855049%3AN7dSuz2QPknOr7%3A7; urlgen="{\"118.130.42.209\": 3786}:1gxlt0:MQE6LQVqA_Yx1TDr9O9Wfrzh9Mw"',
}
url = "https://www.instagram.com/graphql/query/?query_hash=f92f56d47dc7a55b606908374b43a314&variables=%7B%22tag_name%22%3A%22%E9%9D%A2%E8%86%9C%22%2C%22show_ranked%22%3Afalse%2C%22first%22%3A12%2C%22after%22%3A%22QVFDa2MzWjVkM0o3QjEtcllJOTFzTEFkUE5NVDdYZnJZWG94a24tdVB0akM0ZWRUU2M4LU03UW9TNEVULTlWQ09xLUY3SXZ1RlI0dTFCME5KNXlRaGdnRA%3D%3D%22%7D"
res = requests.get(url, headers=headers).text
print(res)