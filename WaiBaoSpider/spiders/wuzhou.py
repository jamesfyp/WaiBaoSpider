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
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class WuZhouSpider(scrapy.Spider):
    name = "wuzhou"
    base_url = "http://www.wuzhou.gov.cn/web/wzegmh/letter/letter_list.ptl?pageNo={}"
    data_path = os.getcwd() + "/WaiBaoSpider/data/"
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

    def start_requests(self):
        for i in range(1, 310):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//div[@class='kuang']/table[@class='tab']/tr")[1:]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"信件标题"] = info.xpath("./td[1]/div/a/text()")[0].strip() if info.xpath("./td[1]/div/a/text()") else ""
            link = info.xpath("./td[1]/div/a/@onclick")[0].strip()
            item[u"链接"] = "http://www.wuzhou.gov.cn/web/wzegmh/letter/inquiry_detail.ptl?inquiryId={}".format(
                re.search("\d+", link).group())
            item[u"信件编号"] = "'{}'".format(
                info.xpath("./td[2]/text()")[0].strip() if info.xpath("./td[2]/text()") else "")
            item[u"处理单位"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"来信人"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"来信时间"] = info.xpath("./td[5]/text()")[0].strip() if info.xpath("./td[5]/text()") else ""
            item[u"类型"] = info.xpath("./td[6]/text()")[0].strip() if info.xpath("./td[6]/text()") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers, meta={"url": item[u"链接"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"标题"] = html.xpath("//table[@class='reply']/tr[2]/td[2]/text()")[0].strip() if html.xpath(
            "//table[@class='reply']/tr[2]/td[2]/text()") else ""
        item[u"来信时间"] = html.xpath("//table[@class='reply']/tr[3]/td[2]/text()")[0].strip() if html.xpath(
            "//table[@class='reply']/tr[3]/td[2]/text()") else ""
        item[u"内容"] = deal_ntr(
            html.xpath("//table[@class='reply']/tr[4]/td[2]/text()")[0].strip() if html.xpath(
                "//table[@class='reply']/tr[4]/td[2]/text()") else "")
        item[u"处理部门"] = html.xpath("//table[@class='reply']/tbody[1]/tr[1]/td[2]/text()")[0].strip() if html.xpath(
            "//table[@class='reply']/tbody[1]/tr[1]/td[2]/text()") else ""
        item[u"处理时间"] = html.xpath("//table[@class='reply']/tbody[1]/tr[1]/td[4]/text()")[0].strip() if html.xpath(
            "//table[@class='reply']/tbody[1]/tr[1]/td[4]/text()") else ""
        item[u"回复"] = deal_ntr(
            html.xpath("//table[@class='reply']/tbody[1]/tr[2]/td[2]/text()")[0].strip() if html.xpath(
                "//table[@class='reply']/tbody[1]/tr[2]/td[2]/text()") else "")
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
