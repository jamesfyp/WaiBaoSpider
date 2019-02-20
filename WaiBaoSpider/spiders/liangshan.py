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


class LiangShanSpider(scrapy.Spider):
    name = "liangshan"
    base_url = "http://12345.lsz.gov.cn/Flow/FlowPublic?PageNum={}"
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
        for i in range(1, 353):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//tr[@class='datarow']")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"来电来信编号"] = "'{}'".format(
                info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else "")
            item[u"类型"] = info.xpath("./td[2]/text()")[0].strip() if info.xpath("./td[2]/text()") else ""
            item[u"标题"] = info.xpath("./td[3]/a/text()")[0].strip() if info.xpath("./td[3]/a/text()") else ""
            item[u"发布时间"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"处理情况"] = info.xpath("./td[5]/text()")[0].strip() if info.xpath("./td[5]/text()") else ""
            item[u"链接"] = "http://12345.lsz.gov.cn{}".format(
                info.xpath("./td[3]/a/@href")[0].strip() if info.xpath("./td[3]/a/@href") else "")
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "bh": item[u"来电来信编号"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"信件标题"] = html.xpath("//table[@class='flow-detail-table']/tr[1]/td[2]/text()")[
            0].strip() if html.xpath("//table[@class='flow-detail-table']/tr[1]/td[2]/text()") else ""
        item[u"信件编号"] = data["bh"]
        item[u"来信时间"] = html.xpath("//table[@class='flow-detail-table']/tr[2]/td[4]/text()")[
            0].strip() if html.xpath("//table[@class='flow-detail-table']/tr[2]/td[4]/text()") else ""
        item[u"处理情况"] = html.xpath("//table[@class='flow-detail-table']/tr[3]/td[2]//text()") if html.xpath(
            "//table[@class='flow-detail-table']/tr[3]/td[2]//text()") else []
        item[u"处理情况"] = deal_ntr("".join(item[u"处理情况"]))
        item[u"内容"] = html.xpath("//table[@class='flow-detail-table']/tr[4]/td[2]//text()") if html.xpath(
            "//table[@class='flow-detail-table']/tr[4]/td[2]//text()") else []
        item[u"内容"] = deal_ntr("".join(item[u"内容"]))
        item[u"处理结果"] = html.xpath("//table[@class='flow-detail-table']/tr[5]/td[2]//text()") if html.xpath(
            "//table[@class='flow-detail-table']/tr[5]/td[2]//text()") else []
        item[u"处理结果"] = deal_ntr("".join(item[u"处理结果"]))
        item[u"满意度"] = html.xpath("//table[@class='flow-detail-table']/tr[6]/td[2]//text()") if html.xpath(
            "//table[@class='flow-detail-table']/tr[6]/td[2]//text()") else []
        item[u"满意度"] = deal_ntr("".join(item[u"满意度"]))
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
