# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/3/23
# @File: main2.py
# @Software: PyCharm

import time
import redis
import requests
from csvWriter import CSVDumper
from support import deal_text, deal_detail

f_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
dumper = CSVDumper("{}_elm_data.csv".format(f_time))

rediser = redis.Redis(host='127.0.0.1', port='6379', db=2, )

headers = {
    "referer":"https://www.ele.me/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "cookie": "ubt_ssid=gj10m2ir1s2mspy7dg706vn0js6psq9o_2019-03-20; _utrace=d78c176a5d8890d24445cfa420b81fa5_2019-03-20; cna=6qeRFJNUxAMCAT2cydFg/fUc; eleme__ele_me=597ad32a9035a95ae5864d2162e13c9d%3A08c83c1c8529de4f8b019a90d0e74a2f44e740ba; track_id=1553086509|9166c6f7f0a679d36e2aad687322978e644b7aa604839d4666|f8e3fc3a47813d69da35afef54ab572b; USERID=2085922706; UTUSER=2085922706; SID=VyP55YxQjdiecmDu6gbYVfjjNlimz6DQc58w; isg=BKGhmss2WeUXJPUWSzXhQGY3sGt75hUozKog2AN3cKgHasw8V5zsEVeryd7J-a14; pizza73686f7070696e67=9n5StWrlVIv0LTcR6n8rV0HbmLsXstUddolO1nIh6pZwLZXRO1WkpVG3-F-64Sck",
}

headers_d = {
    "referer": "",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "cookie": "ubt_ssid=gj10m2ir1s2mspy7dg706vn0js6psq9o_2019-03-20; _utrace=d78c176a5d8890d24445cfa420b81fa5_2019-03-20; cna=6qeRFJNUxAMCAT2cydFg/fUc; eleme__ele_me=597ad32a9035a95ae5864d2162e13c9d%3A08c83c1c8529de4f8b019a90d0e74a2f44e740ba; track_id=1553086509|9166c6f7f0a679d36e2aad687322978e644b7aa604839d4666|f8e3fc3a47813d69da35afef54ab572b; USERID=2085922706; UTUSER=2085922706; SID=VyP55YxQjdiecmDu6gbYVfjjNlimz6DQc58w; isg=BKGhmss2WeUXJPUWSzXhQGY3sGt75hUozKog2AN3cKgHasw8V5zsEVeryd7J-a14; pizza73686f7070696e67=9n5StWrlVIv0LTcR6n8rV0HbmLsXstUddolO1nIh6pZwLZXRO1WkpVG3-F-64Sck",
}

ref_uel = "https://www.ele.me/shop/{}"
caidan_url = "https://www.ele.me/restapi/shopping/v2/menu?restaurant_id={}"

list_url = "https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash={geo}&latitude={la}&limit=24&longitude={lo}&offset={of}&terminal=web"


for mnm in range(50):
    ss = rediser.spop("beijingaddr")
    rediser.sadd("beijingaddr_back", ss)
    if ss:
        print(" start one localtion %s" % mnm)
        ss_list = ss.split("#$#$")
        count = int(ss_list[0])
        print("count: %s " % count)
        geo = ss_list[1]
        lo = ss_list[2]
        la = ss_list[3]
        of = 0
        while of < count + 1:
            print(of)
            alist_url = list_url.format(geo=geo, la=la, lo=lo, of=of)
            print(alist_url)
            res_list = requests.get(alist_url, headers=headers).text
            item_list = deal_text(res_list)
            if len(item_list) > 0:
                for info in item_list:
                    id = info["id"]
                    headers_d["referer"] = ref_uel.format(id)
                    detail_url = caidan_url.format(id)
                    res_detail = requests.get(detail_url, headers=headers_d).text
                    info["foods"] = deal_detail(res_detail)
                    # print(info)
                    dumper.process_item(info)
                of += 24
                time.sleep(2)
            else:
                pass
    else:
        break

