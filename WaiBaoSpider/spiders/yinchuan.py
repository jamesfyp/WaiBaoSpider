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


class YinChuanSpider(scrapy.Spider):
    name = "yinchuan"
    base_url = "http://www.yc12345.gov.cn/?m=web&c=index&a=chaxun&page={}"
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
        for i in range(1, 223):
            # for i in range(1, 5):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//table[@class='list']/tr")[1:]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"工单编号"] = info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else ""
            item[u"标题"] = info.xpath("./td[2]/a/text()")[0].strip() if info.xpath("./td[2]/a/text()") else ""
            item[u"提交时间"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"办结时间"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"链接"] = "http://www.yc12345.gov.cn/{}".format(
                info.xpath("./td[2]/a/@href")[0].strip() if info.xpath("./td[2]/a/@href") else "")
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers, meta={"url": item[u"链接"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        data = response.meta
        item = {}
        item[u"工单编号"] = html.xpath("//table[@class='mytable']/tr[1]/td/text()")[0].strip() if html.xpath(
            "//table[@class='mytable']/tr[1]/td/text()") else ""
        item[u"标题"] = html.xpath("//table[@class='mytable']/tr[2]/td/text()")[0].strip() if html.xpath(
            "//table[@class='mytable']/tr[2]/td/text()") else ""
        item[u"提交时间"] = html.xpath("//table[@class='mytable']/tr[3]/td/text()")[0].strip() if html.xpath(
            "//table[@class='mytable']/tr[3]/td/text()") else ""
        item[u"内容"] = deal_ntr(html.xpath("//table[@class='mytable']/tr[4]/td/text()")[0].strip() if html.xpath(
            "//table[@class='mytable']/tr[4]/td/text()") else "")
        item[u"内容分类"] = html.xpath("//table[@class='mytable']/tr[5]/td/text()")[0].strip() if html.xpath(
            "//table[@class='mytable']/tr[5]/td/text()") else ""
        item[u"工单分类"] = html.xpath("//table[@class='mytable']/tr[6]/td/text()")[0].strip() if html.xpath(
            "//table[@class='mytable']/tr[6]/td/text()") else ""
        item[u"工单所属地"] = html.xpath("//table[@class='mytable']/tr[7]/td/text()")[0].strip() if html.xpath(
            "//table[@class='mytable']/tr[7]/td/text()") else ""
        item[u"主办单位"] = html.xpath("//table[@class='mytable']/tr[8]/td/text()")[0].strip() if html.xpath(
            "//table[@class='mytable']/tr[8]/td/text()") else ""
        item[u"办结时间"] = html.xpath("//table[@class='mytable']/tr[9]/td/text()")[0].strip() if html.xpath(
            "//table[@class='mytable']/tr[9]/td/text()") else ""
        item[u"办结回复"] = deal_ntr(html.xpath("//table[@class='mytable']/tr[10]/td/text()")[0].strip() if html.xpath(
            "//table[@class='mytable']/tr[10]/td/text()") else "")
        item[u"链接"] = data['url']
        self.dump_detail.process_item(item)
