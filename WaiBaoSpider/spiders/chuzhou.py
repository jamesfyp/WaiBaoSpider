# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class ChuzhouSpider(scrapy.Spider):
    name = 'chuzhou'
    base_url = "http://www.chuzhou.gov.cn/content/column/2983504?organId=&pageIndex={}"
    data_path = os.getcwd() + "/WaiBaoSpider/data/%s/" % name
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)

    def start_requests(self):
        for i in range(1, 349):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            print(url)
            yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//div[@class='lyy_listbox']/ul/li")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"信件类型"] = info.xpath(".//p[@class='p1']/text()")[0].strip() if info.xpath(
                ".//p[@class='p1']/text()") else ""
            item[u"信件编号"] = "'{}'".format(
                info.xpath(".//p[@class='p2']/text()")[0].strip() if info.xpath(".//p[@class='p2']/text()") else "")
            item[u"信件标题"] = info.xpath(".//p[@class='p3']/a/@title")[0].strip() if info.xpath(
                ".//p[@class='p3']/a/@title") else ""
            item[u"留言时间"] = info.xpath(".//p[@class='p4']/text()")[0].strip() if info.xpath(
                ".//p[@class='p4']/text()") else ""
            item[u"评价结果"] = info.xpath(".//p[@class='p5']/text()")[0].strip() if info.xpath(
                ".//p[@class='p5']/text()") else ""
            item[u"链接"] = info.xpath(".//p[@class='p3']/a/@href")[0].strip() if info.xpath(
                ".//p[@class='p3']/a/@href") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, meta={"url": item[u"链接"], "bnum": item[u"信件编号"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"标题"] = html.xpath("//h1[@class='mesgtitle']/text()")[0].strip() if html.xpath(
            "//h1[@class='mesgtitle']/text()") else ""
        item[u"编号"] = data["bnum"]
        item[u"来信时间"] = html.xpath("(//td[@class='nr'])[2]/div/text()")[0].strip() if html.xpath(
            "(//td[@class='nr'])[2]/div/text()") else ""
        item[u"类型"] = html.xpath("(//td[@class='nr'])[3]/text()")[0].strip() if html.xpath(
            "(//td[@class='nr'])[3]/text()") else ""
        item[u"网友"] = deal_ntr(html.xpath("(//td[@class='nr'])[4]/text()")[0].strip() if html.xpath(
            "(//td[@class='nr'])[4]/text()") else "")
        content = html.xpath("(//td[@class='nrtxt'])[1]//text()") if html.xpath(
            "(//td[@class='nrtxt'])[1]//text()") else []
        item[u"内容"] = deal_ntr("".join(content).strip())
        item[u"转办单位"] = html.xpath("(//td[@class='nr'])[5]/text()")[0].strip() if html.xpath(
            "(//td[@class='nr'])[5]/text()") else ""
        re_content = html.xpath("(//td[@class='nrtxt'])[2]//text()") if html.xpath(
            "(//td[@class='nrtxt'])[2]//text()") else []
        item[u"答复情况"] = deal_ntr("".join(re_content).strip())
        item[u"用户满意度评价"] = html.xpath("(//td[@class='nr'])[6]/text()")[0].strip() if html.xpath(
            "(//td[@class='nr'])[6]/text()") else ""
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
