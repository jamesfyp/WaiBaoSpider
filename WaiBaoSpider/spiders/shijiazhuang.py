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


class ShiJiaZhuangSpider(scrapy.Spider):
    name = "shijiazhuang"
    base_url = "http://new.sjz.gov.cn/zfxxinfolist.jsp?current={}&wid=1&cid=1259811582187"
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
        for i in range(1, 20800):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//table[@class='tably']")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"网友"] = info.xpath("./tr[1]/td[1]/table/tr[1]/td/text()")[
                0].strip().replace(u"网友：", u"") if info.xpath(
                "./tr[1]/td[1]/table/tr[1]/td/text()") else ""
            item[u"时间"] = info.xpath("./tr[1]/td[1]/table/tr[2]/td/text()")[
                0].strip().replace(u"时间：", u"") if info.xpath(
                "./tr[1]/td[1]/table/tr[2]/td/text()") else ""
            item[u"留言对象"] = info.xpath("./tr[1]/td[1]/table/tr[3]/td/text()")[
                0].strip().replace(u"留言对象：", u"") if info.xpath(
                "./tr[1]/td[1]/table/tr[3]/td/text()") else ""
            item[u"留言内容"] = deal_ntr(info.xpath("./tr[1]/td[2]/table/tr/td/text()")[
                                         0].strip() if info.xpath(
                "./tr[1]/td[2]/table/tr/td/text()") else "")
            item[u"回复时间"] = info.xpath("./tr[2]/td[1]/table/tr[1]/td/text()")[
                0].strip().replace(u"时间：", u"") if info.xpath(
                "./tr[2]/td[1]/table/tr[1]/td/text()") else ""
            item[u"回复部门"] = info.xpath("./tr[2]/td[1]/table/tr[2]/td/text()")[
                0].strip().replace(u"回复部门：", u"") if info.xpath(
                "./tr[2]/td[1]/table/tr[2]/td/text()") else ""
            item[u"回复内容"] = deal_ntr(info.xpath("./tr[2]/td[2]/table/tr/td/text()")[
                                         0].strip() if info.xpath(
                "./tr[2]/td[2]/table/tr/td/text()") else "")
            item[u"链接"] = response.url
            self.dump_list.process_item(item)
    #         yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers, meta={"url": item[u"链接"]})
    #
    # def parse_detail(self, response):
    #     body = unicode_body(response)
    #     html = etree.HTML(body)
    #     item = {}
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
    #     self.dump_detail.process_item(item)
