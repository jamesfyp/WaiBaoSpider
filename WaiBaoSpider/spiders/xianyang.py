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


class XianYangSpider(scrapy.Spider):
    name = "xianyang"
    base_url = "http://www.xianyang.gov.cn/appeal/list.jsp?model_id=1&cur_page={}"
    base_url2 = "http://www.xianyang.gov.cn/appeal/list.jsp?model_id=4&cur_page={}"
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
        for i in range(1, 503):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers, meta={"source": u"市长信箱"})
        for i in range(1, 562):
            # for i in range(1, 2):
            url = self.base_url2.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers, meta={"source": u"部门信箱"})

    def parse_list(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        lines = html.xpath("//table[@class='mail_table']/tbody/tr")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"来源"] = data["source"]
            item[u"信件编号"] = "'{}'".format(
                info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else "")
            item[u"信件标题"] = info.xpath("./td[2]/a/text()")[0].strip() if info.xpath("./td[2]/a/text()") else ""
            item[u"来信时间"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"链接"] = "http://www.xianyang.gov.cn{}".format(
                info.xpath("./td[2]/a/@href")[0].strip() if info.xpath("./td[2]/a/@href") else "")
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "source": data["source"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"来源"] = data["source"]
        item[u"编号"] = "'{}'".format(
            html.xpath("(//table[@class='mail_content'])[1]/tr[2]/td/text()")[0].strip() if html.xpath(
                "(//table[@class='mail_content'])[1]/tr[2]/td/text()") else "")
        item[u"类型"] = html.xpath("(//table[@class='mail_content'])[1]/tr[3]/td/text()")[0].strip() if html.xpath(
            "(//table[@class='mail_content'])[1]/tr[3]/td/text()") else ""
        item[u"标题"] = html.xpath("(//table[@class='mail_content'])[1]/tr[4]/td/text()")[0].strip() if html.xpath(
            "(//table[@class='mail_content'])[1]/tr[4]/td/text()") else ""
        item[u"时间"] = html.xpath("(//table[@class='mail_content'])[1]/tr[5]/td/text()")[0].strip() if html.xpath(
            "(//table[@class='mail_content'])[1]/tr[5]/td/text()") else ""
        item[u"内容"] = deal_ntr(
            html.xpath("(//table[@class='mail_content'])[1]/tr[6]/td/text()")[0].strip() if html.xpath(
                "(//table[@class='mail_content'])[1]/tr[6]/td/text()") else "")
        item[u"受理单位"] = html.xpath("(//table[@class='mail_content'])[2]/tr[2]/td/text()")[
            0].strip() if html.xpath("(//table[@class='mail_content'])[2]/tr[2]/td/text()") else ""
        item[u"回复日期"] = html.xpath("(//table[@class='mail_content'])[2]/tr[3]/td/text()")[
            0].strip() if html.xpath("(//table[@class='mail_content'])[2]/tr[3]/td/text()") else ""
        item[u"回复内容"] = html.xpath("(//table[@class='mail_content'])[2]/tr[4]/td//text()") if html.xpath(
            "(//table[@class='mail_content'])[2]/tr[4]/td//text()") else []
        item[u"回复内容"] = deal_ntr("".join(item[u"回复内容"]))
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
