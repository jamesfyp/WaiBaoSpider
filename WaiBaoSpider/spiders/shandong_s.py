# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm
import re

import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body
import os


class ShanDongSSpider(scrapy.Spider):
    name = "shandong_s"
    base_url = "http://zwfw.sd.gov.cn/sdzw/see/notice/noticemore.do?regionId=370000&num={}"
    data_path = os.getcwd() + "/WaiBaoSpider/data/%s/" % name
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    # dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    custom_settings = {
        'DOWNLOAD_DELAY': 0.2,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }

    def start_requests(self):
        # for i in range(1, 24700):
        for i in range(1, 2):
            print(i)
            # for i in range(1, 2):
            # self.data_form["pageID"] = str(i)
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//table")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"申请人"] = info.xpath("./tr/td[1]/a/text()")[0].strip() if info.xpath(
                "./tr/td[1]/a/text()") else ""
            item[u"办件名称"] = info.xpath("./tr/td[2]/a/text()")[0].strip() if info.xpath(
                "./tr/td[2]/a/text()") else ""
            item[u"统一申办号"] = "'{}'".format(
                info.xpath("./tr/td[3]/a/text()")[0].strip() if info.xpath("./tr/td[3]/a/text()") else "")
            item[u"办结时间"] = info.xpath("./tr/td[4]/text()")[0].strip() if info.xpath(
                "./tr/td[4]/text()") else ""
            item[u"结果"] = info.xpath("./tr/td[5]/text()")[0].strip() if info.xpath(
                "./tr/td[5]/text()") else ""
            link = info.xpath("./tr/td[2]/a/@href")[0].strip() if info.xpath(
                "./tr/td[2]/a/@href") else ""
            if re.search(u"^\.", link):
                item[u"链接"] = "http://zwfw.sd.gov.cn/sdzw/see/notice{}".format(link[1:])
            else:
                item[u"链接"] = link
            self.dump_list.process_item(item)
