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


class LiuPanShuiSpider(scrapy.Spider):
    name = "liupanshui"
    base_url = "http://tszx.gzlps.gov.cn/jlpt/front/letterlist.do?type=4&currentPage={}&groupId=0"
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
        for i in range(1, 357):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("(//tr)/td[@class='liststyle1']")
        print(len(lines))
        for i in range(0, len(lines), 7):
            item = {}
            item[u"信件编号"] = "'{}'".format(lines[i].xpath("./text()")[0].strip() if lines[1].xpath("./text()") else "")
            item[u"标题"] = lines[i + 1].xpath("./div/a/text()")[0].strip() if lines[i + 1].xpath(
                "./div/a/text()") else ""
            item[u"类型"] = lines[i + 2].xpath("./text()")[0].strip() if lines[i + 2].xpath("./text()") else ""
            item[u"状态"] = lines[i + 3].xpath("./text()")[0].strip() if lines[i + 3].xpath("./text()") else ""
            item[u"人气"] = lines[i + 4].xpath("./text()")[0].strip() if lines[i + 4].xpath("./text()") else ""
            item[u"来信时间"] = lines[i + 5].xpath("./text()")[0].strip() if lines[i + 5].xpath("./text()") else ""
            item[u"受理单位"] = lines[i + 6].xpath("./text()")[0].strip() if lines[i + 6].xpath("./text()") else ""
            link = lines[i + 1].xpath("./div/a/@onclick")[0].strip() if lines[i + 1].xpath(
                "./div/a/@onclick") else ""
            item[u"链接"] = "http://tszx.gzlps.gov.cn/jlpt/front/detailview.do?iid={}".format(
                re.search("\d+", link).group())
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "bh": item[u"信件编号"], "bt": item[u"标题"], "gzd": item[u"人气"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"办件标题"] = data["bt"]
        item[u"信件内容"] = html.xpath("//div[@class='zw']/table[4]/tbody/tr/td[3]//text()") if html.xpath(
            "//div[@class='zw']/table[4]/tbody/tr/td[3]//text()") else []
        item[u"信件内容"] = deal_ntr("".join(item[u"信件内容"]))
        item[u"办件来源"] = html.xpath("//div[@class='zw']/table[6]/tbody/tr/td[3]/text()")[0].strip() if html.xpath(
            "//div[@class='zw']/table[6]/tbody/tr/td[3]/text()") else ""
        item[u"办件编号"] = data["bh"]
        item[u"关注度"] = data["gzd"]
        item[u"提交时间"] = html.xpath("//div[@class='zw']/table[10]/tbody/tr/td[3]/text()")[0].strip() if html.xpath(
            "//div[@class='zw']/table[10]/tbody/tr/td[3]/text()") else ""
        item[u"处理时间"] = html.xpath("//div[@class='zw']/table[10]/tbody/tr/td[6]/text()")[0].strip() if html.xpath(
            "//div[@class='zw']/table[10]/tbody/tr/td[6]/text()") else ""
        item[u"处理状态"] = html.xpath("//div[@class='zw']/table[12]/tbody/tr/td[3]/text()")[0].strip() if html.xpath(
            "//div[@class='zw']/table[12]/tbody/tr/td[3]/text()") else ""
        item[u"答复部门"] = html.xpath("//div[@class='zw']/table[12]/tbody/tr/td[6]/text()")[0].strip() if html.xpath(
            "//div[@class='zw']/table[12]/tbody/tr/td[6]/text()") else ""
        item[u"回复意见"] = html.xpath("//div[@class='zw']/table[14]/tbody/tr/td[3]//text()") if html.xpath(
            "//div[@class='zw']/table[14]/tbody/tr/td[3]//text()") else []
        item[u"回复意见"] = deal_ntr("".join(item[u"回复意见"]))
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
