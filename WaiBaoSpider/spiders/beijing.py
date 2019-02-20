# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm
import json

import scrapy
from scrapy import Request, FormRequest
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class BeiJingSpider(scrapy.Spider):
    name = "beijing"
    base_url = "http://rexian.beijing.gov.cn/default/com.web.complain.complain.moreNewComplain.biz.ext"
    data_path = os.getcwd() + "/WaiBaoSpider/data/"
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    data_form = {
        "PageCond/begin": "",
        "PageCond/isCount": "true",
        "PageCond/length": "6",
    }

    type_data = {
        "1": u"咨询",
        "2": u"建议",
        "3": u"投诉",
    }

    def start_requests(self):
        # for i in range(1, 267):
        i = 0
        while i < 10283:
            # while i < 10:
            self.data_form["PageCond/begin"] = str(i)
            print(i)
            yield FormRequest(self.base_url, formdata=self.data_form, callback=self.parse_list, headers=self.headers)
            i += 10

    def parse_list(self, response):
        body = unicode_body(response)
        res = json.loads(body)
        lines = res["newComplainnList"]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"类型"] = self.type_data.get(info["letterType"], u"")
            item[u"标题"] = info.get("letterTitle", "")
            item[u"评价人数"] = info.get("reCode", "")
            item[u"发起时间"] = info.get("fomateWriteDate", "")
            id = info["originalId"]
            item[
                u"链接"] = "http://rexian.beijing.gov.cn/default/com.web.complain.complainDetail.flow?originalId={}".format(
                id)
            text = info.get("letterContent", "")
            author = info.get("writeUser", "")
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "text": text, "author": author, "title": item[u"标题"],
                                "pingnum": item[u"评价人数"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"标题"] = data["title"]
        item[u"来信人"] = data["author"]
        item[u"来信时间"] = html.xpath("//p[@class='font12 gray time_mail']/span[2]/text()")[0].strip() if html.xpath(
            "//p[@class='font12 gray time_mail']/span[2]/text()") else ""
        item[u"网友评价"] = data["pingnum"]
        item[u"处理部门"] = html.xpath("(//div[@class='mail_track'])[2]/span[1]/text()")[0].strip() if html.xpath(
            "(//div[@class='mail_track'])[2]/span[1]/text()") else ""
        item[u"回复时间"] = html.xpath("(//div[@class='mail_track'])[2]/span[2]/text()")[0].strip() if html.xpath(
            "(//div[@class='mail_track'])[2]/span[2]/text()") else ""
        item[u"回复内容"] = html.xpath("(//div[@class='mail_track'])[2]/p//text()") if html.xpath(
            "(//div[@class='mail_track'])[2]/p//text()") else []
        item[u"回复内容"] = deal_ntr("".join(item[u"回复内容"]))
        item[u"赞"] = html.xpath("(//a[@id]/span[@id])[1]/text()")[0].strip() if html.xpath(
            "(//a[@id]/span[@id])[1]/text()") else ""
        item[u"踩"] = html.xpath("(//a[@id]/span[@id])[2]/text()")[0].strip() if html.xpath(
            "(//a[@id]/span[@id])[2]/text()") else ""
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
