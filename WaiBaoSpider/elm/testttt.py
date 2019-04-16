# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/3/25
# @File: testttt.py
# @Software: PyCharm
import json

import redis
import requests
import traceback
import time
from csvWriter import CSVDumper
import re

f_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
dumper = CSVDumper("{}_elm_detail.csv".format(f_time))
ref_uel = "https://h5.ele.me/shop/"
caidan_url = "https://h5.ele.me/pizza/shopping/restaurants/{}/batch_shop"

rediser = redis.Redis(host='127.0.0.1', port='6379', db=0, )

headers_d = {
    "referer": "",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "cookie": "",
}

while True:
    # try:
    #     all_in = rediser.spop("BeijingUrl")
    # # all_in = "''8364529521265123''#$#$https://h5.ele.me/shop/#id=E4164727854040463229"
    # except:
    #     break
    # print("--%s--" % all_in)
    # all_in_l = all_in.split("#$#$")
    # auid = all_in_l[0].strip()[1:-1]
    # url = all_in_l[1].strip()
    item = {u"id": "aaa", u"菜品名称/菜品销量/好评率/菜品分类/菜品价格": u"-"}
    try:
        # id = re.search("shop/#id=(.*)", url)
        # if not id:
        #     id = re.search("shop/\?id=(.*)", url)
        # id = id.group(1)
        id = "E17166512646533728554"
        # print("%s -- %s" % (auid, id))
        api_u = caidan_url.format(id)
        print(api_u)
        res = requests.get(api_u, headers=headers_d).text
        # print(res)
        liness = json.loads(res)
        lines = liness.get("menu", [])
        if lines:
            pass
        else:
            lines = liness
        print("get len %s lines" % len(lines))
        str_ll = []
        for info in lines:
            for fo in info.get("foods", []):
                small_str = []
                small_str.append(fo.get("name", u"-"))
                small_str.append(str(fo.get("month_sales", u"-")))
                small_str.append(str(fo.get("satisfy_rate", u"-")))
                small_str.append(str(fo.get("type", u"-")))
                small_str.append(str(fo.get("specfoods", [{}])[0].get("price", u"-")))
                sm_str = u"/".join(small_str)
                str_ll.append(sm_str)
        str_all = u"|".join(str_ll)
        item[u"菜品名称/菜品销量/好评率/菜品分类/菜品价格"] = str_all
        dumper.process_item(item)
    except:
        print(str(traceback.format_exc()))
        dumper.process_item(item)
    time.sleep(2)
