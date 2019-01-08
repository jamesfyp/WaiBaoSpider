# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm

import scrapy
import json
from scrapy import Request, FormRequest
import demjson
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class BeiHaiSpider(scrapy.Spider):
    name = "beihai"
    base_url = "http://zwhd.beihai.gov.cn:8080/wcm/RefersServlet"
    base_url_detail = "http://zwhd.beihai.gov.cn:8080/wcm/GetGrSelect.do"
    data_path = os.getcwd() + "/WaiBaoSpider/data/%s/" % name
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    custom_settings = {
        # 'DOWNLOAD_DELAY': 1,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    data_form = {
        "areaCode": "1",
        "sType": "refertheme",
        "currPage": "",
        "pageSize": "20",
    }
    data_form_detail = {
        "method": "details",
        "id": "",
        "withJavaEncrypt": "1",
    }

    def start_requests(self):
        for i in range(1, 1176):
            # for i in range(1, 2):
            self.data_form["currPage"] = str(i)
            yield FormRequest(self.base_url, callback=self.parse_list, formdata=self.data_form, headers=self.headers)

    def parse_list(self, response):
        res = json.loads(response.body)
        lines = res["mails"]
        print(len(lines))
        for info in lines:
            item = {}
            id = info["id"]
            item[u"主题"] = info["theme"]
            item[u"链接"] = "http://zwhd.beihai.gov.cn:8080/wcm/govrefer2/wyxx/refer_detail.html?sn={}".format(id)
            item[u"类型"] = info["category"]
            item[u"处理时间"] = info["dealTime"]
            item[u"处理单位"] = info["deptName"]
            item[u"处理状态"] = info["status"]
            item[u"人气"] = info["clickTime"]
            self.dump_list.process_item(item)
            self.data_form_detail["id"] = id
            yield FormRequest(self.base_url_detail, formdata=self.data_form_detail, callback=self.parse_detail,
                              headers=self.headers,
                              meta={"url": item[u"链接"]})

    def parse_detail(self, response):
        res = demjson.decode(response.body)
        data = response.meta
        item = {}
        item[u"标题"] = res["zhuti"]
        item[u"办件类型"] = res["leixing"]
        item[u"提交者"] = res["who"]
        item[u"转办时间"] = res["time"]
        item[u"内容"] = deal_ntr(res["neirong"])
        item[u"当前状态"] = res["zhuangtai"]
        item[u"回复内容"] = deal_ntr("".join(etree.HTML(res["jieguo"]).xpath("//text()")))
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
