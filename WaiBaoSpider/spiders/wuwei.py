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


class WuWeiSpider(scrapy.Spider):
    name = "wuwei"
    base_url = "http://www.ww.gansu.gov.cn/zmhd/szxx/index{}.htm"
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
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    }

    def start_requests(self):
        for i in range(1, 210):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//div[@class='sjhf']/table/tr")[1:]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"诉求类别"] = info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else ""
            item[u"诉求标题"] = info.xpath("./td[2]/div/a/text()")[0].strip() if info.xpath("./td[2]/div/a/text()") else ""
            item[u"链接"] = "http://www.ww.gansu.gov.cn/zmhd/szxx/{}".format(
                info.xpath("./td[2]/div/a/@href")[0].strip() if info.xpath("./td[2]/div/a/@href") else "")
            item[u"状态"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"时间"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers, meta={"url": item[u"链接"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"信件类型"] = html.xpath("(//div[@class='biaoge']/table)[1]/tr[1]/td[2]/text()")[
            0].strip() if html.xpath("(//div[@class='biaoge']/table)[1]/tr[1]/td[2]/text()") else ""
        item[u"来信时间"] = html.xpath("(//div[@class='biaoge']/table)[1]/tr[2]/td[2]/text()")[
            0].strip() if html.xpath("(//div[@class='biaoge']/table)[1]/tr[2]/td[2]/text()") else ""
        item[u"来信标题"] = html.xpath("(//div[@class='biaoge']/table)[1]/tr[3]/td[2]/text()")[
            0].strip() if html.xpath("(//div[@class='biaoge']/table)[1]/tr[3]/td[2]/text()") else ""
        item[u"来信内容"] = deal_ntr(
            html.xpath("(//div[@class='biaoge']/table)[1]/tr[4]/td[2]/text()")[0].strip() if html.xpath(
                "(//div[@class='biaoge']/table)[1]/tr[4]/td[2]/text()") else "")
        item[u"信件状态"] = html.xpath("(//div[@class='biaoge']/table)[2]/tr[1]/td[2]/text()")[
            0].strip() if html.xpath("(//div[@class='biaoge']/table)[2]/tr[1]/td[2]/text()") else ""
        item[u"回复时间"] = html.xpath("(//div[@class='biaoge']/table)[2]/tr[1]/td[4]/text()")[
            0].strip() if html.xpath("(//div[@class='biaoge']/table)[2]/tr[1]/td[4]/text()") else ""
        item[u"回复内容"] = html.xpath("(//div[@class='biaoge']/table)[2]/tr[2]/td[2]//text()") if html.xpath(
            "(//div[@class='biaoge']/table)[2]/tr[2]/td[2]//text()") else []
        item[u"回复内容"] = deal_ntr("".join(item[u"回复内容"]))
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
