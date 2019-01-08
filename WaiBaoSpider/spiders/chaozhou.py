# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm

import scrapy
from scrapy import Request, FormRequest
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class ChaoZhouSpider(scrapy.Spider):
    name = "chaozhou"
    base_url = "http://www.chaozhou.gov.cn/event/v_list.jspx"
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
    data_form = {
        "typeId": "",
        "pageSize": "7",
        "pageNo": "",
        "deptId": "0",
        "year": "0",
    }

    def start_requests(self):
        for i in range(1, 545):
            # for i in range(1, 2):
            self.data_form["typeId"] = "1"
            self.data_form["pageNo"] = str(i)
            yield FormRequest(self.base_url, formdata=self.data_form, callback=self.parse_list, headers=self.headers,
                              meta={"lb": u"网上咨询"})
        for i in range(1, 582):
            # for i in range(1, 2):
            self.data_form["typeId"] = "2"
            self.data_form["pageNo"] = str(i)
            yield FormRequest(self.base_url, formdata=self.data_form, callback=self.parse_list, headers=self.headers,
                              meta={"lb": u"投诉举报"})

    def parse_list(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        lines = html.xpath("//table[@bgcolor='#d2d3d5']/tr")[1:]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"来源"] = data["lb"]
            item[u"主题"] = info.xpath("./td[1]/a/text()")[0].strip() if info.xpath("./td[1]/a/text()") else ""
            item[u"链接"] = "http://www.chaozhou.gov.cn{}".format(
                info.xpath("./td[1]/a/@href")[0].strip() if info.xpath("./td[1]/a/@href") else "")
            item[u"姓名"] = info.xpath("./td[2]/text()")[0].strip() if info.xpath("./td[2]/text()") else ""
            item[u"提交日期"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"回复单位"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"处理状态"] = info.xpath("./td[5]/text()")[0].strip() if info.xpath("./td[5]/text()") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "lb": item[u"来源"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"主题"] = html.xpath("//div[@id='div2']/table/tr[1]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@id='div2']/table/tr[1]/td[2]/text()") else ""
        item[u"提交日期"] = html.xpath("//div[@id='div2']/table/tr[2]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@id='div2']/table/tr[2]/td[2]/text()") else ""
        content = html.xpath("//div[@id='div2']/table/tr[3]/td[2]//text()") if html.xpath(
            "//div[@id='div2']/table/tr[3]/td[2]//text()") else []
        item[u"内容"] = deal_ntr("".join(content))
        item[u"收件人"] = deal_ntr(html.xpath("//div[@id='div2']/table/tr[4]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@id='div2']/table/tr[4]/td[2]/text()") else "")
        item[u"回复日期"] = html.xpath("//div[@id='div2']/table/tr[5]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@id='div2']/table/tr[5]/td[2]/text()") else ""
        item[u"回复人"] = deal_ntr(html.xpath("//div[@id='div2']/table/tr[6]/td[2]/text()")[0].strip() if html.xpath(
            "//div[@id='div2']/table/tr[6]/td[2]/text()") else "")
        re_content = html.xpath("//div[@id='div2']/table/tr[7]/td[2]//text()") if html.xpath(
            "//div[@id='div2']/table/tr[7]/td[2]//text()") else []
        item[u"回复内容"] = deal_ntr("".join(re_content))
        item[u"链接"] = data["url"]
        item[u"来源"] = data["lb"]
        self.dump_detail.process_item(item)
