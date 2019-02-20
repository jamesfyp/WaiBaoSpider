# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: huaibei.py
# @Software: PyCharm
import re

import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class HuaiBeiSpider(scrapy.Spider):
    name = "huaibei"
    base_url = "http://www.huaibei.gov.cn/content/column/4697478?pageIndex={}"
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
        for i in range(1, 267):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//div[@id='mm2']/div[2]/ul")[1:]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"主题"] = info.xpath("./li[@class='t1']/a/font/text()")[0].strip() if info.xpath(
                "./li[@class='t1']/a/font/text()") else ""
            item[u"回复单位"] = info.xpath("./li[@class='t3']/text()")[0].strip() if info.xpath(
                "./li[@class='t3']/text()") else ""
            item[u"受理状态"] = info.xpath("./li[@class='t4']/span/text()")[0].strip() if info.xpath(
                "./li[@class='t4']/span/text()") else ""
            item[u"回复时间"] = info.xpath("./li[@class='t2']/text()")[0].strip() if info.xpath(
                "./li[@class='t2']/text()") else ""
            item[u"链接"] = info.xpath("./li[@class='t1']/a/@href")[0].strip() if info.xpath(
                "./li[@class='t1']/a/@href") else ""
            item[u"浏览次数"] = info.xpath("./li[@class='t5']/text()")[0].strip() if info.xpath(
                "./li[@class='t5']/text()") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "title": item[u"主题"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"信件编号"] = "'{}'".format(
            html.xpath("//table[@class='liuyancon']/tr[1]/td[@class='nr'][1]/text()")[0].strip() if html.xpath(
                "//table[@class='liuyancon']/tr[1]/td[@class='nr'][1]/text()") else "")
        item[u"来信时间"] = html.xpath("//table[@class='liuyancon']/tr[1]/td[@class='nr'][2]/text()")[
            0].strip() if html.xpath("//table[@class='liuyancon']/tr[1]/td[@class='nr'][2]/text()") else ""
        item[u"信件类型"] = html.xpath("//table[@class='liuyancon']/tr[2]/td[@class='nr'][1]/text()")[
            0].strip() if html.xpath("//table[@class='liuyancon']/tr[2]/td[@class='nr'][1]/text()") else ""
        item[u"姓名"] = html.xpath("//table[@class='liuyancon']/tr[2]/td[@class='nr'][2]/text()")[
            0].strip() if html.xpath("//table[@class='liuyancon']/tr[2]/td[@class='nr'][2]/text()") else ""
        content = html.xpath("//table[@class='liuyancon']/tr[3]/td[@class='nrtxt']//text()") if html.xpath(
            "//table[@class='liuyancon']/tr[3]/td[@class='nrtxt']//text()") else []
        item[u"内容"] = deal_ntr("".join(content))
        dfdw_dfsj = \
            html.xpath("//table[@class='liuyancon']/tr[4]/td[@class='nrtxt']//div[@class='clearfix']/text()")[
                0].strip() if html.xpath(
                "//table[@class='liuyancon']/tr[4]/td[@class='nrtxt']//div[@class='clearfix']/text()") else ""
        dfdw = re.search(u"答复单位：(.*)", dfdw_dfsj)
        if dfdw:
            item[u"答复单位"] = deal_ntr(dfdw.group(1))
        else:
            item[u"答复单位"] = u""
        dfsj = re.search(u"答复时间：(.*)", dfdw_dfsj)
        if dfsj:
            item[u"答复时间"] = deal_ntr(dfsj.group(1))
        else:
            item[u"答复时间"] = u""
        dfqk = html.xpath("//table[@class='liuyancon']/tr[4]/td[@class='nrtxt']//text()") if html.xpath(
            "//table[@class='liuyancon']/tr[4]/td[@class='nrtxt']//text()") else []
        item[u"答复情况"] = deal_ntr("".join(dfqk))
        manyi = html.xpath("//tr[@id='myComment']/td//text()") if html.xpath("//tr[@id='myComment']/td//text()") else []
        item[u"用户满意度评价"] = deal_ntr("".join(manyi))
        item[u"链接"] = data["url"]
        item[u"标题"] = data["title"]
        self.dump_detail.process_item(item)
