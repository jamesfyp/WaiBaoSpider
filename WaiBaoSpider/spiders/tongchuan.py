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


class TongChuanSpider(scrapy.Spider):
    name = "tongchuan"
    base_url = "http://www.tongchuan.gov.cn/news_list.rt?mailType=0&titleNumber=30&newsNumber=10&step=1&sort=7&type=1&isTuijian=2&channlId=181&pageNo={}"
    data_path = os.getcwd() + "/WaiBaoSpider/data/%s/" % name
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }

    def start_requests(self):
        for i in range(1, 1196):
            # for i in range(1, 12):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//table[@class='shouli_tab']/tr")[1:]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"受理编号"] = info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else ""
            item[u"信件标题题"] = info.xpath("./td[2]/a/text()")[0].strip() if info.xpath("./td[2]/a/text()") else ""
            item[u"受理时间"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"办理部门"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"办理状态"] = info.xpath("./td[5]/span/text()")[0].strip() if info.xpath("./td[5]/span/text()") else ""
            item[u"链接"] = "http://www.tongchuan.gov.cn{}".format(
                info.xpath("./td[2]/a/@href")[0].strip() if info.xpath("./td[2]/a/@href") else "")
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers, meta={"url": item[u"链接"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"姓名"] = html.xpath("//div[@class='yisq']/table[1]/tr[1]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@class='yisq']/table[1]/tr[1]/td[2]/text()") else ""
        item[u"来信时间"] = html.xpath("//div[@class='yisq']/table[1]/tr[2]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@class='yisq']/table[1]/tr[2]/td[2]/text()") else ""
        item[u"是否公开"] = html.xpath("//div[@class='yisq']/table[1]/tr[3]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@class='yisq']/table[1]/tr[3]/td[2]/text()") else ""
        item[u"信件主题"] = html.xpath("//div[@class='yisq']/table[1]/tr[4]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@class='yisq']/table[1]/tr[4]/td[2]/text()") else ""
        item[u"信件内容"] = html.xpath("//div[@class='yisq']/table[1]/tr[5]/td[2]//text()") if html.xpath(
            "//div[@class='yisq']/table[1]/tr[5]/td[2]//text()") else []
        item[u"信件内容"] = deal_ntr("".join(item[u"信件内容"]))
        item[u"受理时间"] = html.xpath("//div[@class='yisq']/table[2]/tr[1]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@class='yisq']/table[2]/tr[1]/td[2]/text()") else ""
        item[u"办理时间"] = html.xpath("//div[@class='yisq']/table[2]/tr[2]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@class='yisq']/table[2]/tr[2]/td[2]/text()") else ""
        item[u"办理部门"] = html.xpath("//div[@class='yisq']/table[2]/tr[3]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@class='yisq']/table[2]/tr[3]/td[2]/text()") else ""
        item[u"办理状态"] = html.xpath("//div[@class='yisq']/table[2]/tr[4]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@class='yisq']/table[2]/tr[4]/td[2]/text()") else ""
        item[u"办理情况"] = html.xpath("//div[@class='yisq']/table[2]/tr[5]/td[2]//text()") if html.xpath(
            "//div[@class='yisq']/table[2]/tr[5]/td[2]//text()") else []
        item[u"办理情况"] = deal_ntr("".join(item[u"办理情况"]))
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
