# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm
import json
import time
import scrapy
from scrapy import Request, FormRequest
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class LeShanSpider(scrapy.Spider):
    name = "leshan"
    base_url = "http://www.leshan.gov.cn/user/linked/list.do"
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
        "pageSize": "30",
        "pageNo": "",
    }

    def start_requests(self):
        for i in range(1, 672):
            # for i in range(1, 2):
            self.data_form["pageNo"] = str(i)
            yield FormRequest(self.base_url, formdata=self.data_form, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        result = json.loads(body)
        lines = result["data"]["dataList"]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"标题"] = info["title"]
            item[u"链接"] = "http://www.leshan.gov.cn/lsszww/ldxx/dzemail_content.shtml?id={}".format(info["id"])
            item[u"回复时间"] = info["completeDate"]
            item[u"回复状态"] = u"已回复"
            self.dump_list.process_item(item)
            item_detail = {}
            item_detail[u"区域"] = info["region"]
            item_detail[u"详细区域"] = info["address"]
            item_detail[u"信件类型"] = info["infoType"]
            item_detail[u"信件编号"] = "'{}'".format(info["code"])
            a = str(info["createTime"])[:10]
            item_detail[u"来信时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(a)))
            item_detail[u"信件标题"] = info["title"]
            item_detail[u"信件内容"] = info["content"]
            item_detail[u"信件内容"] = etree.HTML(item_detail[u"信件内容"]).xpath("//text()")
            item_detail[u"信件内容"] = deal_ntr("".join(item_detail[u"信件内容"]))
            item_detail[u"回复内容"] = etree.HTML(info["dealWithDescription"]).xpath("//text()")
            item_detail[u"回复内容"] = deal_ntr("".join(item_detail[u"回复内容"]))
            item_detail[u"发布部门"] = info["department"]
            item_detail[u"回复时间"] = info["completeDate"]
            item_detail[u"链接"] = item[u"链接"]
            self.dump_detail.process_item(item_detail)
    # def parse_detail(self, response):
    #     body = unicode_body(response)
    #     html = etree.HTML(body)
    #     item = {}
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     self.dump_detail.process_item(item)
