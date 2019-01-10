# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm

import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os
import re


class PingLiangSpider(scrapy.Spider):
    name = "pingliang"
    base_url = "http://wzly.pingliang.gov.cn/Index_index_p_{}_"
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

    def start_requests(self):
        for i in range(1, 5707):
            # for i in range(1, 5):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//div[@class='booklist']")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"网友"] = info.xpath("./div[1]//text()") if info.xpath(
                "./div[1]//text()") else []
            item[u"网友"] = deal_ntr("".join(item[u"网友"]))
            item[u"留言编号"] = "'{}'".format(info.xpath(".//span[@class='number']/a/text()")[0].strip() if info.xpath(
                ".//span[@class='number']/a/text()") else "")
            item[u"单位地区分类IP及日期"] = info.xpath("./div[2]/h3/span/text()[2]")[
                0].strip() if info.xpath("./div[2]/h3/span/text()[2]") else ""
            item[u"单位地区分类IP及日期"] = deal_ntr(item[u"单位地区分类IP及日期"])
            rq = re.search(u"\d{4}-\d{1,2}-\d{1,2}", item[u"单位地区分类IP及日期"])
            if rq:
                item[u"日期"] = rq.group()
            else:
                item[u"日期"] = u""
            item[u"办理状态"] = info.xpath("./div[2]/h3/div//span/text()")[0].strip() if info.xpath(
                "./div[2]/h3/div//span/text()") else ""
            item[u"标题"] = info.xpath("./div[2]/h2/a/text()")[0].strip() if info.xpath(
                "./div[2]/h2/a/text()") else ""
            item[u"留言内容"] = info.xpath("./div[2]/text()") if info.xpath(
                "./div[2]/text()") else []
            item[u"留言内容"] = deal_ntr("".join(item[u"留言内容"]))
            item[u"链接"] = "http://wzly.pingliang.gov.cn{}".format(
                info.xpath("./div[2]/h2/a/@href")[0].strip() if info.xpath("./div[2]/h2/a/@href") else "")
            self.dump_list.process_item(item)
            detail_item = item
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers, meta={"item": detail_item})

    def parse_detail(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        item = response.meta["item"]
        rq_ll = html.xpath("//span[@class='number']/text()")[0].strip()
        rq = re.search(u"\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}", rq_ll, re.DOTALL)
        if rq:
            item[u"日期"] = rq.group()
        else:
            item[u"日期"] = ""
        llcs = re.search(u"浏览次数：(\d+)", rq_ll, re.DOTALL)
        if llcs:
            item[u"浏览次数"] = llcs.group(1)
        else:
            item[u"浏览次数"] = ""
        item[u"回复内容"] = html.xpath("//div[@class='booklist official']/div[@class='content']/text()") if html.xpath(
            "//div[@class='booklist official']/div[@class='content']/text()") else []
        item[u"回复内容"] = deal_ntr("".join(item[u"回复内容"]))
        item[u"回复单位"] = \
            html.xpath("//div[@class='booklist official']/div[@class='content']/div[@class='orgInfo']/text()[1]")[
                0].strip() if html.xpath(
                "//div[@class='booklist official']/div[@class='content']/div[@class='orgInfo']/text()[1]") else ""
        item[u"回复时间"] = \
            html.xpath("//div[@class='booklist official']/div[@class='content']/div[@class='orgInfo']/text()[2]")[
                0].strip() if html.xpath(
                "//div[@class='booklist official']/div[@class='content']/div[@class='orgInfo']/text()[2]") else ""
        self.dump_detail.process_item(item)
