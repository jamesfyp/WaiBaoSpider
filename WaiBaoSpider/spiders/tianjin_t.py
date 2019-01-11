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


class TianJinTwoSpider(scrapy.Spider):
    name = "tianjintwo"
    base_url = "http://zm.tj.gov.cn/gov_open/question/zero/list8a.jsp?curpage={}&rows=15&deptId=1002000000000000"
    data_path = os.getcwd() + "/WaiBaoSpider/data/%s/" % name
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
        for i in range(1, 15491):
            # for i in range(1, 10):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//table[@align]/tr")[1:-1]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"类别"] = info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else ""
            item[u"标题"] = info.xpath("./td[2]/a/span/text()")[0].strip() if info.xpath("./td[2]/a/span/text()") else ""
            item[u"各区"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"日期"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"回复"] = info.xpath("./td[5]/text()")[0].strip() if info.xpath("./td[5]/text()") else ""
            item[u"状态"] = info.xpath("./td[6]/text()")[0].strip() if info.xpath("./td[6]/text()") else ""
            item[u"链接"] = info.xpath("./td[2]/a/@href")[0].strip() if info.xpath("./td[2]/a/@href") else ""
            self.dump_list.process_item(item)
            id = re.search(u"ly/\?id=(\d+)", item[u"链接"]).group(1)
            real_url = "http://zm.tj.gov.cn/gov_open/{}.html".format(id)
            yield Request(real_url, callback=self.parse_detail, headers=self.headers, meta={"url": item[u"链接"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"发表人"] = html.xpath("(//span[@class='content'])[1]/text()")[0].strip() if html.xpath(
            "(//span[@class='content'])[1]/text()") else ""
        item[u"提问时间"] = html.xpath("(//span[@class='content'])[2]/text()")[0].strip() if html.xpath(
            "(//span[@class='content'])[2]/text()") else ""
        item[u"标题"] = html.xpath("(//span[@class='content'])[3]/text()")[0].strip() if html.xpath(
            "(//span[@class='content'])[3]/text()") else ""
        item[u"内容"] = html.xpath("(//span[@class='content'])[4]//text()") if html.xpath(
            "(//span[@class='content'])[4]//text()") else []
        item[u"内容"] = deal_ntr("".join(item[u"内容"]))
        item[u"回复部门"] = html.xpath("(//span[@class='content'])[5]/a/text()")[0].strip() if html.xpath(
            "(//span[@class='content'])[5]/a/text()") else ""
        item[u"回复时间"] = html.xpath("(//span[@class='content'])[6]/text()")[0].strip().replace(u"&nbsp",
                                                                                              u"") if html.xpath(
            "(//span[@class='content'])[6]/text()") else ""
        item[u"是否超时"] = html.xpath("(//span[@class='content'])[7]/text()")[0].strip() if html.xpath(
            "(//span[@class='content'])[7]/text()") else ""
        item[u"回复标题"] = html.xpath("(//span[@class='content'])[8]/text()")[0].strip() if html.xpath(
            "(//span[@class='content'])[8]/text()") else ""
        item[u"回复内容"] = html.xpath("(//span[@class='content'])[9]//text()") if html.xpath(
            "(//span[@class='content'])[9]//text()") else []
        item[u"回复内容"] = deal_ntr("".join(item[u"回复内容"]))
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
