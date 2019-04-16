# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/3/23
# @File: test.py
# @Software: PyCharm

import requests
import json

session = requests.session()
data = {"status": 200,
        "http_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "request_method": "get", "timestamp": "2019-04-13T09:06:25.006Z",
        "http_url": "https://bbs.nga.cn/read.php?tid=16930782&_ff=-7&rand=569", "event": "load", "is_new": 0,
        "http_referer": "https://bbs.nga.cn/misc/adpage_insert_2.html?https://bbs.nga.cn/read.php?tid=16930782&_ff=-7&rand=569",
        "cookie": "e80bed26441dcfc6a54dff94a305a5ac", "page_id": "8522099cae2f9c0668058768986c1cdd",
        "short_cookie": "5bbf0f95e6eea8ae0e3f7118b9c9e91d", "appkey": "uvhyzh0cudcn0o39"}

url = "https://xy-log2.tagtic.cn/mininfo/v1/logs/uvhyzh0cudcn0o39"
res = session.post(url).text
print(res)
from csvWriter import CSVDumper

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "Cookie": "ngaPassportUid=guest05cb1a1d558964; taihe=e80bed26441dcfc6a54dff94a305a5ac; UM_distinctid=16a15e03c3423e-0e83670f3cb349-12376d51-13c680-16a15e03c35ad7; CNZZDATA1256638820=685109523-1555144510-https%253A%252F%252Fbbs.nga.cn%252F%7C1555144510; CNZZDATA30043604=cnzz_eid%3D1008146034-1555142801-https%253A%252F%252Fbbs.nga.cn%252F%26ntime%3D1555142801; CNZZDATA30039253=cnzz_eid%3D867693601-1555142918-https%253A%252F%252Fbbs.nga.cn%252F%26ntime%3D1555142918; Hm_lvt_5adc78329e14807f050ce131992ae69b=1555145178; guestJs=1555146013; lastpath=/read.php?tid=16930782&_ff=-7&rand=569; taihe_session=5bbf0f95e6eea8ae0e3f7118b9c9e91d; lastvisit=1555146169; bbsmisccookies=%7B%22insad_refreshid%22%3A%7B0%3A%22/WsVWjNWf5dgI1WS2rFTus2g9CqDDOmotPZmB72as%22%2C1%3A1555749976%7D%2C%22pv_count_for_insad%22%3A%7B0%3A-46%2C1%3A1555174832%7D%2C%22insad_views%22%3A%7B0%3A1%2C1%3A1555174832%7D%2C%22uisetting%22%3A%7B0%3A%22c%22%2C1%3A1555146470%7D%7D; Hm_lpvt_5adc78329e14807f050ce131992ae69b=1555146171"
}

res = session.get("https://bbs.nga.cn/read.php?tid=16930782&_ff=-7&rand=569", headers=headers).content.decode("gbk")
print(res)

# dumper = CSVDumper("test.csv")
#
# a = {"dasd": "3rfeds", "asdc": "32re", "asc": "dq2dq", "adsc": "21eds", "dassadad": "ascas"}
# dumper.process_item(a)

# for i in range(10):
#     try:
#         if i == 3:
#             continue
#         else:
#             print(i)
#     except:
#         pass
# import redis
#
# dumper = CSVDumper("shanghaicsv.csv")
# rediser = redis.Redis(host='127.0.0.1', port='6379', db=2, )
#
# while True:
#     item = {"a": "-"}
#     ss = rediser.spop("shanghaiaddr")
#     item["a"] = ss
#     dumper.process_item(item)


# from selenium import webdriver
#
# driver = webdriver.Chrome("./chromedriver")
#
# driver.get("https://blog.csdn.net/qq_39247153/article/details/81902559")
# focus = driver.find_element_by_xpath('//textarea[@name="comment_content"]')
# driver.execute_script("arguments[0].scrollIntoView();", focus)


# base_url = "https://www.ele.me/restapi/shopping/v2/menu?restaurant_id={}"
#
# ref_url = "https://www.ele.me/shop/{}"
#
# headers = {
#     # "referer":"",
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "accept-encoding": "gzip, deflate, br",
#     "accept-language": "zh-CN,zh;q=0.9",
#     "cache-control": "max-age=0",
#     "upgrade-insecure-requests": "1",
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
#     "cookie": "ubt_ssid=gj10m2ir1s2mspy7dg706vn0js6psq9o_2019-03-20; _utrace=d78c176a5d8890d24445cfa420b81fa5_2019-03-20; cna=6qeRFJNUxAMCAT2cydFg/fUc; eleme__ele_me=597ad32a9035a95ae5864d2162e13c9d%3A08c83c1c8529de4f8b019a90d0e74a2f44e740ba; track_id=1553086509|9166c6f7f0a679d36e2aad687322978e644b7aa604839d4666|f8e3fc3a47813d69da35afef54ab572b; USERID=2085922706; UTUSER=2085922706; SID=VyP55YxQjdiecmDu6gbYVfjjNlimz6DQc58w; isg=BKGhmss2WeUXJPUWSzXhQGY3sGt75hUozKog2AN3cKgHasw8V5zsEVeryd7J-a14; pizza73686f7070696e67=9n5StWrlVIv0LTcR6n8rV0HbmLsXstUddolO1nIh6pZwLZXRO1WkpVG3-F-64Sck",
# }
# url = "https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=wx4g14x9ff7m&latitude=39.91639&limit=24&longitude=116.421555&offset=408&terminal=web"
#
# res = requests.get(url, headers=headers).text
# print(res)


# id = "E9507640462406294772"
#
# headers["referer"] = ref_url.format(id)
# url = base_url.format(id)
# res = requests.get(url, headers=headers).text
# print(res)
#
#
# def deal_detail(content):
#     respp = json.loads(content)
#     d_item = []
#     mo = u"{}: {}"
#     for info in respp:
#         for f in info["foods"]:
#             foo_l = []
#             foo_l.append(mo.format("name", f["name"]))
#             foo_l.append(mo.format("rating", f["rating"]))
#             foo_l.append(mo.format("month_sales", f["month_sales"]))
#             foo_l.append(mo.format("rating_count", f["rating_count"]))
#             foo_l.append(mo.format("tips", f["tips"]))
#             foo_l.append(mo.format("item_id", f["item_id"]))
#             foo_l.append(mo.format("satisfy_count", f["satisfy_count"]))
#             foo_l.append(mo.format("satisfy_rate", f["satisfy_rate"]))
#             foo_l.append(mo.format("category_id", f["category_id"]))
#             foo_l.append(mo.format("catename", ""))
#             foo_l.append(mo.format("catetype", ""))
#             foods = u"__".join(foo_l)
#             d_item.append(foods)
#     foo_str = u"\n".join(d_item)
#     return foo_str
#
#
# a = deal_detail(res)
# import redis
# rediser = redis.Redis(host='127.0.0.1', port='6379', db=0, )
# a = u"http:"
# b = rediser.sadd("bejingurl", u"{}#$#$".format(a))
# print(b)

# a = rediser.sismember("beijingaddr", "sss")
# print(a)
