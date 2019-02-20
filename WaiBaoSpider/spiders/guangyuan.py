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


class GuangYuanSpider(scrapy.Spider):
    name = "guangyuan"
    base_url = "http://www.gysjxx.com/szxx/index.asp?t=&page={}&section=2"
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
        for i in range(1, 841):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//td[@valign='top']//td[@valign='top']/table[2]/tbody/tr[@bgcolor]")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"编号"] = "'{}'".format(
                info.xpath("./td[2]/font/text()")[0].strip() if info.xpath("./td[2]/font/text()") else "")
            item[u"标题"] = info.xpath("./td[3]/a/font/text()")[0].strip() if info.xpath("./td[3]/a/font/text()") else ""
            item[u"链接"] = "http://www.gysjxx.com/szxx/{}".format(
                info.xpath("./td[3]/a/@href")[0].strip() if info.xpath("./td[3]/a/@href") else "")
            item[u"写信时间"] = info.xpath("./td[4]/font/text()")[0].strip() if info.xpath("./td[4]/font/text()") else ""
            item[u"对外公开时间"] = info.xpath("./td[5]/font/text()")[0].strip() if info.xpath("./td[5]/font/text()") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "bh": item[u"编号"], "bt": item[u"标题"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"信件编号"] = data["bh"]
        item[u"信件状态"] = html.xpath("//span[@id='Label2']/table/tbody/tr[1]/td[4]/a/text()")[0].strip() if html.xpath(
            "//span[@id='Label2']/table/tbody/tr[1]/td[4]/a/text()") else ""
        item[u"写信人"] = html.xpath("//span[@id='Label2']/table/tbody/tr[2]/td[2]/a/text()")[0].strip() if html.xpath(
            "//span[@id='Label2']/table/tbody/tr[2]/td[2]/a/text()") else ""
        item[u"写信时间"] = html.xpath("//span[@id='Label2']/table/tbody/tr[2]/td[4]/a/text()")[0].strip() if html.xpath(
            "//span[@id='Label2']/table/tbody/tr[2]/td[4]/a/text()") else ""
        item[u"联系地址"] = html.xpath("//span[@id='Label2']/table/tbody/tr[3]/td[2]/a/text()")[0].strip() if html.xpath(
            "//span[@id='Label2']/table/tbody/tr[3]/td[2]/a/text()") else ""
        item[u"联系电话"] = html.xpath("//span[@id='Label2']/table/tbody/tr[3]/td[4]/a/text()")[0].strip() if html.xpath(
            "//span[@id='Label2']/table/tbody/tr[3]/td[4]/a/text()") else ""
        item[u"收件人"] = html.xpath("//span[@id='Label2']/table/tbody/tr[4]/td[2]/a/text()")[0].strip() if html.xpath(
            "//span[@id='Label2']/table/tbody/tr[4]/td[2]/a/text()") else ""
        item[u"信件主题"] = data["bt"]
        item[u"信件内容"] = html.xpath("//span[@id='Label2']/table/tbody/tr[6]/td[2]//text()") if html.xpath(
            "//span[@id='Label2']/table/tbody/tr[6]/td[2]//text()") else []
        item[u"信件内容"] = deal_ntr("".join(item[u"信件内容"]))
        item[u"回复1"] = html.xpath(
            "//span[@id='Label2']/table/tbody/tr[7]/td[2]/table[1]/tbody/tr[1]//text()") if html.xpath(
            "//span[@id='Label2']/table/tbody/tr[7]/td[2]/table[1]/tbody/tr[1]//text()") else []
        item[u"回复1"] = deal_ntr("".join(item[u"回复1"]))
        item[u"回复1单位及时间"] = html.xpath(
            "//span[@id='Label2']/table/tbody/tr[7]/td[2]/table[1]/tbody/tr[2]//text()") if html.xpath(
            "//span[@id='Label2']/table/tbody/tr[7]/td[2]/table[1]/tbody/tr[2]//text()") else []
        item[u"回复1单位及时间"] = deal_ntr("".join(item[u"回复1单位及时间"]))
        item[u"回复2"] = html.xpath(
            "//span[@id='Label2']/table/tbody/tr[7]/td[2]/table[2]/tbody/tr[1]//text()") if html.xpath(
            "//span[@id='Label2']/table/tbody/tr[7]/td[2]/table[2]/tbody/tr[1]//text()") else []
        item[u"回复2"] = deal_ntr("".join(item[u"回复2"]))
        item[u"回复2单位及时间"] = html.xpath(
            "//span[@id='Label2']/table/tbody/tr[7]/td[2]/table[2]/tbody/tr[2]//text()") if html.xpath(
            "//span[@id='Label2']/table/tbody/tr[7]/td[2]/table[2]/tbody/tr[2]//text()") else []
        item[u"回复2单位及时间"] = deal_ntr("".join(item[u"回复2单位及时间"]))
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
