# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/3/22
# @File: support.py
# @Software: PyCharm

import time
import redis
import json

from mitmproxy import ctx
from csvWriter import CSVDumper
import traceback

rediser = redis.Redis(host='127.0.0.1', port='6379', db=0, )

f_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
dumper = CSVDumper("{}_elm_data.csv".format(f_time))


def deal_text(content):
    """
    :param content:
    :return:
    """
    respp = json.loads(content)
    ctx.log("this page has %s lines" % len(respp))
    for info in respp:
        item = {u"城市": u"北京", u"行政区": u"-", u"商圈": u"-", u"店铺简介": u"-", u"配送费": u"-", u"配送时间": u"-", u"手机号": u"-",
                u"电话": u"-", u"配送费简介": u"-", u"评分": u"-", u"评论数量": u"-", u"经度": u"-", u"纬度": u"-", u"营业时间": u"-",
                u"采集时间": u"-", u"店铺分类": u"-", u"菜品名称/菜品销量/好评率/菜品分类/菜品价格": u"-", u"店铺销量": u"-", u"起送金额": u"-",
                u"店铺地址": u"-", u"店铺名": u"-", u"scheme": u"", u"url": u"",
                u"authid": u"", u"id": u""}
        try:
            autid = "'{}'".format(info["authentic_id"])
            item[u"authid"] = autid
            ctx.log(autid)
            if rediser.sismember("restid", item[u"authid"]):
                ctx.log("reppp!!! and jump this!!!")
                continue
            else:
                rediser.sadd("restid", item[u"authid"])
            item[u"评分"] = info["rating"]
            item[u"配送费"] = info["delivery_fee_discount"]
            item[u"店铺简介"] = info["description"].replace(u"\n", u"").replace(u"\t", u"").replace(u" ", u"")
            item[u"配送费简介"] = info["piecewise_agent_fee"].get("description", u"-")
            item[u"配送时间"] = info["order_lead_time"]
            item[u"手机号"] = "'{}'".format(info["phone"])
            item[u"电话"] = u"-"
            item[u"评论数量"] = info["rating_count"]
            yysj = info["opening_hours"]
            yyll = []
            for i in yysj:
                yyll.append(i)
            item[u"营业时间"] = u" ".join(yyll)
            item[u"采集时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item[u"店铺销量"] = info["recent_order_num"]
            item[u"起送金额"] = info["float_minimum_order_amount"]
            item[u"纬度"] = "'{}'".format(info["latitude"])
            item[u"经度"] = "'{}'".format(info["longitude"])
            item[u"店铺名"] = info["name"]
            item[u"店铺分类"] = info["type"]
            item[u"店铺地址"] = info["address"]
            item[u"scheme"] = info["scheme"]
            tag_detail = u"{}#$#${}".format(u"'{}'".format(item[u"authid"]), item[u"scheme"])
            a = rediser.sadd("BeijingUrl", tag_detail)
            ctx.log("### %s ###" % a)
            item[u"url"] = "https://www.ele.me/shop/{}".format(info["id"])
            item[u"id"] = info["id"]
            item[u"菜品名称/菜品销量/好评率/菜品分类/菜品价格"] = u" "
            dumper.process_item(item)
        except:
            ctx.log(str(traceback.format_exc()))
            dumper.process_item(item)


# def deal_detail(content):
#     respp = json.loads(content)
#     d_item = []
#     mo = u"{}:{}"
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
#             foo_l.append(mo.format("catename", " "))
#             foo_l.append(mo.format("catetype", " "))
#             foods = u" ".join(foo_l)
#             d_item.append(foods)
#     foo_str = u"-$-".join(d_item)
#     return foo_str
