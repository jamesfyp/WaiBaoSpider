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
from urlparse import urljoin
import os


class SuZhouSpider(scrapy.Spider):
    name = "suzhou"
    base_url = "http://12345.ahsz.gov.cn/web/blsxxd/ncny/index_{}.html"
    data_path = os.getcwd() + "/WaiBaoSpider/data/"
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    custom_settings = {
        'DOWNLOAD_DELAY': 0.2,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }

    def start_requests(self):
        # for i in range(1, 399):
        yield Request("http://12345.ahsz.gov.cn/web/blsxxd/ncny/index.html", callback=self.parse_list,
                      headers=self.headers)
        for i in range(2, 399):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//table[@class='tstable margin_db']/tbody/tr[@id]")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"受理编号"] = "'{}'".format(
                info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else "")
            item[u"受理件标题"] = info.xpath("./td[2]/a/text()")[0].strip() if info.xpath("./td[2]/a/text()") else ""
            item[u"受理来源"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"办理单位"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"回复时间"] = info.xpath("./td[5]/text()")[0].strip() if info.xpath("./td[5]/text()") else ""
            item[u"链接"] = urljoin("http://12345.ahsz.gov.cn",
                                  info.xpath("./td[2]/a/@href")[0].strip().replace(u"../", u""))
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers, meta={"url": item[u"链接"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"主题"] = html.xpath("(//table[@class='xjxq_tab'])[1]/tr[1]/td/text()")[0].strip() if html.xpath(
            "(//table[@class='xjxq_tab'])[1]/tr[1]/td/text()") else ""
        item[u"受理件类型"] = html.xpath("(//table[@class='xjxq_tab'])[1]/tr[2]/td/text()")[0].strip() if html.xpath(
            "(//table[@class='xjxq_tab'])[1]/tr[2]/td/text()") else ""
        item[u"受理件内容"] = deal_ntr(
            html.xpath("(//table[@class='xjxq_tab'])[1]/tr[3]/td/text()")[0].strip() if html.xpath(
                "(//table[@class='xjxq_tab'])[1]/tr[3]/td/text()") else "")
        item[u"办理部门"] = html.xpath("(//table[@class='xjxq_tab'])[2]/tr[1]/td/text()")[0].strip() if html.xpath(
            "(//table[@class='xjxq_tab'])[2]/tr[1]/td/text()") else ""
        item[u"办理时间"] = html.xpath("(//table[@class='xjxq_tab'])[2]/tr[2]/td/text()")[0].strip() if html.xpath(
            "(//table[@class='xjxq_tab'])[2]/tr[2]/td/text()") else ""
        item[u"办理内容"] = deal_ntr(
            html.xpath("(//table[@class='xjxq_tab'])[2]/tr[3]/td/text()")[0].strip() if html.xpath(
                "(//table[@class='xjxq_tab'])[2]/tr[3]/td/text()") else "")
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
