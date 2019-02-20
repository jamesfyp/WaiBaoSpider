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


class XianNingSpider(scrapy.Spider):
    name = "xianning"
    base_url = "http://wz.xianning.gov.cn/Home/AppealList?Length=4"
    data_path = os.getcwd() + "/WaiBaoSpider/data/"
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    custom_settings = {
        'DOWNLOAD_DELAY': 0.8,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36",
    }

    def start_requests(self):
        yield Request(self.base_url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//div[@id='content']/div")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"编号"] = "'{}'".format(
                info.xpath("./ul/a/li[1]/text()")[0].strip() if info.xpath("./ul/a/li[1]/text()") else "")
            item[u"类别"] = info.xpath("./ul/a/li[2]/text()")[0].strip() if info.xpath("./ul/a/li[2]/text()") else ""
            item[u"正在问"] = info.xpath("./ul/a/li[3]/text()")[0].strip() if info.xpath("./ul/a/li[3]/text()") else ""
            item[u"来信人"] = info.xpath("./ul/a/li[4]/text()")[0].strip() if info.xpath("./ul/a/li[4]/text()") else ""
            item[u"处理部门"] = info.xpath("./ul/a/li[5]/text()")[0].strip() if info.xpath("./ul/a/li[5]/text()") else ""
            item[u"状态"] = info.xpath("./ul/a/li[6]/text()")[0].strip() if info.xpath("./ul/a/li[6]/text()") else ""
            item[u"时间"] = info.xpath("./ul/a/li[7]/text()")[0].strip() if info.xpath("./ul/a/li[7]/text()") else ""
            item[u"链接"] = "http://wz.xianning.gov.cn{}".format(
                info.xpath("./ul/a/@href")[0].strip() if info.xpath("./ul/a/@href") else "")
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers, meta={"url": item[u"链接"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"诉求主题 "] = html.xpath("//table[@class='content']/tr[1]/td[2]/text()")[0].strip() if html.xpath(
            "//table[@class='content']/tr[1]/td[2]/text()") else ""
        item[u"来信人"] = html.xpath("//table[@class='content']/tr[2]/td[2]/text()")[0].strip() if html.xpath(
            "//table[@class='content']/tr[2]/td[2]/text()") else ""
        item[u"受理单位"] = html.xpath("//table[@class='content']/tr[3]/td[2]/text()")[0].strip() if html.xpath(
            "//table[@class='content']/tr[3]/td[2]/text()") else ""
        item[u"诉求时间"] = html.xpath("//table[@class='content']/tr[3]/td[4]/text()")[0].strip() if html.xpath(
            "//table[@class='content']/tr[3]/td[4]/text()") else ""
        item[u"来信类型"] = html.xpath("//table[@class='content']/tr[4]/td[2]/text()")[0].strip() if html.xpath(
            "//table[@class='content']/tr[4]/td[2]/text()") else ""
        item[u"办理状态"] = html.xpath("//table[@class='content']/tr[4]/td[4]//text()") if html.xpath(
            "//table[@class='content']/tr[4]/td[4]//text()") else []
        item[u"办理状态"] = deal_ntr("".join(item[u"办理状态"]))
        item[u"来信内容"] = html.xpath("//table[@class='content']/tr[5]/td[2]//text()") if html.xpath(
            "//table[@class='content']/tr[5]/td[2]//text()") else []
        item[u"来信内容"] = deal_ntr("".join(item[u"来信内容"]))
        item[u"办理跟踪"] = html.xpath("//div[@class='list_con']/ul/li//text()") if html.xpath(
            "//div[@class='list_con']/ul/li//text()") else []
        item[u"办理跟踪"] = deal_ntr("_".join(item[u"办理跟踪"]))
        item[u"单位回复"] = u"如在使用过程中遇到故障请致电：0715-8128121"
        item[u"处理单位"] = html.xpath("(//table[@class='content2'])[1]/tr[1]/td[2]/text()")[0].strip() if html.xpath(
            "(//table[@class='content2'])[1]/tr[1]/td[2]/text()") else ""
        item[u"处理时间"] = html.xpath("(//table[@class='content2'])[1]/tr[1]/td[4]/text()")[0].strip() if html.xpath(
            "(//table[@class='content2'])[1]/tr[1]/td[4]/text()") else ""
        item[u"回复内容"] = html.xpath("(//table[@class='content2'])[1]/tr[2]/td[2]//text()") if html.xpath(
            "(//table[@class='content2'])[1]/tr[2]/td[2]//text()") else []
        item[u"回复内容"] = deal_ntr("".join(item[u"回复内容"]))
        manyi = html.xpath("(//table[@class='content2'])[2]/tr[2]")
        if manyi:
            item[u"满意数"] = html.xpath("(//table[@class='content2'])[2]/tr[2]/td[1]/text()")[
                0].strip() if html.xpath("(//table[@class='content2'])[2]/tr[2]/td[1]/text()") else ""
            item[u"不满意数"] = html.xpath("(//table[@class='content2'])[2]/tr[2]/td[2]/text()")[
                0].strip() if html.xpath("(//table[@class='content2'])[2]/tr[2]/td[2]/text()") else ""
            item[u"满意率"] = html.xpath("(//table[@class='content2'])[2]/tr[2]/td[3]/text()")[
                0].strip() if html.xpath("(//table[@class='content2'])[2]/tr[2]/td[3]/text()") else ""
        else:
            item[u"满意数"] = ""
            item[u"不满意数"] = ""
            item[u"满意率"] = ""
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
