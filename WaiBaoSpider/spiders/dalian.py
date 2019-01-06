# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class DalianSpider(scrapy.Spider):
    name = 'dalian'
    base_url = "http://xzfw.dl.gov.cn/fgw/gzjl/xjlb_{}.jspx"
    data_path = os.getcwd() + "/WaiBaoSpider/data/dalian/"
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    def start_requests(self):
        for i in range(1, 379):
            url = self.base_url.format(i)
            print(url)
            yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//ul[@class='mt10']/li")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"信件编号"] = info.xpath("./a[1]/text()")[0].strip() if info.xpath("./a[1]/text()") else ""
            item[u"信件标题"] = info.xpath("./a[2]/span/text()")[0].strip() if info.xpath("./a[2]/span/text()") else ""
            item[u"链接"] = "http://xzfw.dl.gov.cn{}".format(info.xpath("./a[2]/@href")[0])
            item[u"类型"] = info.xpath("./a[3]/text()")[0].strip() if info.xpath("./a[3]/text()") else ""
            item[u"状态"] = info.xpath("./a[4]/text()")[0].strip() if info.xpath("./a[4]/text()") else ""
            item[u"办理单位"] = info.xpath("./a[5]/text()")[0].strip() if info.xpath("./a[5]/text()") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail,
                          meta={"slbh": item[u"信件编号"], "blzt": item[u"状态"], "title": item[u"信件标题"],
                                "sldw": item[u"办理单位"], "url": item[u"链接"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"受理编号"] = data.get("slbh", "")
        item[u"处理状态"] = data.get("blzt", "")
        item[u"反映标题"] = data.get("title", "")
        item[u"受理单位"] = data.get("sldw", "")
        item[u"链接"] = data.get("url", "")
        item[u"反映内容"] = deal_ntr(
            html.xpath("//table/tbody/tr[3]/td/text()")[0] if html.xpath("//table/tbody/tr[3]/td/text()") else "")
        item[u"答复内容"] = deal_ntr(
            html.xpath("//table/tbody/tr[5]/td/text()")[0] if html.xpath("//table/tbody/tr[5]/td/text()") else "")
        item[u"反映时间"] = html.xpath("//table/tbody/tr[6]/td[1]/text()")[0].strip() if html.xpath(
            "//table/tbody/tr[6]/td[1]/text()") else ""
        item[u"反馈时间"] = html.xpath("//table/tbody/tr[6]/td[2]/text()")[0].strip() if html.xpath(
            "//table/tbody/tr[6]/td[2]/text()") else ""
        self.dump_detail.process_item(item)
